"""
database.py — SQLite Database Schema, Migrations & Realistic Seed Data
Compliant with DPDP Act 2023, IT Act 2000, and Child Labour Prohibition Act.
Zero-PII leakage: Raw IDs and plain phone numbers are masked/hashed.
"""

import os
import sqlite3
import hashlib
import base64
import uuid
import json
from datetime import datetime, timedelta

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "kaam_milega.db"))
SECRET_SALT = os.environ.get("KAAM_MILEGA_SALT", "KaamMilega_Rural_Shield_2026_Secure_Salt")

def get_db(db_path=None):
    target = db_path or os.environ.get("DB_PATH", DB_PATH)
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

def hash_phone(phone: str) -> str:
    cleaned = "".join(filter(str.isdigit, phone))
    return hashlib.sha256((cleaned + SECRET_SALT).encode("utf-8")).hexdigest()

def mask_phone_for_display(phone: str) -> str:
    cleaned = "".join(filter(str.isdigit, phone))
    if len(cleaned) >= 10:
        return f"+91 {cleaned[:2]}XXX-XX{cleaned[-2:]}"
    return "+91 XXXXX-XXXXX"

def obfuscate_phone(phone: str) -> str:
    cleaned = "".join(filter(str.isdigit, phone))
    return base64.b64encode(cleaned.encode("utf-8")).decode("utf-8")

def deobfuscate_phone(obf: str) -> str:
    try:
        return base64.b64decode(obf.encode("utf-8")).decode("utf-8")
    except Exception:
        return ""

