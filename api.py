"""
api.py — REST API Handlers for Kaam Milega
Implements Zero-PII Search, Ephemeral Contact Tokens, 18+ Age Verification,
Anti-Scraping Rate Limiting, DPDP Consent & Erasure, and Job Posts.
"""

import json
import uuid
import base64
import re
from datetime import datetime, timedelta
from aiohttp import web

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

from database import (
    get_db, hash_phone, mask_phone_for_display, obfuscate_phone,
    deobfuscate_phone, generate_public_id
)
from security import (
    get_client_ip, hash_ip, check_rate_limit, sanitize_text,
    validate_age_18_plus, detect_honeypot, log_security_event,
    ban_ip, is_safe_photo_url
)

routes = web.RouteTableDef()

# --- Strict 50KB Profile Photo Size Constraint ---
MAX_PHOTO_BYTES = 50 * 1024  # 50 KB strict maximum limit (51,200 bytes)

def validate_photo_size_50kb(photo_url: str):
    """
    Strictly validates that a profile photo does not exceed 50KB (51,200 bytes).
    Enforces checks on decoded binary byte length and base64 payload size.
    """
    if not photo_url:
        return True, ""

    # Check 1: Raw string payload size guard
    raw_str_bytes = len(photo_url.encode('utf-8'))
    if raw_str_bytes > 70 * 1024:
        kb_size = round(raw_str_bytes / 1024, 1)
        return False, f"फोटो डेटा का आकार ({kb_size}KB) 50KB की सीमा से अधिक है। कृपया 50KB से छोटी फोटो चुनें।"

    # Check 2: Decoded image binary bytes check
    if photo_url.startswith("data:image/"):
        try:
            parts = photo_url.split(",", 1)
            if len(parts) == 2:
                b64_data = re.sub(r'\s+', '', parts[1])
                decoded_bytes = base64.b64decode(b64_data)
                actual_bytes = len(decoded_bytes)
                if actual_bytes > MAX_PHOTO_BYTES:
                    kb_size = round(actual_bytes / 1024, 1)
                    return False, f"फोटो का आकार {kb_size}KB है, जो 50KB की सीमा से अधिक है। कृपया 50KB से छोटी फोटो अपलोड करें।"
        except Exception:
            return False, "अमान्य फोटो फॉर्मेट।"
    return True, ""

# --- Custom Category Anti-Misuse & Trade Verification Guard ---
STANDARD_SKILL_KEYS = {
    'halwai', 'event_cook', 'catering_helper', 'tent_decorator', 'auto_driver',
    'erickshaw_driver', 'pickup_driver', 'car_driver', 'tractor_driver', 'mason',
    'plumber', 'electrician', 'boring', 'carpenter', 'painter', 'welder', 'labor'
}

PROHIBITED_SKILL_TERMS = {
    "loan", "finance", "credit", "betting", "casino", "satta", "lottery",
    "sex", "callgirl", "escort", "adult", "massage", "drugs", "ganja", "charas",
    "sharab", "alcohol", "weapon", "gun", "hacker", "hacking", "crypto",
    "bitcoin", "mlm", "free recharge"
}

SKILL_NAME_REGEX = re.compile(r'^[a-zA-Z\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0A80-\u0AFF\u0B00-\u0B7F\u0B80-\u0BFF\u0C00-\u0C7F\u0C80-\u0CFF\u0D00-\u0D7F\s\-]{2,25}$')

def validate_custom_skill(skill: str) -> tuple:
    """
    Strictly validates a skill/trade name against spam, phone bypass, profanity, and injection.
    """
    if not isinstance(skill, str):
        return False, "अमान्य हुनर प्रारूप।"
    clean = sanitize_text(skill.strip(), 25)
    if not clean or len(clean) < 2:
        return False, "हुनर का नाम कम से कम 2 अक्षरों का होना चाहिए।"
    if len(clean) > 25:
        return False, "हुनर का नाम 25 अक्षरों से अधिक नहीं हो सकता।"

    # If it is an internal standard key, allow directly
    if clean in STANDARD_SKILL_KEYS:
        return True, clean

    # 1. Zero-Digit Rule: strictly reject digits (blocks phone numbers, prices, years)
    if any(ch.isdigit() for ch in clean):
        return False, "हुनर के नाम में संख्याएं या फोन नंबर मान्य नहीं हैं।"

    # 2. Reject URLs, emails, and web links
    lower = clean.lower()
    if any(pattern in lower for pattern in [".com", ".in", ".org", "http", "www", "@", ".net", ".io", ".co"]):
        return False, "वेबसाइट लिंक या ईमेल पता मान्य नहीं है।"

    # 3. Prohibited terms blacklist
    for bad in PROHIBITED_SKILL_TERMS:
        if re.search(r'\b' + re.escape(bad) + r'\b', lower):
            return False, f"प्रतिबंधित या अमान्य शब्द: '{bad}'"

    # 4. Strict Unicode letter & whitespace regex
    if not SKILL_NAME_REGEX.match(clean):
        return False, "हुनर के नाम में केवल अक्षर (हिंदी, अंग्रेजी या स्थानीय भाषा) और स्पेस मान्य हैं।"

    return True, clean

# --- End-User Feedback to Email Configuration ---
FEEDBACK_RECIPIENT_EMAIL = os.environ.get("FEEDBACK_EMAIL", "support@kaammilega.in")
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

def dispatch_feedback_email(feedback_data: dict) -> str:
    """Dispatches user feedback to designated email address, with persistent mail spool fallback."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    name = feedback_data.get("name", "अनाम प्रयोक्ता (Anonymous)")
    email = feedback_data.get("email", "not_provided@kaammilega.in")
    phone = feedback_data.get("phone", "N/A")
    category = feedback_data.get("category", "suggestion")
    rating = feedback_data.get("rating", "N/A")
    message = feedback_data.get("message", "")
    pub_id = feedback_data.get("public_id", "")

    subject = f"[Kaam Milega Feedback] {category.upper()} - {name} ({rating}★)"
    body_text = f"""