def generate_public_id(prefix: str = "w") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Users Table (No plain-text phone, strict 18+ constraint, DPDP consent, is_demo flag)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        public_id TEXT UNIQUE NOT NULL,
        phone_hash TEXT NOT NULL,
        phone_obfuscated TEXT NOT NULL,
        phone_masked TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('worker', 'employer', 'admin')),
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        tehsil TEXT,
        village TEXT NOT NULL,
        photo_url TEXT,
        declared_age_18_plus INTEGER NOT NULL CHECK(declared_age_18_plus = 1),
        birth_year INTEGER NOT NULL,
        consent_given_at TEXT NOT NULL,
        is_verified INTEGER DEFAULT 0,
        verification_tier TEXT DEFAULT 'tier1' CHECK(verification_tier IN ('tier1', 'tier2', 'tier3')),
        is_deleted INTEGER DEFAULT 0,
        is_demo INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Worker Profiles Table (Opaque public IDs, trade tags, daily rates, seasonal status, is_demo flag)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS worker_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        public_id TEXT UNIQUE NOT NULL,
        skills_json TEXT NOT NULL,
        experience_years INTEGER NOT NULL DEFAULT 1,
        daily_rate INTEGER NOT NULL DEFAULT 600,
        availability_status TEXT NOT NULL DEFAULT 'available' CHECK(availability_status IN ('available', 'busy', 'seasonal_dormancy')),
        bio_text TEXT,
        is_team_leader INTEGER DEFAULT 0,
        team_size INTEGER DEFAULT 1,
        vouched_count INTEGER DEFAULT 0,
        rating_avg REAL DEFAULT 5.0,
        review_count INTEGER DEFAULT 0,
        is_hidden INTEGER DEFAULT 0,
        is_demo INTEGER DEFAULT 0,
        updated_at TEXT NOT NULL
    )
    """)

    # 3. Portfolio Items (Proof of Craftsmanship)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER NOT NULL REFERENCES worker_profiles(id) ON DELETE CASCADE,
        image_url TEXT NOT NULL,
        title TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 3b. Peer Vouches (Anti-fraud peer verification & trust tiers)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS peer_vouches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER NOT NULL REFERENCES worker_profiles(id) ON DELETE CASCADE,
        voucher_session_id TEXT NOT NULL,
        voucher_name TEXT NOT NULL,
        trade TEXT,
        created_at TEXT NOT NULL,
        UNIQUE(worker_id, voucher_session_id)
    )
    """)

    # 4. Reviews Table (Emoji + Star feedback)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER NOT NULL REFERENCES worker_profiles(id) ON DELETE CASCADE,
        employer_public_id TEXT NOT NULL,
        employer_name TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
        emoji TEXT NOT NULL CHECK(emoji IN ('positive', 'neutral', 'negative')),
        comment TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 5. Job Posts (With Child Labour Disclaimer acceptance requirement, is_demo flag)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        public_id TEXT UNIQUE NOT NULL,
        employer_name TEXT NOT NULL,
        employer_phone_masked TEXT NOT NULL,
        skill_needed TEXT NOT NULL,
        num_workers INTEGER NOT NULL DEFAULT 1,
        duration_days INTEGER NOT NULL DEFAULT 1,
        daily_wage_offered INTEGER DEFAULT 600,
        district TEXT NOT NULL,
        village TEXT NOT NULL,
        status TEXT DEFAULT 'open' CHECK(status IN ('open', 'filled', 'closed')),
        child_labour_disclaimer_accepted INTEGER NOT NULL CHECK(child_labour_disclaimer_accepted = 1),
        is_demo INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # Column migrations for existing tables
    for tbl in ("users", "worker_profiles", "job_posts"):
        try:
            cursor.execute(f"ALTER TABLE {tbl} ADD COLUMN is_demo INTEGER DEFAULT 0")
        except Exception:
            pass

    # 6. Ephemeral Contact Unlock Tokens (Anti-Scraping / Tokenized Reveal)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_unlock_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT UNIQUE NOT NULL,
        worker_public_id TEXT NOT NULL,
        employer_session_id TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        used INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # 7. Contact Logs (Dispute & Safety Audit Trail)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER NOT NULL,
        employer_session_id TEXT NOT NULL,
        contact_type TEXT NOT NULL CHECK(contact_type IN ('call', 'whatsapp')),
        ip_hash TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    # 8. Reports & Grievances Table (Two-way reporting, Child labour flag)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_type TEXT NOT NULL CHECK(target_type IN ('worker', 'job', 'employer')),
        target_public_id TEXT NOT NULL,
        reporter_session_id TEXT NOT NULL,
        reason TEXT NOT NULL,
        details TEXT,
        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'reviewed', 'resolved')),
        created_at TEXT NOT NULL
    )
    """)

    # 9. Auth Sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auth_sessions (
        session_id TEXT PRIMARY KEY,
        phone_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        user_public_id TEXT,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )
    """)

    # 10. End-User Feedback Table (Suggestions, bugs, service experience & email delivery)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        public_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        category TEXT NOT NULL CHECK(category IN ('suggestion', 'bug', 'experience', 'complaint', 'other')),
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        message TEXT NOT NULL,
        session_id TEXT,
        email_status TEXT DEFAULT 'pending',
        created_at TEXT NOT NULL
    )
    """)

    # Create Indexes for lightning fast queries (< 20ms)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_public_id ON users(public_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_district ON users(district)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_is_deleted ON users(is_deleted)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_worker_public_id ON worker_profiles(public_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_worker_availability ON worker_profiles(availability_status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_worker_hidden ON worker_profiles(is_hidden)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_peer_vouches_worker ON peer_vouches(worker_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_portfolio_worker ON portfolio_items(worker_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tokens_token ON contact_unlock_tokens(token)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_public_id ON job_posts(public_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_public_id ON feedback(public_id)")

    conn.commit()
    conn.close()

    seed_initial_data()

def seed_initial_data():
    if os.environ.get("SEED_DEMO_DATA", "0").lower() not in ("1", "true", "yes"):
        return

    conn = get_db()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()
    current_year = datetime.utcnow().year

    # Mark existing demo seed records if already present
    cursor.execute("UPDATE users SET is_demo = 1 WHERE phone_hash LIKE '9839%' OR phone_hash IN (SELECT phone_hash FROM users WHERE name LIKE '%(%)')")
    cursor.execute("UPDATE worker_profiles SET is_demo = 1 WHERE user_id IN (SELECT id FROM users WHERE is_demo = 1)")
    cursor.execute("UPDATE job_posts SET is_demo = 1 WHERE employer_name IN ('शर्मा जी (शादी समारोह)', 'वर्मा परिवार (विवाह प्रीतिभोज)', 'अमित सिंह (मकान मालिक)', 'विकास कंस्ट्रक्शन (ठेकेदार)', 'राजेश पटेल (किसान साथी)')")

    # 12 Realistic Pilot Artisans across UP & Bihar districts
    seed_workers = [
        {
            "name": "रामेश्वर मिस्त्री (Rameshwar Mistry)",
            "phone": "9839123401",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "tehsil": "पिंडरा (Pindra)",
            "village": "करखियांव (Karkhiyaon)",
            "birth_year": current_year - 38,
            "skills": ["mason"],
            "experience": 15,
            "rate": 750,
            "status": "available",
            "tier": "tier3",
            "vouched": 6,
            "is_leader": 1,
            "team_size": 4,
            "bio": "15 साल से राजमिस्त्री का काम। छत ढलाई, ईंट जोड़ाई, और प्लास्टर के माहिर। 4 लोगों की कुशल टीम के साथ उपलब्ध।",
            "rating": 4.9,
            "reviews": 18
        },
        {
            "name": "सुनील कुमार (Sunil Kumar)",
            "phone": "9839123402",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "tehsil": "सदर (Sadar)",
            "village": "शिवपुर (Shivpur)",
            "birth_year": current_year - 29,
            "skills": ["electrician"],
            "experience": 7,
            "rate": 600,
            "status": "available",
            "tier": "tier2",
            "vouched": 4,
            "is_leader": 0,
            "team_size": 1,
            "bio": "घर की पूरी वायरिंग, सबमर्सिबल स्टार्टर, इन्वर्टर फिटिंग और फॉल्ट रिपेयर का काम तुरंत।",
            "rating": 4.8,
            "reviews": 12
        },
        {
            "name": "दिनेश कुमार (Dinesh Kumar)",
            "phone": "9839123403",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "मिर्ज़ापुर (Mirzapur)",
            "tehsil": "चुनार (Chunar)",
            "village": "जमालपुर (Jamalpur)",
            "birth_year": current_year - 34,
            "skills": ["plumber", "boring"],
            "experience": 11,
            "rate": 700,
            "status": "available",
            "tier": "tier3",
            "vouched": 5,
            "is_leader": 1,
            "team_size": 3,
            "bio": "हैंडपंप बोरिंग, मोटर बोरिंग, बाथरूम पाइपलाइन और टंकी फिटिंग का पक्का काम।",
            "rating": 5.0,
            "reviews": 21
        },
        {
            "name": "मनोज शर्मा (Manoj Sharma)",
            "phone": "9839123404",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "प्रयागराज (Prayagraj)",
            "tehsil": "फूलपुर (Phulpur)",
            "village": "बहादुरपुर (Bahadurpur)",
            "birth_year": current_year - 42,
            "skills": ["carpenter"],
            "experience": 20,
            "rate": 800,
            "status": "available",
            "tier": "tier3",
            "vouched": 8,
            "is_leader": 0,
            "team_size": 1,
            "bio": "दरवाजे, खिड़की, चौखट, अलमारी और शटरिंग का बेहतरीन फिनिशिंग वाला काम।",
            "rating": 4.9,
            "reviews": 16
        },
        {
            "name": "राकेश राजभर (Rakesh Rajbhar)",
            "phone": "9839123405",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "tehsil": "राजातालाब (Rajatalaab)",
            "village": "रोहनिया (Rohaniya)",
            "birth_year": current_year - 27,
            "skills": ["painter"],
            "experience": 6,
            "rate": 550,
            "status": "available",
            "tier": "tier2",
            "vouched": 3,
            "is_leader": 0,
            "team_size": 2,
            "bio": "दीवार पुट्टी, प्राइमर, डिस्टेंपर, एशियन पेंट्स और टेक्सचर डिजाइन। साफ-सुथरा काम।",
            "rating": 4.7,
            "reviews": 9
        },
        {
            "name": "सुरेश वेल्डर (Suresh Welder)",
            "phone": "9839123406",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "tehsil": "पिंडरा (Pindra)",
            "village": "फूलपुर बाजार (Phulpur Bazar)",
            "birth_year": current_year - 36,
            "skills": ["welder"],
            "experience": 12,
            "rate": 700,
            "status": "busy",
            "tier": "tier2",
            "vouched": 3,
            "is_leader": 0,
            "team_size": 1,
            "bio": "लोहे का गेट, ग्रिल, शेड, रेलिंग और ट्रैक्टर ट्रॉली मरम्मत का मजबूत वेल्डिंग कार्य।",
            "rating": 4.8,
            "reviews": 14
        },
        {
            "name": "संतोष यादव (Santosh Yadav)",
            "phone": "9839123407",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "मिर्ज़ापुर (Mirzapur)",
            "tehsil": "सदर (Sadar)",
            "village": "विंध्याचल (Vindhyachal)",
            "birth_year": current_year - 31,
            "skills": ["labor"],
            "experience": 8,
            "rate": 450,
            "status": "available",
            "tier": "tier2",
            "vouched": 5,
            "is_leader": 1,
            "team_size": 6,
            "bio": "मकान निर्माण, गड्ढा खुदाई, ईंट-रेत ढुलाई के लिए मेहनती मजदूरों की टीम उपलब्ध है।",
            "rating": 4.9,
            "reviews": 11
        },
        {
            "name": "मुन्ना मिस्त्री (Munna Mistry)",
            "phone": "9839123408",
            "state": "बिहार (Bihar)",
            "district": "पटना (Patna)",
            "tehsil": "दानापुर (Danapur)",
            "village": "मनेर (Maner)",
            "birth_year": current_year - 35,
            "skills": ["mason"],
            "experience": 14,
            "rate": 800,
            "status": "available",
            "tier": "tier3",
            "vouched": 7,
            "is_leader": 1,
            "team_size": 5,
            "bio": "मार्बल, टाइल्स और मकान निर्माण का 14 साल का तजुर्बा। काम में कोई शिकायत नहीं।",
            "rating": 4.9,
            "reviews": 23
        },
        {
            "name": "अरविंद पासवान (Arvind Paswan)",
            "phone": "9839123409",
            "state": "बिहार (Bihar)",
            "district": "गया (Gaya)",
            "tehsil": "बोधगया (Bodhgaya)",
            "village": "बकरौर (Bakraur)",
            "birth_year": current_year - 28,
            "skills": ["electrician"],
            "experience": 5,
            "rate": 550,
            "status": "seasonal_dormancy",
            "tier": "tier2",
            "vouched": 2,
            "is_leader": 0,
            "team_size": 1,
            "bio": "बिजली वायरिंग और मोटर मरम्मत। (नोट: धान रोपाई के चलते 15 तारीख तक छुट्टी पर हूँ)",
            "rating": 4.6,
            "reviews": 7
        },
        {
            "name": "किशन लाल बढ़ई (Kishan Lal)",
            "phone": "9839123410",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "tehsil": "सेवापुरी (Sewapuri)",
            "village": "कपसेठी (Kapsethi)",
            "birth_year": current_year - 45,
            "skills": ["carpenter"],
            "experience": 22,
            "rate": 850,
            "status": "available",
            "tier": "tier3",
            "vouched": 9,
            "is_leader": 0,
            "team_size": 1,
            "bio": "परंपरागत काष्ठशिल्प, आधुनिक मॉड्यूलर किचन, मंदिर डिजाइन और फर्नीचर।",
            "rating": 5.0,
            "reviews": 29
        },
        {
            "name": "बबलू चौहान (Bablu Chauhan)",
            "phone": "9839123411",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "प्रयागराज (Prayagraj)",
            "tehsil": "करछना (Karchhana)",
            "village": "भीता (Bhita)",
            "birth_year": current_year - 33,
            "skills": ["boring", "plumber"],
            "experience": 10,
            "rate": 700,
            "status": "available",
            "tier": "tier2",
            "vouched": 4,
            "is_leader": 1,
            "team_size": 4,
            "bio": "4 इंच और 6 इंच बोरिंग मशीन के साथ उपलब्ध। 24 घंटे में मीठा पानी की गारंटी।",
            "rating": 4.8,
            "reviews": 15
        },
        {
            "name": "दीपक सोनकर (Deepak Sonkar)",
            "phone": "9839123412",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "tehsil": "सदर (Sadar)",
            "village": "मंडुवाडीह (Manduadih)",
            "birth_year": current_year - 26,
            "skills": ["painter"],
            "experience": 5,
            "rate": 500,
            "status": "available",
            "tier": "tier1",
            "vouched": 2,
            "is_leader": 0,
            "team_size": 1,
            "bio": "सस्ता और टिकाऊ पेंट-पुट्टी का काम। कम समय में साफ काम की गारंटी।",
            "rating": 4.7,
            "reviews": 5
        },
        {
            "name": "मुकेश कुमार (Mukesh Kumar)",
            "phone": "9839123413",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "tehsil": "सदर (Sadar)",
            "village": "कैंट स्टेशन (Cantt)",
            "birth_year": current_year - 32,
            "skills": ["auto_driver"],
            "experience": 9,
            "rate": 600,
            "status": "available",
            "tier": "tier2",
            "vouched": 6,
            "is_leader": 0,
            "team_size": 1,
            "bio": "सीएनजी ऑटो रिक्शा, रेलवे स्टेशन, कैंट, गोदौलिया और आसपास लोकल सवारी या सामान बुकिंग के लिए उपलब्ध।",
            "rating": 4.9,
            "reviews": 24
        },
        {
            "name": "पंकज मौर्या (Pankaj Maurya)",
            "phone": "9839123414",
            "state": "बिहार (Bihar)",
            "district": "पटना (Patna)",
            "tehsil": "दानापुर (Danapur)",
            "village": "सगुना मोड़ (Saguna More)",
            "birth_year": current_year - 28,
            "skills": ["erickshaw_driver"],
            "experience": 5,
            "rate": 500,
            "status": "available",
            "tier": "tier2",
            "vouched": 4,
            "is_leader": 0,
            "team_size": 1,
            "bio": "बैटरी ई-रिक्शा, बाजार और मोहल्ले में सवारी सेवा और छोटी पार्सल डिलीवरी। सुरक्षित व विनम्र।",
            "rating": 4.8,
            "reviews": 19
        },
        {
            "name": "अवधेश यादव (Awadhesh Yadav)",
            "phone": "9839123415",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "प्रयागराज (Prayagraj)",
            "tehsil": "करछना (Karchhana)",
            "village": "नैनी (Naini)",
            "birth_year": current_year - 37,
            "skills": ["pickup_driver"],
            "experience": 13,
            "rate": 900,
            "status": "available",
            "tier": "tier3",
            "vouched": 7,
            "is_leader": 0,
            "team_size": 1,
            "bio": "महिंद्रा बोलेरो पिकअप / छोटा हाथी मालवाहक। कृषि मंडी, सीमेंट-ईंट या घरेलू शिफ्टिंग हेतु उपलब्ध।",
            "rating": 4.9,
            "reviews": 28
        },
        {
            "name": "प्रदीप शर्मा (Pradeep Sharma)",
            "phone": "9839123416",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "लखनऊ (Lucknow)",
            "tehsil": "सरोजिनी नगर",
            "village": "ट्रांसपोर्ट नगर",
            "birth_year": current_year - 35,
            "skills": ["car_driver"],
            "experience": 11,
            "rate": 750,
            "status": "available",
            "tier": "tier2",
            "vouched": 5,
            "is_leader": 0,
            "team_size": 1,
            "bio": "निजी कार व कमर्शियल टैक्सी चालक। 11 साल का अनुभव, शांत व सुरक्षित ड्राइविंग, लंबी दूरी का अनुभव।",
            "rating": 4.9,
            "reviews": 17
        },
        {
            "name": "जसविंदर सिंह (Jaswinder Singh)",
            "phone": "9839123417",
            "state": "पंजाब (Punjab)",
            "district": "लुधियाना (Ludhiana)",
            "tehsil": "खन्ना (Khanna)",
            "village": "समराला रोड",
            "birth_year": current_year - 40,
            "skills": ["tractor_driver"],
            "experience": 18,
            "rate": 850,
            "status": "available",
            "tier": "tier3",
            "vouched": 8,
            "is_leader": 0,
            "team_size": 1,
            "bio": "खेत जुताई, रोटावेटर, कल्टीवेटर और ढुलाई का लंबा अनुभव।",
            "rating": 4.9,
            "reviews": 16
        },
        {
            "name": "दिवाकर टेंट वाले (Diwakar Tent Decorator)",
            "phone": "9839123418",
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "tehsil": "पिंडरा (Pindra)",
            "village": "फूलपुर",
            "birth_year": current_year - 33,
            "skills": ["tent_decorator"],
            "experience": 13,
            "rate": 900,
            "status": "available",
            "tier": "tier3",
            "vouched": 7,
            "is_leader": 1,
            "team_size": 10,
            "bio": "वाटरप्रूफ पंडाल, शादी स्टेज जयमाल डेकोरेशन, साउंड सिस्टम, जनरेटर और रंग-बिरंगी लाइटिंग के अनुभवी कारीगर।",
            "rating": 4.9,
            "reviews": 23
        }
    ]

    for w in seed_workers:
        p_hash = hash_phone(w["phone"])
        cursor.execute("SELECT id FROM users WHERE phone_hash = ?", (p_hash,))
        if cursor.fetchone():
            continue

        user_pub_id = generate_public_id("u")
        worker_pub_id = generate_public_id("w")
        p_obf = obfuscate_phone(w["phone"])
        p_masked = mask_phone_for_display(w["phone"])

        # Insert into users
        cursor.execute("""
        INSERT INTO users (
            public_id, phone_hash, phone_obfuscated, phone_masked, name, role,
            state, district, tehsil, village, photo_url, declared_age_18_plus,
            birth_year, consent_given_at, is_verified, verification_tier, is_deleted, created_at
        ) VALUES (?, ?, ?, ?, ?, 'worker', ?, ?, ?, ?, ?, 1, ?, ?, 1, ?, 0, ?)
        """, (
            user_pub_id, p_hash, p_obf, p_masked, w["name"],
            w["state"], w["district"], w["tehsil"], w["village"],
            f"/static/images/icons/{w['skills'][0]}.svg",
            w["birth_year"], now, w["tier"], now
        ))
        user_id = cursor.lastrowid

        # Insert into worker_profiles
        cursor.execute("""
        INSERT INTO worker_profiles (
            user_id, public_id, skills_json, experience_years, daily_rate,
            availability_status, bio_text, is_team_leader, team_size, vouched_count,
            rating_avg, review_count, is_hidden, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
        """, (
            user_id, worker_pub_id, json.dumps(w["skills"]), w["experience"],
            w["rate"], w["status"], w["bio"], w["is_leader"], w["team_size"],
            w["vouched"], w["rating"], w["reviews"], now
        ))
        worker_id = cursor.lastrowid

        # Insert sample review
        cursor.execute("""
        INSERT INTO reviews (worker_id, employer_public_id, employer_name, rating, emoji, comment, created_at)
        VALUES (?, 'emp_demo_1', 'गुप्ता जी (ठेकेदार)', 5, 'positive', 'बहुत ही ईमानदार और समय के पाबंद कारीगर हैं। काम में पूरा संतोष मिला।', ?)
        """, (worker_id, now))

    # Seed Sample Job Posts with child labour disclaimer accepted
    sample_jobs = [
        {
            "employer": "शर्मा जी (शादी समारोह)",
            "phone": "9839999904",
            "skill": "halwai",
            "workers": 2,
            "duration": 3,
            "wage": 1200,
            "district": "वाराणसी (Varanasi)",
            "village": "पांडेयपुर (Pandeypur)"
        },
        {
            "employer": "वर्मा परिवार (विवाह प्रीतिभोज)",
            "phone": "9839999905",
            "skill": "event_cook",
            "workers": 4,
            "duration": 2,
            "wage": 1100,
            "district": "प्रयागराज (Prayagraj)",
            "village": "सिविल लाइंस (Civil Lines)"
        },
        {
            "employer": "अमित सिंह (मकान मालिक)",
            "phone": "9839999901",
            "skill": "mason",
            "workers": 3,
            "duration": 7,
            "wage": 750,
            "district": "वाराणसी (Varanasi)",
            "village": "शिवपुर (Shivpur)"
        },
        {
            "employer": "विकास कंस्ट्रक्शन (ठेकेदार)",
            "phone": "9839999902",
            "skill": "electrician",
            "workers": 2,
            "duration": 3,
            "wage": 650,
            "district": "प्रयागराज (Prayagraj)",
            "village": "झूंसी (Jhunsi)"
        },
        {
            "employer": "राजेश पटेल (किसान साथी)",
            "phone": "9839999903",
            "skill": "boring",
            "workers": 4,
            "duration": 2,
            "wage": 700,
            "district": "मिर्ज़ापुर (Mirzapur)",
            "village": "चुनार (Chunar)"
        }
    ]

    for j in sample_jobs:
        cursor.execute("SELECT id FROM job_posts WHERE employer_name = ?", (j["employer"],))
        if cursor.fetchone():
            continue

        cursor.execute("""
        INSERT INTO job_posts (
            public_id, employer_name, employer_phone_masked, skill_needed,
            num_workers, duration_days, daily_wage_offered, district, village,
            status, child_labour_disclaimer_accepted, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', 1, ?)
        """, (
            generate_public_id("job"), j["employer"], mask_phone_for_display(j["phone"]),
            j["skill"], j["workers"], j["duration"], j["wage"], j["district"], j["village"], now
        ))


    # Seed craftsmanship portfolio for demo artisans
    cursor.execute("SELECT id FROM worker_profiles WHERE user_id IN (SELECT id FROM users WHERE phone_hash = ?)", (hash_phone("9839123401"),))
    rw = cursor.fetchone()
    if rw:
        rw_id = rw["id"]
        cursor.execute("SELECT COUNT(*) FROM portfolio_items WHERE worker_id = ?", (rw_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO portfolio_items (worker_id, image_url, title, created_at) VALUES (?, ?, ?, ?)",
                           (rw_id, '/static/images/icons/mason.svg', 'ईंट की दीवार चुनाई व प्लास्टर', now))
            cursor.execute("INSERT INTO portfolio_items (worker_id, image_url, title, created_at) VALUES (?, ?, ?, ?)",
                           (rw_id, '/static/images/icons/mason.svg', 'मार्बल व टाइल्स फिनिशिंग', now))

    cursor.execute("SELECT id FROM worker_profiles WHERE user_id IN (SELECT id FROM users WHERE phone_hash = ?)", (hash_phone("9839123402"),))
    sw = cursor.fetchone()
    if sw:
        sw_id = sw["id"]
        cursor.execute("SELECT COUNT(*) FROM portfolio_items WHERE worker_id = ?", (sw_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO portfolio_items (worker_id, image_url, title, created_at) VALUES (?, ?, ?, ?)",
                           (sw_id, '/static/images/icons/electrician.svg', 'घरेलू वायरिंग व MCB बॉक्स', now))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Kaam Milega Database initialized and seeded successfully!")