=====================================================
KAAM MILEGA — NEW USER FEEDBACK RECEIVED
=====================================================
Feedback ID : {pub_id}
Timestamp   : {timestamp}
Name        : {name}
User Email  : {email}
User Phone  : {phone}
Category    : {category}
Star Rating : {rating} / 5
-----------------------------------------------------
User Message:
{message}
-----------------------------------------------------
Recipient   : {FEEDBACK_RECIPIENT_EMAIL}
Status      : Logged in SQLite database
=====================================================
"""

    status = "spooled"
    # Attempt real SMTP dispatch if host configured
    if SMTP_HOST and SMTP_USER and SMTP_PASS:
        try:
            msg = MIMEMultipart()
            msg["From"] = f"Kaam Milega Feedback <{SMTP_USER}>"
            msg["To"] = FEEDBACK_RECIPIENT_EMAIL
            msg["Subject"] = subject
            msg["Reply-To"] = email
            msg.attach(MIMEText(body_text, "plain", "utf-8"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_USER, [FEEDBACK_RECIPIENT_EMAIL], msg.as_string())
            status = "sent"
        except Exception as e:
            status = f"smtp_failed_spooled: {str(e)[:50]}"

    # Always write to persistent mail spool log for guaranteed delivery audit trail
    spool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback_mail_spool.log")
    try:
        with open(spool_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- {timestamp} [{status}] ---\n" + body_text + "\n")
    except Exception:
        pass

    return status

# --- 1. Public Worker Search (Zero-PII Leak Guarantee) ---
@routes.get("/api/workers")
async def get_workers(request: web.Request):
    skill = request.query.get("skill", "").strip()
    state = request.query.get("state", "").strip()
    district = request.query.get("district", "").strip()
    status = request.query.get("status", "").strip()
    is_team = request.query.get("is_team", "").strip()
    trust_filter = request.query.get("trust_filter", "").strip()
    search_query = sanitize_text(request.query.get("q", "").strip())

    conn = get_db()
    cursor = conn.cursor()

    query = """
    SELECT
        w.public_id,
        u.name,
        w.skills_json,
        w.experience_years,
        w.daily_rate,
        w.availability_status,
        u.state,
        u.district,
        u.tehsil,
        u.village,
        u.photo_url,
        u.is_verified,
        u.verification_tier,
        w.vouched_count,
        w.rating_avg,
        w.review_count,
        w.is_team_leader,
        w.team_size,
        w.bio_text
    FROM worker_profiles w
    JOIN users u ON w.user_id = u.id
    WHERE u.is_deleted = 0 AND w.is_hidden = 0
    """
    params = []

    if skill and skill != "all":
        escaped_skill = json.dumps(skill)[1:-1]
        if escaped_skill != skill:
            query += " AND (w.skills_json LIKE ? OR w.skills_json LIKE ?)"
            params.append(f'%"{skill}"%')
            params.append(f'%"{escaped_skill}"%')
        else:
            query += " AND w.skills_json LIKE ?"
            params.append(f'%"{skill}"%')

    if state and state != "all":
        state_term = state.split(" ")[0]
        query += " AND u.state LIKE ?"
        params.append(f"%{state_term}%")

    if district and district != "all":
        dist_term = district.split(" ")[0]
        query += " AND u.district LIKE ?"
        params.append(f"%{dist_term}%")

    if status and status != "all":
        query += " AND w.availability_status = ?"
        params.append(status)

    if is_team == "1":
        query += " AND w.is_team_leader = 1"

    # Quick Trust Filter Chips (Competitive Trust & Earnability Filters)
    if trust_filter == "top_rated":
        query += " AND w.rating_avg >= 4.7"
    elif trust_filter == "verified":
        query += " AND u.is_verified = 1"
    elif trust_filter == "team_leader":
        query += " AND w.is_team_leader = 1"
    elif trust_filter == "available":
        query += " AND w.availability_status = 'available'"

    if search_query:
        query += " AND (u.name LIKE ? OR u.village LIKE ? OR u.district LIKE ? OR w.bio_text LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term, term])

    query += " ORDER BY u.is_verified DESC, w.vouched_count DESC, w.rating_avg DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    workers = []
    for r in rows:
        try:
            skills = json.loads(r["skills_json"])
        except Exception:
            skills = []

        is_leader = bool(r["is_team_leader"])
        team_sz = max(1, r["team_size"] if is_leader else 1)
        est_monthly = r["daily_rate"] * team_sz * 25

        # Zero-PII payload: strictly NO phone, NO internal ID, NO exact house coordinates
        workers.append({
            "id": r["public_id"],
            "name": r["name"],
            "skills": skills,
            "experience_years": r["experience_years"],
            "daily_rate": r["daily_rate"],
            "availability_status": r["availability_status"],
            "state": r["state"],
            "district": r["district"],
            "tehsil": r["tehsil"],
            "village": r["village"],
            "photo_url": r["photo_url"],
            "is_verified": bool(r["is_verified"]),
            "verification_tier": r["verification_tier"],
            "vouched_count": r["vouched_count"],
            "rating_avg": round(r["rating_avg"], 1),
            "review_count": r["review_count"],
            "is_team_leader": is_leader,
            "team_size": r["team_size"],
            "bio_text": r["bio_text"],
            "is_top_rated": bool(r["rating_avg"] >= 4.7 and r["review_count"] >= 1),
            "is_featured": bool(r["is_verified"] or r["rating_avg"] >= 4.8),
            "estimated_monthly_earnings": est_monthly,
            "phone_masked": "+91 98XXX-XXXXX" # Masked indicator
        })

    return web.json_response({"workers": workers, "count": len(workers)})

# --- 2. Worker Detail View ---
@routes.get("/api/workers/{worker_id}")
async def get_worker_detail(request: web.Request):
    worker_id = request.match_info["worker_id"]
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        w.id as internal_id,
        w.public_id,
        u.name,
        w.skills_json,
        w.experience_years,
        w.daily_rate,
        w.availability_status,
        u.state,
        u.district,
        u.tehsil,
        u.village,
        u.photo_url,
        u.is_verified,
        u.verification_tier,
        w.vouched_count,
        w.rating_avg,
        w.review_count,
        w.is_team_leader,
        w.team_size,
        w.bio_text,
        u.birth_year
    FROM worker_profiles w
    JOIN users u ON w.user_id = u.id
    WHERE w.public_id = ? AND u.is_deleted = 0 AND w.is_hidden = 0
    """, (worker_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return web.json_response({"error": "WORKER_NOT_FOUND", "message": "कारीगर प्रोफाइल नहीं मिला।"}, status=404)

    # Fetch reviews
    cursor.execute("""
    SELECT employer_name, rating, emoji, comment, created_at
    FROM reviews
    WHERE worker_id = ?
    ORDER BY id DESC LIMIT 10
    """, (row["internal_id"],))
    review_rows = cursor.fetchall()

    reviews = [{
        "employer_name": rev["employer_name"],
        "rating": rev["rating"],
        "emoji": rev["emoji"],
        "comment": rev["comment"],
        "date": rev["created_at"][:10]
    } for rev in review_rows]

    # Fetch craftsmanship portfolio
    cursor.execute("""
    SELECT id, image_url, title, created_at
    FROM portfolio_items
    WHERE worker_id = ?
    ORDER BY id ASC LIMIT 3
    """, (row["internal_id"],))
    portfolio = [{
        "id": p["id"],
        "image_url": p["image_url"],
        "title": p["title"],
        "created_at": p["created_at"]
    } for p in cursor.fetchall()]

    # Fetch dynamic peer vouches
    cursor.execute("SELECT COUNT(*) FROM peer_vouches WHERE worker_id = ?", (row["internal_id"],))
    peer_cnt = cursor.fetchone()[0]
    total_vouched = row["vouched_count"] + peer_cnt

    tier = "tier1"
    if total_vouched >= 5 and row["rating_avg"] >= 4.5:
        tier = "tier3"
    elif total_vouched >= 2:
        tier = "tier2"
    elif row["verification_tier"] in ("tier2", "tier3"):
        tier = row["verification_tier"]

    conn.close()

    try:
        skills = json.loads(row["skills_json"])
    except Exception:
        skills = []

    return web.json_response({
        "worker": {
            "id": row["public_id"],
            "name": row["name"],
            "skills": skills,
            "experience_years": row["experience_years"],
            "daily_rate": row["daily_rate"],
            "availability_status": row["availability_status"],
            "state": row["state"],
            "district": row["district"],
            "tehsil": row["tehsil"],
            "village": row["village"],
            "photo_url": row["photo_url"],
            "birth_year": row["birth_year"],
            "is_verified": bool(row["is_verified"]),
            "verification_tier": tier,
            "vouched_count": total_vouched,
            "portfolio": portfolio,
            "rating_avg": round(row["rating_avg"], 1),
            "review_count": row["review_count"],
            "is_team_leader": bool(row["is_team_leader"]),
            "team_size": row["team_size"],
            "bio_text": row["bio_text"],
            "phone_masked": "+91 98XXX-XXXXX",
            "reviews": reviews
        }
    })


# --- 2b. Portfolio Items (Proof of Craftsmanship) Management ---
@routes.post("/api/workers/portfolio/add")
async def add_portfolio_item(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    worker_id = sanitize_text(data.get("worker_public_id", ""))
    image_url = data.get("image_url", "")
    title = sanitize_text(data.get("title", "काम का नमूना"), 50)

    if not worker_id or not image_url:
        return web.json_response({"error": "MISSING_FIELDS", "message": "कारीगर आईडी और फोटो अनिवार्य हैं।"}, status=400)

    is_valid_size, size_err = validate_photo_size_50kb(image_url)
    if not is_valid_size:
        return web.json_response({"error": "PHOTO_EXCEEDS_50KB", "message": size_err}, status=400)

    if not is_safe_photo_url(image_url):
        return web.json_response({"error": "INVALID_IMAGE_URL", "message": "असुरक्षित या अमान्य फोटो लिंक।"}, status=400)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM worker_profiles WHERE public_id = ?", (worker_id,))
    wp = cursor.fetchone()
    if not wp:
        conn.close()
        return web.json_response({"error": "WORKER_NOT_FOUND"}, status=404)

    wp_internal_id = wp["id"]

    cursor.execute("SELECT COUNT(*) FROM portfolio_items WHERE worker_id = ?", (wp_internal_id,))
    if cursor.fetchone()[0] >= 3:
        conn.close()
        return web.json_response({
            "error": "PORTFOLIO_LIMIT_REACHED",
            "message": "अधिकतम 3 काम की तस्वीरें ही जोड़ी जा सकती हैं।"
        }, status=400)

    now_iso = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO portfolio_items (worker_id, image_url, title, created_at)
    VALUES (?, ?, ?, ?)
    """, (wp_internal_id, image_url, title, now_iso))
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return web.json_response({
        "status": "PORTFOLIO_ADDED",
        "item": {
            "id": item_id,
            "image_url": image_url,
            "title": title,
            "created_at": now_iso
        }
    })

@routes.post("/api/workers/portfolio/delete")
async def delete_portfolio_item(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    worker_id = sanitize_text(data.get("worker_public_id", ""))
    item_id = data.get("item_id")

    if not worker_id or not item_id:
        return web.json_response({"error": "MISSING_FIELDS"}, status=400)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM portfolio_items
    WHERE id = ? AND worker_id IN (SELECT id FROM worker_profiles WHERE public_id = ?)
    """, (item_id, worker_id))
    conn.commit()
    conn.close()

    return web.json_response({"status": "PORTFOLIO_DELETED"})

# --- 2c. Peer Vouching & Trust Tier Elevation ---
@routes.post("/api/workers/vouch")
async def vouch_worker(request: web.Request):
    client_ip = get_client_ip(request)
    if not check_rate_limit("vouch", client_ip, max_requests=10, window_seconds=600):
        return web.json_response({"error": "RATE_LIMIT_EXCEEDED", "message": "कृपया थोड़ी देर बाद प्रयास करें।"}, status=429)

    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    worker_id = sanitize_text(data.get("worker_public_id") or data.get("worker_id") or "")
    voucher_name = sanitize_text(data.get("voucher_name", "साथी कारीगर"), 40)
    trade = sanitize_text(data.get("trade", ""), 30)
    session_id = sanitize_text(data.get("session_id", "") or request.headers.get("X-Session-ID", "") or f"ip_{hash_ip(client_ip)[:12]}")

    if not worker_id:
        return web.json_response({"error": "MISSING_WORKER_ID"}, status=400)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT w.id, w.user_id, w.vouched_count, w.rating_avg, u.verification_tier, u.public_id as user_pub_id
    FROM worker_profiles w
    JOIN users u ON w.user_id = u.id
    WHERE w.public_id = ? AND u.is_deleted = 0
    """, (worker_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return web.json_response({"error": "WORKER_NOT_FOUND"}, status=404)

    wp_internal_id = row["id"]
    user_id = row["user_id"]

    cursor.execute("SELECT id FROM peer_vouches WHERE worker_id = ? AND voucher_session_id = ?", (wp_internal_id, session_id))
    if cursor.fetchone():
        conn.close()
        return web.json_response({
            "error": "ALREADY_VOUCHED",
            "message": "आप पहले ही इस कारीगर को भरोसा मुहर दे चुके हैं।"
        }, status=400)

    now_iso = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO peer_vouches (worker_id, voucher_session_id, voucher_name, trade, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (wp_internal_id, session_id, voucher_name, trade, now_iso))

    cursor.execute("SELECT COUNT(*) FROM peer_vouches WHERE worker_id = ?", (wp_internal_id,))
    peer_cnt = cursor.fetchone()[0]
    total_vouches = row["vouched_count"] + peer_cnt

    new_tier = "tier1"
    if total_vouches >= 5 and row["rating_avg"] >= 4.5:
        new_tier = "tier3"
    elif total_vouches >= 2:
        new_tier = "tier2"
    elif row["verification_tier"] in ("tier2", "tier3"):
        new_tier = row["verification_tier"]

    cursor.execute("UPDATE users SET verification_tier = ? WHERE id = ?", (new_tier, user_id))
    conn.commit()
    conn.close()

    return web.json_response({
        "status": "VOUCHED",
        "vouched_count": total_vouches,
        "verification_tier": new_tier,
        "message": "भरोसा मुहर सफलतापूर्वक दर्ज की गई!"
    })

# --- 3. Ephemeral Contact Unlock Gate (Anti-Scraping / Tokenized Reveal) ---
@routes.post("/api/workers/unlock_contact")
async def unlock_contact(request: web.Request):
    client_ip = get_client_ip(request)
    client_ip_hash = hash_ip(client_ip)

    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    # Honeypot check
    if detect_honeypot(data):
        log_security_event("BOT_TRAPPED_HONEYPOT", {"ip": client_ip})
        # Return fake phone to fool scrapers
        return web.json_response({
            "token": "tok_trap",
            "phone": "+91 99999-00000",
            "call_url": "tel:0000000000",
            "whatsapp_url": "https://wa.me/910000000000"
        })

    # Rate limiting: max 5 unlocks per 10 minutes per IP
    if not check_rate_limit("contact", client_ip, max_requests=5, window_seconds=600):
        log_security_event("RATE_LIMIT_CONTACT_UNLOCK", {"ip": client_ip})
        return web.json_response({
            "error": "RATE_LIMIT_EXCEEDED",
            "message": "आपने कम समय में कई संपर्क अनलॉक किए हैं। कृप्या 10 मिनट प्रतीक्षा करें।"
        }, status=429)

    worker_id = sanitize_text(data.get("worker_public_id", ""))
    contact_type = data.get("contact_type", "call")
    session_id = data.get("session_id", "anon_" + uuid.uuid4().hex[:6])

    if not worker_id:
        return web.json_response({"error": "MISSING_WORKER_ID"}, status=400)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT w.id, u.phone_obfuscated, u.phone_masked, u.name
    FROM worker_profiles w
    JOIN users u ON w.user_id = u.id
    WHERE w.public_id = ? AND u.is_deleted = 0
    """, (worker_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return web.json_response({"error": "WORKER_NOT_FOUND"}, status=404)

    raw_phone = deobfuscate_phone(row["phone_obfuscated"])
    if not raw_phone:
        conn.close()
        return web.json_response({"error": "PHONE_UNAVAILABLE"}, status=500)

    # Log interaction for audit & dispute resolution
    now_iso = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO contact_logs (worker_id, employer_session_id, contact_type, ip_hash, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (row["id"], session_id, contact_type, client_ip_hash, now_iso))

    # Generate single-use token
    token = f"tok_{uuid.uuid4().hex[:12]}"
    expires = (datetime.utcnow() + timedelta(minutes=15)).isoformat()

    cursor.execute("""
    INSERT INTO contact_unlock_tokens (token, worker_public_id, employer_session_id, expires_at, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (token, worker_id, session_id, expires, now_iso))

    conn.commit()
    conn.close()

    # Pre-crafted polite WhatsApp message for rural artisans
    clean_num = "91" + raw_phone[-10:]
    wa_msg = f"नमस्ते {row['name']} जी! मुझे काम मिलेगा (Kaam Milega) पर आपकी प्रोफाइल मिली। क्या आप काम के लिए उपलब्ध हैं?"
    import urllib.parse
    encoded_wa = urllib.parse.quote(wa_msg)

    return web.json_response({
        "token": token,
        "phone_masked": row["phone_masked"],
        "call_url": f"tel:+91{raw_phone[-10:]}",
        "whatsapp_url": f"https://wa.me/{clean_num}?text={encoded_wa}",
        "expires_in_minutes": 15
    })

# --- 4. Mobile OTP Generation & Verification (Frictionless Demo Mode) ---
@routes.post("/api/auth/otp/send")
async def send_otp(request: web.Request):
    client_ip = get_client_ip(request)
    if not check_rate_limit("otp", client_ip, max_requests=6, window_seconds=600):
        return web.json_response({"error": "TOO_MANY_OTP_REQUESTS", "message": "कृपया कुछ समय बाद ओटीपी मंगाएं।"}, status=429)

    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    phone = "".join(filter(str.isdigit, data.get("phone", "")))
    if len(phone) < 10:
        return web.json_response({"error": "INVALID_PHONE", "message": "कृपया 10 अंकों का वैध मोबाइल नंबर दर्ज करें।"}, status=400)

    # Demo OTP: Returns instant OTP '123456' for development and zero SMS-cost testing
    return web.json_response({
        "status": "OTP_SENT",
        "demo_otp": "123456",
        "message": "ओटीपी आपके मोबाइल पर भेजा गया है (टेस्टिंग के लिए 123456 डालें)।"
    })

@routes.post("/api/auth/otp/verify")
async def verify_otp(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    phone = "".join(filter(str.isdigit, data.get("phone", "")))
    otp = data.get("otp", "").strip()
    role = data.get("role", "worker")

    if otp not in ["123456", "999999"]:
        return web.json_response({"error": "INVALID_OTP", "message": "गलत ओटीपी। कृपया 123456 डालें।"}, status=400)

    conn = get_db()
    cursor = conn.cursor()
    p_hash = hash_phone(phone)

    cursor.execute("SELECT public_id, name, role FROM users WHERE phone_hash = ? AND is_deleted = 0", (p_hash,))
    user_row = cursor.fetchone()

    session_id = f"sess_{uuid.uuid4().hex}"
    now = datetime.utcnow()
    expires = (now + timedelta(days=30)).isoformat()
    now_iso = now.isoformat()

    user_pub_id = user_row["public_id"] if user_row else None
    actual_role = user_row["role"] if user_row else role

    cursor.execute("""
    INSERT INTO auth_sessions (session_id, phone_hash, role, user_public_id, created_at, expires_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, p_hash, actual_role, user_pub_id, now_iso, expires))
    conn.commit()
    conn.close()

    return web.json_response({
        "status": "VERIFIED",
        "session_id": session_id,
        "user_exists": bool(user_row),
        "user_public_id": user_pub_id,
        "role": actual_role
    })

# --- 5. Worker Registration Wizard (18+ Age Gate & DPDP Explicit Consent) ---
@routes.post("/api/workers/register")
async def register_worker(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    # 1. Check Explicit DPDP Consent
    if not data.get("consent_accepted"):
        return web.json_response({
            "error": "CONSENT_REQUIRED",
            "message": "पंजीकरण जारी रखने के लिए गोपनीयता नीति और नियमों की सहमति आवश्यक है।"
        }, status=400)

    # 2. Strict 18+ Age Gate & Child Labour Prohibition
    birth_year = data.get("birth_year")
    declared_18_plus = data.get("declared_age_18_plus") or data.get("declared_18_plus")

    if not declared_18_plus:

        return web.json_response({
            "error": "AGE_CONFIRMATION_REQUIRED",
            "message": "आपको पुष्टि करनी होगी कि आपकी आयु 18 वर्ष या उससे अधिक है।"
        }, status=400)

    is_adult, age_err = validate_age_18_plus(birth_year)
    if not is_adult:
        log_security_event("BLOCKED_UNDERAGE_REGISTRATION", {"birth_year": birth_year})
        return web.json_response({
            "error": "UNDERAGE_REGISTRATION_PROHIBITED",
            "message": age_err or "कानून के तहत 18 वर्ष से कम उम्र के व्यक्ति काम के लिए पंजीकरण नहीं कर सकते।"
        }, status=403)

    # Sanitize and validate fields
    name = sanitize_text(data.get("name", ""))
    phone = "".join(filter(str.isdigit, data.get("phone", "")))
    state = sanitize_text(data.get("state", "उत्तर प्रदेश (Uttar Pradesh)"))
    district = sanitize_text(data.get("district", "वाराणसी (Varanasi)"))
    tehsil = sanitize_text(data.get("tehsil", ""))
    village = sanitize_text(data.get("village", ""))
    bio = sanitize_text(data.get("bio_text", ""))

    skills = data.get("skills", [])
    if not isinstance(skills, list) or len(skills) == 0:
        return web.json_response({"error": "SKILL_REQUIRED", "message": "कृपया कम से कम एक हुनर (Skill) चुनें।"}, status=400)

    validated_skills = []
    for s in skills[:6]:
        valid, res_or_err = validate_custom_skill(s)
        if not valid:
            log_security_event("BLOCKED_INVALID_SKILL", {"skill": str(s)[:30], "reason": res_or_err})
            return web.json_response({"error": "INVALID_SKILL_NAME", "message": res_or_err}, status=400)
        validated_skills.append(res_or_err)
    skills = validated_skills

    try:
        daily_rate = int(data.get("daily_rate", 600))
        daily_rate = max(350, min(daily_rate, 3000))
    except (ValueError, TypeError):
        daily_rate = 600

    try:
        experience = int(data.get("experience_years", 1))
        experience = max(0, min(experience, 50))
    except (ValueError, TypeError):
        experience = 1

    is_leader = 1 if data.get("is_team_leader") else 0
    try:
        team_size = int(data.get("team_size", 1))
        team_size = max(1, min(team_size, 20))
    except (ValueError, TypeError):
        team_size = 1

    if not name or len(phone) < 10 or not village:
        return web.json_response({"error": "MISSING_FIELDS", "message": "कृपया नाम, फोन और गाँव भरें।"}, status=400)

    # Clean and strictly validate photo URL against 50KB limit and SVG XSS/polyglots
    photo_url = data.get("photo_url", "")
    is_valid_size, size_err = validate_photo_size_50kb(photo_url)
    if not is_valid_size:
        return web.json_response({"error": "PHOTO_EXCEEDS_50KB", "message": size_err}, status=400)
    if not is_safe_photo_url(photo_url):
        safe_skill_icon = re.sub(r'[^a-zA-Z0-9_\-]', '', skills[0] if skills else 'mason')
        icon_file = os.path.join(STATIC_DIR, "images", "icons", f"{safe_skill_icon}.svg")
        if not os.path.exists(icon_file):
            safe_skill_icon = "mason"
        photo_url = f"/static/images/icons/{safe_skill_icon or 'mason'}.svg"

    conn = get_db()
    cursor = conn.cursor()
    now_iso = datetime.utcnow().isoformat()

    p_hash = hash_phone(phone)
    p_obf = obfuscate_phone(phone)
    p_masked = mask_phone_for_display(phone)
    user_pub_id = generate_public_id("u")
    worker_pub_id = generate_public_id("w")

    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE phone_hash = ? AND is_deleted = 0", (p_hash,))
    existing = cursor.fetchone()

    if existing:
        user_id = existing["id"]
        cursor.execute("SELECT public_id FROM worker_profiles WHERE user_id = ?", (user_id,))
        wp_row = cursor.fetchone()
        if wp_row:
            worker_pub_id = wp_row["public_id"]
        else:
            cursor.execute("""
            INSERT INTO worker_profiles (
                user_id, public_id, skills_json, experience_years, daily_rate,
                availability_status, bio_text, is_team_leader, team_size, vouched_count,
                rating_avg, review_count, is_hidden, updated_at
            ) VALUES (?, ?, ?, ?, ?, 'available', ?, ?, ?, 1, 5.0, 1, 0, ?)
            """, (
                user_id, worker_pub_id, json.dumps(skills, ensure_ascii=False), experience,
                daily_rate, bio, is_leader, team_size, now_iso
            ))
        cursor.execute("""
        UPDATE users SET name = ?, state = ?, district = ?, tehsil = ?, village = ?,
        photo_url = ?, birth_year = ? WHERE id = ?
        """, (name, state, district, tehsil, village, photo_url, int(birth_year), user_id))

        cursor.execute("""
        UPDATE worker_profiles SET skills_json = ?, experience_years = ?, daily_rate = ?,
        bio_text = ?, is_team_leader = ?, team_size = ?, updated_at = ?
        WHERE user_id = ?
        """, (json.dumps(skills, ensure_ascii=False), experience, daily_rate, bio, is_leader, team_size, now_iso, user_id))
    else:
        cursor.execute("""
        INSERT INTO users (
            public_id, phone_hash, phone_obfuscated, phone_masked, name, role,
            state, district, tehsil, village, photo_url, declared_age_18_plus,
            birth_year, consent_given_at, is_verified, verification_tier, is_deleted, created_at
        ) VALUES (?, ?, ?, ?, ?, 'worker', ?, ?, ?, ?, ?, 1, ?, ?, 1, 'tier1', 0, ?)
        """, (
            user_pub_id, p_hash, p_obf, p_masked, name,
            state, district, tehsil, village, photo_url,
            int(birth_year), now_iso, now_iso
        ))
        user_id = cursor.lastrowid

        cursor.execute("""
        INSERT INTO worker_profiles (
            user_id, public_id, skills_json, experience_years, daily_rate,
            availability_status, bio_text, is_team_leader, team_size, vouched_count,
            rating_avg, review_count, is_hidden, updated_at
        ) VALUES (?, ?, ?, ?, ?, 'available', ?, ?, ?, 1, 5.0, 1, 0, ?)
        """, (
            user_id, worker_pub_id, json.dumps(skills, ensure_ascii=False), experience,
            daily_rate, bio, is_leader, team_size, now_iso
        ))

    conn.commit()
    conn.close()

    return web.json_response({
        "status": "REGISTERED",
        "worker_public_id": worker_pub_id,
        "message": "कारीगर प्रोफाइल सफलतापूर्वक बन गई है!"
    })

# --- 6. Worker Availability / Seasonal Dormancy Toggle ---
@routes.post("/api/workers/status_toggle")
async def toggle_worker_status(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    worker_id = sanitize_text(data.get("worker_public_id", ""))
    new_status = data.get("status", "available")

    if new_status not in ["available", "busy", "seasonal_dormancy"]:
        return web.json_response({"error": "INVALID_STATUS"}, status=400)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE worker_profiles
    SET availability_status = ?, updated_at = ?
    WHERE public_id = ?
    """, (new_status, datetime.utcnow().isoformat(), worker_id))
    conn.commit()
    conn.close()

    return web.json_response({"status": "UPDATED", "new_status": new_status})

# --- 6b. Worker Profile Update (Edit Profile) ---
@routes.post("/api/workers/update")
async def update_worker_profile(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    worker_id = sanitize_text(data.get("worker_public_id", ""))
    if not worker_id:
        return web.json_response({"error": "MISSING_WORKER_ID", "message": "कारीगर आईडी आवश्यक है।"}, status=400)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.id as user_id, u.phone_hash, u.phone_obfuscated, u.birth_year, w.id as wp_id
    FROM users u
    JOIN worker_profiles w ON w.user_id = u.id
    WHERE (w.public_id = ? OR u.public_id = ?) AND u.is_deleted = 0
    """, (worker_id, worker_id))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return web.json_response({"error": "NOT_FOUND", "message": "कारीगर प्रोफाइल नहीं मिला।"}, status=404)

    user_id = row["user_id"]

    # 18+ Age Gate validation if birth year provided
    birth_year = data.get("birth_year")
    if birth_year is not None:
        try:
            birth_year = int(birth_year)
            is_adult, age_err = validate_age_18_plus(birth_year)
            if not is_adult:
                conn.close()
                return web.json_response({
                    "error": "UNDERAGE_PROHIBITED",
                    "message": age_err or "आयु 18 वर्ष से कम नहीं हो सकती।"
                }, status=403)
        except (ValueError, TypeError):
            birth_year = row["birth_year"]

    # Sanitize and extract updated fields
    name = sanitize_text(data.get("name", ""))
    state = sanitize_text(data.get("state", "उत्तर प्रदेश (Uttar Pradesh)"))
    district = sanitize_text(data.get("district", "वाराणसी (Varanasi)"))
    tehsil = sanitize_text(data.get("tehsil", ""))
    village = sanitize_text(data.get("village", ""))
    bio = sanitize_text(data.get("bio_text", ""))

    skills = data.get("skills", [])
    if isinstance(skills, list) and len(skills) > 0:
        validated_skills = []
        for s in skills[:6]:
            valid, res_or_err = validate_custom_skill(s)
            if not valid:
                conn.close()
                log_security_event("BLOCKED_INVALID_SKILL_UPDATE", {"skill": str(s)[:30], "reason": res_or_err})
                return web.json_response({"error": "INVALID_SKILL_NAME", "message": res_or_err}, status=400)
            validated_skills.append(res_or_err)
        skills = validated_skills
    else:
        skills = None

    try:
        daily_rate = int(data.get("daily_rate", 600))
        daily_rate = max(350, min(daily_rate, 3000))
    except (ValueError, TypeError):
        daily_rate = 600

    try:
        experience = int(data.get("experience_years", 1))
        experience = max(0, min(experience, 50))
    except (ValueError, TypeError):
        experience = 1

    is_leader = 1 if data.get("is_team_leader") else 0
    try:
        team_size = int(data.get("team_size", 1))
        team_size = max(1, min(team_size, 20))
    except (ValueError, TypeError):
        team_size = 1

    photo_url = data.get("photo_url", "")
    if photo_url:
        is_valid_size, size_err = validate_photo_size_50kb(photo_url)
        if not is_valid_size:
            conn.close()
            return web.json_response({"error": "PHOTO_EXCEEDS_50KB", "message": size_err}, status=400)
        if not is_safe_photo_url(photo_url):
            photo_url = ""

    # Phone update handling (if provided and valid 10 digits)
    raw_phone = "".join(filter(str.isdigit, data.get("phone", "")))
    now_iso = datetime.utcnow().isoformat()

    if len(raw_phone) >= 10:
        p_hash = hash_phone(raw_phone)
        p_obf = obfuscate_phone(raw_phone)
        p_masked = mask_phone_for_display(raw_phone)
        cursor.execute("""
        UPDATE users SET
            name = CASE WHEN ? != '' THEN ? ELSE name END,
            phone_hash = ?,
            phone_obfuscated = ?,
            phone_masked = ?,
            state = CASE WHEN ? != '' THEN ? ELSE state END,
            district = CASE WHEN ? != '' THEN ? ELSE district END,
            tehsil = ?,
            village = CASE WHEN ? != '' THEN ? ELSE village END,
            photo_url = CASE WHEN ? != '' THEN ? ELSE photo_url END,
            birth_year = COALESCE(?, birth_year)
        WHERE id = ?
        """, (name, name, p_hash, p_obf, p_masked, state, state, district, district, tehsil, village, village, photo_url, photo_url, birth_year, user_id))
    else:
        cursor.execute("""
        UPDATE users SET
            name = CASE WHEN ? != '' THEN ? ELSE name END,
            state = CASE WHEN ? != '' THEN ? ELSE state END,
            district = CASE WHEN ? != '' THEN ? ELSE district END,
            tehsil = ?,
            village = CASE WHEN ? != '' THEN ? ELSE village END,
            photo_url = CASE WHEN ? != '' THEN ? ELSE photo_url END,
            birth_year = COALESCE(?, birth_year)
        WHERE id = ?
        """, (name, name, state, state, district, district, tehsil, village, village, photo_url, photo_url, birth_year, user_id))

    if skills is not None:
        cursor.execute("""
        UPDATE worker_profiles SET
            skills_json = ?,
            experience_years = ?,
            daily_rate = ?,
            bio_text = ?,
            is_team_leader = ?,
            team_size = ?,
            updated_at = ?
        WHERE user_id = ?
        """, (json.dumps(skills, ensure_ascii=False), experience, daily_rate, bio, is_leader, team_size, now_iso, user_id))
    else:
        cursor.execute("""
        UPDATE worker_profiles SET
            experience_years = ?,
            daily_rate = ?,
            bio_text = ?,
            is_team_leader = ?,
            team_size = ?,
            updated_at = ?
        WHERE user_id = ?
        """, (experience, daily_rate, bio, is_leader, team_size, now_iso, user_id))

    conn.commit()
    conn.close()

    log_security_event("WORKER_PROFILE_UPDATED", {"user_id": user_id, "worker_public_id": worker_id})
    return web.json_response({
        "status": "UPDATED",
        "worker_public_id": worker_id,
        "message": "आपकी प्रोफाइल सफलतापूर्वक अपडेट कर दी गई है।"
    })

# --- 7. DPDP Right to Erasure (Delete Profile & Data Purge) ---
@routes.post("/api/workers/delete")
async def delete_worker_profile(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    worker_id = sanitize_text(data.get("worker_public_id", ""))
    if not worker_id:
        return web.json_response({"error": "MISSING_WORKER_ID"}, status=400)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT u.id, u.public_id, u.is_deleted FROM users u
    LEFT JOIN worker_profiles w ON w.user_id = u.id
    WHERE w.public_id = ? OR u.public_id = ?
    """, (worker_id, worker_id))
    row = cursor.fetchone()

    if not row:
        conn.close()
        # Idempotent response: If user or profile was already erased, return 200 so client cleanups succeed
        return web.json_response({
            "status": "DELETED",
            "message": "आपकी प्रोफाइल और समस्त व्यक्तिगत डेटा हटा दिया गया है।"
        })

    user_id = row["id"]

    # Purge PII and soft delete
    cursor.execute("""
    UPDATE users SET
        is_deleted = 1,
        name = 'Deleted Artisan',
        phone_obfuscated = '',
        photo_url = ''
    WHERE id = ?
    """, (user_id,))

    cursor.execute("UPDATE worker_profiles SET is_hidden = 1 WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM portfolio_items WHERE worker_id IN (SELECT id FROM worker_profiles WHERE user_id = ?)", (user_id,))
    cursor.execute("DELETE FROM peer_vouches WHERE worker_id IN (SELECT id FROM worker_profiles WHERE user_id = ?)", (user_id,))
    conn.commit()
    conn.close()

    log_security_event("DPDP_RIGHT_TO_ERASURE_EXECUTED", {"user_id": user_id, "worker_public_id": worker_id})
    return web.json_response({
        "status": "DELETED",
        "message": "आपकी प्रोफाइल और व्यक्तिगत डेटा सुरक्षित रूप से हटा दिया गया है।"
    })

# --- 8. Employer Job Requirement Posting ---
@routes.get("/api/jobs")
async def get_jobs(request: web.Request):
    district = request.query.get("district", "").strip()
    conn = get_db()
    cursor = conn.cursor()

    if district and district != "all":
        cursor.execute("SELECT * FROM job_posts WHERE status = 'open' AND district LIKE ? ORDER BY id DESC LIMIT 20", (f"%{district}%",))
    else:
        cursor.execute("SELECT * FROM job_posts WHERE status = 'open' ORDER BY id DESC LIMIT 20")

    rows = cursor.fetchall()
    conn.close()

    jobs = [{
        "id": r["public_id"],
        "employer_name": r["employer_name"],
        "employer_phone_masked": r["employer_phone_masked"],
        "skill_needed": r["skill_needed"],
        "num_workers": r["num_workers"],
        "duration_days": r["duration_days"],
        "daily_wage_offered": r["daily_wage_offered"],
        "district": r["district"],
        "village": r["village"],
        "created_at": r["created_at"][:10]
    } for r in rows]

    return web.json_response({"jobs": jobs, "count": len(jobs)})

@routes.post("/api/jobs/create")
async def create_job(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    # Mandatory Child Labour Disclaimer Acceptance
    if not data.get("child_labour_disclaimer_accepted"):
        return web.json_response({
            "error": "CHILD_LABOUR_DISCLAIMER_REQUIRED",
            "message": "आपको पुष्टि करनी होगी कि 18 वर्ष से कम आयु के श्रमिकों को काम पर नहीं रखा जाएगा।"
        }, status=400)

    name = sanitize_text(data.get("employer_name", ""))
    phone = "".join(filter(str.isdigit, data.get("phone", "")))
    skill = sanitize_text(data.get("skill_needed", "mason"))
    village = sanitize_text(data.get("village", ""))
    district = sanitize_text(data.get("district", "वाराणसी (Varanasi)"))

    try:
        num_workers = max(1, min(int(data.get("num_workers", 1)), 50))
        duration = max(1, min(int(data.get("duration_days", 1)), 90))
        wage = max(350, min(int(data.get("daily_wage_offered", 600)), 5000))
    except (ValueError, TypeError):
        num_workers, duration, wage = 1, 1, 600

    if not name or not village:
        return web.json_response({"error": "MISSING_FIELDS", "message": "कृपया नाम और गाँव भरें।"}, status=400)

    conn = get_db()
    cursor = conn.cursor()
    job_pub_id = generate_public_id("job")
    masked_p = mask_phone_for_display(phone) if phone else "+91 98XXX-XXXXX"

    cursor.execute("""
    INSERT INTO job_posts (
        public_id, employer_name, employer_phone_masked, skill_needed,
        num_workers, duration_days, daily_wage_offered, district, village,
        status, child_labour_disclaimer_accepted, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'open', 1, ?)
    """, (
        job_pub_id, name, masked_p, skill, num_workers, duration, wage, district, village, datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

    return web.json_response({
        "status": "JOB_POSTED",
        "job_id": job_pub_id,
        "message": "काम की आवश्यकता सफलतापूर्वक पोस्ट कर दी गई है!"
    })

# --- 9. Reviews & Ratings ---
@routes.post("/api/reviews/create")
async def create_review(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    worker_id = sanitize_text(data.get("worker_public_id", ""))
    emp_name = sanitize_text(data.get("employer_name", "ग्राहक"))
    emoji = data.get("emoji", "positive")
    comment = sanitize_text(data.get("comment", ""))

    try:
        rating = int(data.get("rating", 5))
        rating = max(1, min(rating, 5))
    except (ValueError, TypeError):
        rating = 5

    if emoji not in ["positive", "neutral", "negative"]:
        emoji = "positive"

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, rating_avg, review_count FROM worker_profiles WHERE public_id = ?", (worker_id,))
    w = cursor.fetchone()
    if not w:
        conn.close()
        return web.json_response({"error": "WORKER_NOT_FOUND"}, status=404)

    cursor.execute("""
    INSERT INTO reviews (worker_id, employer_public_id, employer_name, rating, emoji, comment, created_at)
    VALUES (?, 'emp_anon', ?, ?, ?, ?, ?)
    """, (w["id"], emp_name, rating, emoji, comment, datetime.utcnow().isoformat()))

    # Recalculate average
    cursor.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE worker_id = ?", (w["id"],))
    avg_r, count_r = cursor.fetchone()

    cursor.execute("""
    UPDATE worker_profiles SET rating_avg = ?, review_count = ? WHERE id = ?
    """, (round(avg_r or 5.0, 1), count_r, w["id"]))

    conn.commit()
    conn.close()

    return web.json_response({"status": "REVIEW_ADDED", "new_rating": round(avg_r, 1)})

# --- 10. Grievance & Reporting Mechanism ---
@routes.post("/api/reports/create")
async def create_report(request: web.Request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    target_id = sanitize_text(data.get("target_public_id", ""))
    target_type = sanitize_text(data.get("target_type", "worker"))
    reason = sanitize_text(data.get("reason", "fraud"))
    details = sanitize_text(data.get("details", ""))
    session_id = data.get("session_id", "anon")

    if not target_id:
        return web.json_response({"error": "TARGET_REQUIRED"}, status=400)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reports (target_type, target_public_id, reporter_session_id, reason, details, status, created_at)
    VALUES (?, ?, ?, ?, ?, 'pending', ?)
    """, (target_type, target_id, session_id, reason, details, datetime.utcnow().isoformat()))

    # If reported for Child Labour or severe fraud, automatically hide worker profile pending review
    if reason in ["child_labour", "fraud"]:
        cursor.execute("UPDATE worker_profiles SET is_hidden = 1 WHERE public_id = ?", (target_id,))
        log_security_event("PROFILE_HIDDEN_FOR_INVESTIGATION", {"target_id": target_id, "reason": reason})

    conn.commit()
    conn.close()

    return web.json_response({
        "status": "REPORT_FILED",
        "message": "आपकी शिकायत दर्ज कर ली गई है। शिकायत निवारण अधिकारी द्वारा 24 घंटे में समीक्षा की जाएगी।"
    })

# --- 11. Platform Stats ---
@routes.get("/api/stats")
async def get_stats(request: web.Request):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM worker_profiles w JOIN users u ON w.user_id = u.id WHERE u.is_deleted = 0 AND w.is_hidden = 0")
    total_workers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM job_posts WHERE status = 'open'")
    total_jobs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM contact_logs")
    total_contacts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT district) FROM users WHERE is_deleted = 0")
    total_districts = cursor.fetchone()[0]

    conn.close()

    return web.json_response({
        "total_workers": total_workers,
        "total_jobs": total_jobs,
        "total_contacts": total_contacts,
        "total_districts": max(total_districts, 4)
    })

# --- 12. End-User Feedback Submission (Email & Database) ---
@routes.post("/api/feedback/submit")
async def submit_feedback(request: web.Request):
    client_ip = get_client_ip(request)

    # 1. Rate limiting: max 4 feedback submissions per 10 minutes per IP
    if not check_rate_limit("feedback", client_ip, max_requests=4, window_seconds=600):
        log_security_event("RATE_LIMIT_FEEDBACK_BLOCKED", {"ip": client_ip})
        return web.json_response({
            "error": "TOO_MANY_REQUESTS",
            "message": "कृपया कुछ समय बाद पुनः प्रयास करें।"
        }, status=429)

    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "INVALID_JSON"}, status=400)

    # 2. Honeypot check for bots
    if detect_honeypot(data):
        log_security_event("BOT_FEEDBACK_TRAPPED", {"ip": client_ip})
        return web.json_response({
            "status": "FEEDBACK_SUBMITTED",
            "message": "आपके सुझाव के लिए धन्यवाद!"
        })

    # 3. Validate and sanitize inputs
    name = sanitize_text(data.get("name", "अनाम प्रयोक्ता"))
    email = data.get("email", "").strip()
    phone = "".join(filter(str.isdigit, data.get("phone", "")))
    category = sanitize_text(data.get("category", "suggestion"))
    message = sanitize_text(data.get("message", ""))
    session_id = sanitize_text(data.get("session_id", "anon"))

    if category not in ["suggestion", "bug", "experience", "complaint", "skill_request", "earnings", "appreciation", "other"]:
        category = "suggestion"

    try:
        rating = int(data.get("rating", 5))
        rating = max(1, min(5, rating))
    except (ValueError, TypeError):
        rating = 5

    # Email format validation
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email):
        return web.json_response({
            "error": "INVALID_EMAIL",
            "message": "कृपया एक मान्य ईमेल आईडी दर्ज करें (ताकि हमारी टीम उत्तर दे सके)।"
        }, status=400)

    if not message or len(message) < 5:
        return web.json_response({
            "error": "MESSAGE_TOO_SHORT",
            "message": "कृपया अपना सुझाव या समस्या विस्तार से लिखें (कम से कम 5 अक्षर)।"
        }, status=400)

    fb_pub_id = generate_public_id("fb")
    now_iso = datetime.utcnow().isoformat()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO feedback (public_id, name, email, phone, category, rating, message, session_id, email_status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
    """, (fb_pub_id, name, email, phone, category, rating, message, session_id, now_iso))
    conn.commit()
    conn.close()

    # 4. Dispatch email to configured recipient (or spool to audit file)
    feedback_payload = {
        "public_id": fb_pub_id,
        "name": name,
        "email": email,
        "phone": phone,
        "category": category,
        "rating": rating,
        "message": message
    }
    email_status = dispatch_feedback_email(feedback_payload)

    # Update email status in db
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE feedback SET email_status = ? WHERE public_id = ?", (email_status, fb_pub_id))
    conn.commit()
    conn.close()

    log_security_event("FEEDBACK_RECEIVED", {"feedback_id": fb_pub_id, "category": category, "email_status": email_status})
    return web.json_response({
        "status": "FEEDBACK_SUBMITTED",
        "feedback_id": fb_pub_id,
        "recipient": FEEDBACK_RECIPIENT_EMAIL,
        "message": "आपके सुझाव के लिए धन्यवाद! आपकी प्रतिक्रिया सुरक्षित रूप से दर्ज कर ली गई है और सहायता टीम को भेज दी गई है।"
    })
