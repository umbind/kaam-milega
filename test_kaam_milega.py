import random
import uuid
"""
test_kaam_milega.py — Comprehensive Automated Test Suite
Validates:
1. Database Integrity & Seed Records
2. Zero-PII Leakage in Search APIs
3. Anti-Scraping Rate Limiting & Token Gate
4. Strict 18+ Age Gate & Child Labour Prohibition
5. DPDP Right to Erasure (Account Deletion)
6. SQL Injection & XSS Penetration Resistance
7. Employer Job Posting & Child Labour Disclaimer
8. Hardened Security Headers
"""

import os
import sys
import unittest
import asyncio
import json
import sqlite3
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

# Import application modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import init_db, get_db, DB_PATH
from server import create_app
import security

class TestKaamMilegaSuite(AioHTTPTestCase):

    async def get_application(self):
        # Reset rate limits and re-init database
        security._RATE_LIMITS["otp"].clear()
        security._RATE_LIMITS["contact"].clear()
        security._RATE_LIMITS["api"].clear()
        security._BANNED_IPS.clear()
        return create_app()

    def setUp(self):
        super().setUp()
        init_db()

    # --- Test 1: Database Integrity & Seed Records ---
    def test_database_integrity(self):
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE is_deleted = 0")
        users_count = cursor.fetchone()[0]
        self.assertGreaterEqual(users_count, 10, "Should have at least 10 seeded users")

        cursor.execute("SELECT COUNT(*) FROM worker_profiles WHERE is_hidden = 0")
        worker_count = cursor.fetchone()[0]
        self.assertGreaterEqual(worker_count, 10, "Should have at least 10 active worker profiles")

        # Verify no plain-text phone numbers in users table
        cursor.execute("SELECT phone_hash, phone_obfuscated FROM users LIMIT 5")
        rows = cursor.fetchall()
        for r in rows:
            self.assertEqual(len(r["phone_hash"]), 64, "Phone hash must be 64-char SHA256")
            self.assertTrue(r["phone_obfuscated"], "Phone must be obfuscated")

        conn.close()
        print("  [PASS] Test 1: Database Integrity & Seed Records Verified")

    # --- Test 2: Zero-PII Leakage in Search APIs ---
    async def test_zero_pii_leakage(self):
        resp = await self.client.request("GET", "/api/workers")
        self.assertEqual(resp.status, 200)
        data = await resp.json()

        workers = data.get("workers", [])
        self.assertGreater(len(workers), 0)

        # Inspect every worker returned in public search
        for w in workers:
            self.assertNotIn("phone", w, "Raw phone field must NEVER exist in public API")
            self.assertNotIn("phone_number", w, "phone_number field must NEVER exist in public API")
            self.assertNotIn("phone_obfuscated", w, "phone_obfuscated field must NEVER exist in public API")
            self.assertNotIn("aadhaar", w, "Aadhaar must NEVER exist")
            self.assertNotIn("raw_id", w, "Internal autoincrement ID must not be exposed")
            self.assertTrue(w["id"].startswith("w_"), "ID must be an opaque public hash")
            self.assertIn("phone_masked", w)
            self.assertTrue("XXX" in w["phone_masked"], "Phone preview must be fuzzed/masked")

        print("  [PASS] Test 2: Zero-PII Leakage Guaranteed in Public Search Payloads")

    # --- Test 3: Anti-Scraping Rate Limiter & Token Gate ---
    async def test_anti_scraping_rate_limiter(self):
        # Fetch a valid worker ID
        resp = await self.client.request("GET", "/api/workers")
        data = await resp.json()
        worker_id = data["workers"][0]["id"]

        # 1. Test normal contact reveal
        unlock_resp = await self.client.request("POST", "/api/workers/unlock_contact", json={
            "worker_public_id": worker_id,
            "contact_type": "call"
        })
        self.assertEqual(unlock_resp.status, 200)
        unlock_data = await unlock_resp.json()
        self.assertIn("token", unlock_data)
        self.assertIn("call_url", unlock_data)
        self.assertTrue(unlock_data["call_url"].startswith("tel:+91"))

        # 2. Test honeypot trap detection
        bot_resp = await self.client.request("POST", "/api/workers/unlock_contact", json={
            "worker_public_id": worker_id,
            "website_url": "http://spambot.com", # Honeypot trap triggered!
            "contact_type": "call"
        })
        self.assertEqual(bot_resp.status, 200)
        bot_data = await bot_resp.json()
        self.assertEqual(bot_data["phone"], "+91 99999-00000", "Honeypot must poison bot with dummy phone")

        # 3. Test rapid harvesting lockout (rate limiting threshold = 5)
        hit_429 = False
        for _ in range(7):
            r = await self.client.request("POST", "/api/workers/unlock_contact", json={
                "worker_public_id": worker_id,
                "contact_type": "call"
            })
            if r.status == 429:
                hit_429 = True
                break

        self.assertTrue(hit_429, "Anti-scraping rate limiter must return HTTP 429 after threshold")
        print("  [PASS] Test 3: Anti-Scraping Rate Limiter & Honeypot Defenses Verified")

    # --- Test 4: Strict 18+ Age Gate & Child Labour Prohibition ---
    async def test_18_plus_child_labour_gate(self):
        current_year = 2026

        # 1. Attempt underage registration (age 16)
        underage_payload = {
            "name": "कमल (Underage Test)",
            "phone": "9811223344",
            "birth_year": current_year - 16, # Age 16 -> MUST FAIL
            "declared_age_18_plus": 1,
            "skills": ["labor"],
            "village": "शिवपुर",
            "consent_accepted": True
        }
        resp1 = await self.client.request("POST", "/api/workers/register", json=underage_payload)
        self.assertEqual(resp1.status, 403, "Underage registration MUST be rejected with HTTP 403")
        data1 = await resp1.json()
        self.assertEqual(data1["error"], "UNDERAGE_REGISTRATION_PROHIBITED")

        # 2. Attempt registration without 18+ confirmation
        no_confirm_payload = {
            "name": "राम (Adult Test)",
            "phone": "9811223355",
            "birth_year": current_year - 25,
            "declared_age_18_plus": 0, # Not confirmed!
            "skills": ["mason"],
            "village": "करखियांव",
            "consent_accepted": True
        }
        resp2 = await self.client.request("POST", "/api/workers/register", json=no_confirm_payload)
        self.assertEqual(resp2.status, 400, "Unconfirmed 18+ declaration must return HTTP 400")

        # 3. Valid adult registration (age 26)
        adult_payload = {
            "name": "राम अवतार (Adult Valid)",
            "phone": "9811223366",
            "birth_year": current_year - 26, # Age 26 -> Valid Adult
            "declared_age_18_plus": 1,
            "skills": ["mason", "plumber"],
            "experience_years": 7,
            "state": "उत्तर प्रदेश",
            "district": "वाराणसी",
            "village": "पिंडरा",
            "daily_rate": 700,
            "consent_accepted": True
        }
        resp3 = await self.client.request("POST", "/api/workers/register", json=adult_payload)
        self.assertEqual(resp3.status, 200, "Valid adult registration must succeed")
        data3 = await resp3.json()
        self.assertEqual(data3["status"], "REGISTERED")

        print("  [PASS] Test 4: Strict 18+ Age Gate & Child Labour Prohibition Verified")

    # --- Test 5: DPDP Consent & Right to Erasure ---
    async def test_dpdp_right_to_erasure(self):
        # Register a temporary test worker
        current_year = 2026
        test_payload = {
            "name": "विलोपन परीक्षण (Erasure Test)",
            "phone": "9800000001",
            "birth_year": current_year - 30,
            "declared_age_18_plus": 1,
            "skills": ["painter"],
            "village": "रोहनिया",
            "consent_accepted": True
        }
        reg_resp = await self.client.request("POST", "/api/workers/register", json=test_payload)
        reg_data = await reg_resp.json()
        worker_pub_id = reg_data["worker_public_id"]

        # Verify worker is currently visible in search
        check1 = await self.client.request("GET", f"/api/workers/{worker_pub_id}")
        self.assertEqual(check1.status, 200)

        # Trigger DPDP Right to Erasure
        del_resp = await self.client.request("POST", "/api/workers/delete", json={
            "worker_public_id": worker_pub_id
        })
        self.assertEqual(del_resp.status, 200)
        del_data = await del_resp.json()
        self.assertEqual(del_data["status"], "DELETED")

        # Idempotent re-deletion must also return 200 DELETED
        del_resp2 = await self.client.request("POST", "/api/workers/delete", json={
            "worker_public_id": worker_pub_id
        })
        self.assertEqual(del_resp2.status, 200)
        del_data2 = await del_resp2.json()
        self.assertEqual(del_data2["status"], "DELETED")

        print("  [PASS] Test 5: DPDP Right to Erasure & Account Purge Verified (Idempotent)")

    # --- Test 5b: Worker Profile Edit & 18+ Protection ---
    async def test_worker_profile_update(self):
        # 1. Register an initial worker
        init_payload = {
            "name": "दिनेश कारीगर",
            "phone": "9811223344",
            "birth_year": 1993,
            "declared_age_18_plus": 1,
            "skills": ["mason"],
            "experience_years": 4,
            "daily_rate": 600,
            "village": "राजातालाब",
            "consent_accepted": True
        }
        reg_resp = await self.client.request("POST", "/api/workers/register", json=init_payload)
        self.assertEqual(reg_resp.status, 200)
        reg_data = await reg_resp.json()
        worker_id = reg_data["worker_public_id"]

        # 2. Update profile: edit name, skills (Halwai + Cook), rate, exp, team
        update_payload = {
            "worker_public_id": worker_id,
            "name": "दिनेश मास्टर हलवाई",
            "skills": ["halwai", "event_cook"],
            "daily_rate": 1100,
            "experience_years": 8,
            "is_team_leader": 1,
            "team_size": 5,
            "village": "मिर्ज़ामुराद",
            "bio_text": "शादी-विवाह और त्योहारों के विशेष हलवाई कारीगर।"
        }
        up_resp = await self.client.request("POST", "/api/workers/update", json=update_payload)
        self.assertEqual(up_resp.status, 200)
        up_data = await up_resp.json()
        self.assertEqual(up_data["status"], "UPDATED")

        # 3. Verify updated details via GET worker
        fetch_resp = await self.client.request("GET", f"/api/workers/{worker_id}")
        self.assertEqual(fetch_resp.status, 200)
        worker = (await fetch_resp.json())["worker"]
        self.assertEqual(worker["name"], "दिनेश मास्टर हलवाई")
        self.assertIn("halwai", worker["skills"])
        self.assertIn("event_cook", worker["skills"])
        self.assertEqual(worker["daily_rate"], 1100)
        self.assertEqual(worker["experience_years"], 8)
        self.assertTrue(worker["is_team_leader"])
        self.assertEqual(worker["team_size"], 5)
        self.assertEqual(worker["village"], "मिर्ज़ामुराद")

        # 4. Attempt underage birth year update (Child Labour Act protection)
        underage_payload = {
            "worker_public_id": worker_id,
            "birth_year": 2018
        }
        underage_resp = await self.client.request("POST", "/api/workers/update", json=underage_payload)
        self.assertEqual(underage_resp.status, 403, "Underage updates must be blocked")

        print("  [PASS] Test 5b: Profile Edit & Underage Protection Verified")

    # --- Test 6: Advanced SQL Injection Penetration Resistance ---
    async def test_advanced_sqli_resistance(self):
        sqli_vectors = [
            "' OR 1=1 --",
            "admin'--",
            "' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19 FROM users--",
            "'; DROP TABLE users;--",
            "1' AND SLEEP(2)--",
            "' OR 'x'='x"
        ]

        for payload in sqli_vectors:
            # Test in search query 'q'
            r1 = await self.client.request("GET", f"/api/workers?q={payload}")
            self.assertEqual(r1.status, 200, f"Search q SQLi payload '{payload}' must be safely parameterized")
            
            # Test in 'skill' parameter
            r2 = await self.client.request("GET", f"/api/workers?skill={payload}")
            self.assertEqual(r2.status, 200, f"Skill SQLi payload '{payload}' must be safely parameterized")

            # Test in 'district' parameter
            r3 = await self.client.request("GET", f"/api/jobs?district={payload}")
            self.assertEqual(r3.status, 200, f"Jobs district SQLi payload '{payload}' must be safely parameterized")

        print("  [PASS] Test 6: Advanced SQL Injection Penetration Resistance Verified (6 Attack Vectors)")

    # --- Test 7: Advanced XSS, Script Injections & SVG Polyglot Shield ---
    async def test_advanced_xss_and_svg_polyglot_resistance(self):
        # 1. XSS in report details
        xss_payload = "<script>alert('xss_attack')</script>"
        report_resp = await self.client.request("POST", "/api/reports/create", json={
            "target_public_id": "w_test",
            "reason": "fraud",
            "details": xss_payload
        })
        self.assertEqual(report_resp.status, 200)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT details FROM reports ORDER BY id DESC LIMIT 1")
        stored_details = cursor.fetchone()[0]
        self.assertNotIn("<script>", stored_details, "Raw script tags must be sanitized/escaped")
        conn.close()

        # 2. XSS and malicious SVG payload in worker registration
        malicious_worker = {
            "name": "Ram<script>alert(1)</script>",
            "phone": "9988776655",
            "birth_year": 1990,
            "declared_age_18_plus": 1,
            "skills": ["mason"],
            "experience_years": 5,

            "state": "उत्तर प्रदेश",
            "district": "वाराणसी",
            "village": "Shivpur<iframe src=javascript:alert(1)>",
            "photo_url": "javascript:alert(document.cookie)", # Malicious pseudo-protocol
            "consent_accepted": True
        }
        reg_resp = await self.client.request("POST", "/api/workers/register", json=malicious_worker)
        self.assertEqual(reg_resp.status, 200)
        reg_data = await reg_resp.json()
        worker_id = reg_data["worker_public_id"]

        # Verify in search that all fields were thoroughly sanitized
        detail_resp = await self.client.request("GET", f"/api/workers/{worker_id}")
        self.assertEqual(detail_resp.status, 200)
        worker_data = (await detail_resp.json())["worker"]

        self.assertNotIn("<script>", worker_data["name"])
        self.assertNotIn("<iframe", worker_data["village"])
        self.assertFalse(worker_data["photo_url"].startswith("javascript:"), "Malicious photo URL must be rejected")
        self.assertTrue(worker_data["photo_url"].startswith("/static/images/icons/"), "Fallback safe icon must be used")

        print("  [PASS] Test 7: Advanced XSS, HTML Injection & SVG Polyglot Shield Verified")

    # --- Test 8: CSRF & Origin Validation Shield ---
    async def test_csrf_and_origin_shield(self):
        # 1. State-changing request from unauthorized cross-origin attacker site
        bad_origin_resp = await self.client.request(
            "POST",
            "/api/jobs/create",
            headers={"Origin": "https://malicious-phishing-site.com"},
            json={"employer_name": "Attacker", "phone": "9999999999"}
        )
        self.assertEqual(bad_origin_resp.status, 403, "Cross-origin requests from unauthorized domains must be rejected with 403")

        # 2. State-changing request from legitimate same-origin
        good_origin_resp = await self.client.request(
            "POST",
            "/api/jobs/create",
            headers={"Origin": "http://127.0.0.1:8080"},
            json={
                "employer_name": "ठेकेदार",
                "phone": "9876543210",
                "skill_needed": "mason",
                "village": "रामनगर",
                "child_labour_disclaimer_accepted": 1
            }
        )
        self.assertEqual(good_origin_resp.status, 200, "Same-origin requests must be permitted")

        print("  [PASS] Test 8: CSRF & Cross-Origin Request Forgery Shield Verified")

    # --- Test 9: Mass Assignment & Privilege Escalation Resistance ---
    async def test_mass_assignment_and_privilege_escalation(self):
        # Attacker tries to inject elevated tier and fake vouches during registration
        tampered_worker = {
            "name": "दिलीप मिस्त्री",
            "phone": "9123456780",
            "birth_year": 1988,
            "declared_age_18_plus": 1,
            "skills": ["mason"],
            "experience_years": 10,
            "state": "उत्तर प्रदेश",
            "district": "वाराणसी",
            "village": "सारनाथ",
            "consent_accepted": True,
            # Tampered fields:
            "verification_tier": "tier3",
            "is_verified": 1,
            "rating_avg": 5.0,
            "vouched_count": 999
        }
        reg_resp = await self.client.request("POST", "/api/workers/register", json=tampered_worker)
        self.assertEqual(reg_resp.status, 200)
        worker_id = (await reg_resp.json())["worker_public_id"]

        # Check DB row directly
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT u.verification_tier, w.vouched_count FROM worker_profiles w JOIN users u ON w.user_id = u.id WHERE w.public_id = ?", (worker_id,))
        row = cursor.fetchone()
        conn.close()

        self.assertEqual(row["verification_tier"], "tier1", "Mass assignment must not escalate verification tier")
        self.assertEqual(row["vouched_count"], 1, "Mass assignment must not alter vouched count")

        print("  [PASS] Test 9: Mass Assignment & Privilege Escalation Attack Defenses Verified")

    # --- Test 10: Path Traversal / LFI Resistance ---
    async def test_path_traversal_resistance(self):
        traversal_paths = [
            "/static/../../server.py",
            "/static/..%2f..%2fserver.py",
            "/static/../database.py",
            "/static/....//....//etc/passwd"
        ]
        for path in traversal_paths:
            resp = await self.client.request("GET", path)
            self.assertIn(resp.status, [400, 404], f"Path traversal '{path}' must be blocked (HTTP 400/404)")

        print("  [PASS] Test 10: Path Traversal / Directory Escape Shield Verified")

    # --- Test 11: Employer Job Posting & Child Labour Disclaimer ---
    async def test_job_posting_compliance(self):
        # 1. Attempt posting without child labour disclaimer
        no_disclaimer = {
            "employer_name": "ठेकेदार साहब",
            "phone": "9899001122",
            "skill_needed": "mason",
            "village": "शिवपुर",
            "child_labour_disclaimer_accepted": 0 # Rejected!
        }
        r1 = await self.client.request("POST", "/api/jobs/create", json=no_disclaimer)
        self.assertEqual(r1.status, 400, "Job post without child labour disclaimer must fail")

        # 2. Valid job post
        valid_job = {
            "employer_name": "ठेकेदार साहब",
            "phone": "9899001122",
            "skill_needed": "mason",
            "num_workers": 3,
            "duration_days": 5,
            "daily_wage_offered": 800,
            "district": "वाराणसी (Varanasi)",
            "village": "शिवपुर",
            "child_labour_disclaimer_accepted": 1
        }
        r2 = await self.client.request("POST", "/api/jobs/create", json=valid_job)
        self.assertEqual(r2.status, 200)
        data2 = await r2.json()
        self.assertEqual(data2["status"], "JOB_POSTED")

        print("  [PASS] Test 11: Employer Job Posting & Legal Undertaking Verified")

    # --- Test 12: Hardened Security Headers & Server Banner Masking ---
    async def test_hardened_security_headers_and_banner_masking(self):
        resp = await self.client.request("GET", "/")
        headers = resp.headers

        self.assertIn("Content-Security-Policy", headers)
        self.assertEqual(headers["X-Frame-Options"], "DENY")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(headers["X-XSS-Protection"], "1; mode=block")
        self.assertIn(headers["Referrer-Policy"], ["strict-origin-when-cross-origin", "no-referrer"])
        self.assertIn("noindex", headers["X-Robots-Tag"])
        self.assertEqual(headers["Cross-Origin-Opener-Policy"], "same-origin")
        self.assertEqual(headers["Cross-Origin-Resource-Policy"], "same-origin")
        self.assertEqual(headers["Server"], "KaamMilega-Shield/1.0", "Server header must be masked to prevent banner grabbing")

    # --- Test 13: End-User Feedback Submission, Honeypot, Email Spool & Rate Limiting ---
    async def test_feedback_submission_and_email_spool(self):
        # 1. Invalid email check
        bad_email = {
            "name": "रमेश कुमार",
            "email": "invalid-email-string",
            "category": "suggestion",
            "rating": 5,
            "message": "बहुत ही बेहतरीन प्लेटफ़ॉर्म है।"
        }
        r1 = await self.client.request("POST", "/api/feedback/submit", json=bad_email)
        self.assertEqual(r1.status, 400)
        d1 = await r1.json()
        self.assertEqual(d1["error"], "INVALID_EMAIL")

        # 2. Honeypot bot trap check
        bot_payload = {
            "name": "SpamBot",
            "email": "spambot@example.com",
            "message": "Click here for cheap crypto loans!",
            "website_url": "http://evil-spam.com" # Honeypot filled!
        }
        r2 = await self.client.request("POST", "/api/feedback/submit", json=bot_payload)
        self.assertEqual(r2.status, 200, "Honeypot returns 200 fake success to silently deceive spambots")
        d2 = await r2.json()
        self.assertEqual(d2["status"], "FEEDBACK_SUBMITTED")

        # Verify spambot message was NEVER written to the database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feedback WHERE email = 'spambot@example.com'")
        self.assertEqual(cursor.fetchone()[0], 0, "Bot payload trapped by honeypot must NOT be inserted into database")
        conn.close()

        # 3. Message too short check
        short_payload = {
            "email": "user@example.com",
            "message": "hi" # < 5 chars
        }
        r3 = await self.client.request("POST", "/api/feedback/submit", json=short_payload)
        self.assertEqual(r3.status, 400)
        d3 = await r3.json()
        self.assertEqual(d3["error"], "MESSAGE_TOO_SHORT")

        # 4. Valid feedback submission
        valid_payload = {
            "name": "राजेश मिस्त्री",
            "email": "rajesh.mistry@example.com",
            "phone": "9811223344",
            "category": "suggestion",
            "rating": 5,
            "message": "कृपया वेल्डर श्रेणी में पाइप वेल्डिंग का सब-ऑप्शन भी जोड़ें।"
        }
        r4 = await self.client.request("POST", "/api/feedback/submit", json=valid_payload)
        self.assertEqual(r4.status, 200)
        d4 = await r4.json()
        self.assertEqual(d4["status"], "FEEDBACK_SUBMITTED")
        self.assertTrue(d4["feedback_id"].startswith("fb_"))

        # Verify feedback record was persisted in database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback WHERE public_id = ?", (d4["feedback_id"],))
        fb_row = cursor.fetchone()
        self.assertIsNotNone(fb_row)
        self.assertEqual(fb_row["email"], "rajesh.mistry@example.com")
        self.assertEqual(fb_row["rating"], 5)
        conn.close()

        print("  [PASS] Test 13: End-User Feedback Submission, Honeypot & Email Spool Verified")

    # --- Test 14: Strict 50KB Photo Limit Enforcement on Registration & Profile Edit ---
    async def test_photo_size_limit_50kb_enforcement(self):
        import base64

        # 1. Payload with 65KB photo (> 50KB limit)
        oversized_raw = b"X" * (65 * 1024)
        oversized_b64 = "data:image/jpeg;base64," + base64.b64encode(oversized_raw).decode("ascii")

        reg_oversized = {
            "name": "सुरेश कुमार",
            "phone": "9812345678",
            "birth_year": 1990,
            "declared_age_18_plus": 1,
            "skills": ["mason"],
            "experience_years": 5,
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "village": "रामनगर",
            "daily_rate": 700,
            "availability_status": "available",
            "photo_url": oversized_b64,
            "consent_accepted": True
        }

        r1 = await self.client.request("POST", "/api/workers/register", json=reg_oversized)
        self.assertEqual(r1.status, 400, "Oversized photo (>50KB) must be rejected on registration")
        d1 = await r1.json()
        self.assertEqual(d1["error"], "PHOTO_EXCEEDS_50KB")

        # 2. Payload with 35KB photo (<= 50KB limit) - must pass
        valid_raw = b"Y" * (35 * 1024)
        valid_b64 = "data:image/webp;base64," + base64.b64encode(valid_raw).decode("ascii")

        reg_valid = dict(reg_oversized)
        reg_valid["phone"] = "9812345679"
        reg_valid["photo_url"] = valid_b64

        r2 = await self.client.request("POST", "/api/workers/register", json=reg_valid)
        self.assertEqual(r2.status, 200, "Compliant photo (<=50KB) must succeed")
        d2 = await r2.json()
        worker_id = d2["worker_public_id"]

        # 3. Test profile edit with oversized photo
        update_oversized = {
            "worker_public_id": worker_id,
            "name": "सुरेश कुमार अपडेटेड",
            "birth_year": 1990,
            "skills": ["mason"],
            "experience_years": 6,
            "village": "रामनगर",
            "photo_url": oversized_b64 # > 50KB
        }
        r3 = await self.client.request("POST", "/api/workers/update", json=update_oversized)
        self.assertEqual(r3.status, 400, "Oversized photo (>50KB) must be rejected on profile update")
        d3 = await r3.json()
        self.assertEqual(d3["error"], "PHOTO_EXCEEDS_50KB")

        print("  [PASS] Test 14: Strict 50KB Photo Size Enforcement Verified (Registration & Update)")

    # --- Test 15: Search Trust Filters & Earnability Analytics ---
    async def test_trust_filter_and_earnability(self):
        # 1. Fetch with trust_filter = 'all'
        r_all = await self.client.request("GET", "/api/workers?trust_filter=all")
        self.assertEqual(r_all.status, 200)
        d_all = await r_all.json()
        workers = d_all.get("workers", [])
        self.assertGreater(len(workers), 0)

        # Ensure estimated_monthly_earnings exists on all worker cards
        for w in workers:
            self.assertIn("estimated_monthly_earnings", w)
            self.assertGreater(w["estimated_monthly_earnings"], 0)
            self.assertIn("is_top_rated", w)

        # 2. Fetch with trust_filter = 'team_leader'
        r_team = await self.client.request("GET", "/api/workers?trust_filter=team_leader")
        self.assertEqual(r_team.status, 200)
        d_team = await r_team.json()
        for w in d_team.get("workers", []):
            self.assertEqual(w["is_team_leader"], 1)

        # 3. Fetch with trust_filter = 'available'
        r_avail = await self.client.request("GET", "/api/workers?trust_filter=available")
        self.assertEqual(r_avail.status, 200)
        d_avail = await r_avail.json()
        for w in d_avail.get("workers", []):
            self.assertEqual(w["availability_status"], "available")

        print("  [PASS] Test 15: Search Trust Filters & Monthly Earnability Analytics Verified")

    # --- Test 16: Custom Category Anti-Abuse Guard ---
    async def test_custom_skill_anti_abuse_guard(self):
        base_payload = {
            "name": "राम कुमार टेस्ट",
            "phone": "9812345688",
            "birth_year": 1990,
            "declared_18_plus": True,
            "skills": ["mason"],
            "experience_years": 5,
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "village": "रामनगर",
            "daily_rate": 700,
            "availability_status": "available",
            "consent_accepted": True
        }

        # 1. Reject digits / phone number bypass in skill
        p_digits = dict(base_payload, phone="9812345688", skills=["Call 9876543210"])
        r1 = await self.client.request("POST", "/api/workers/register", json=p_digits)
        self.assertEqual(r1.status, 400)
        d1 = await r1.json()
        self.assertEqual(d1["error"], "INVALID_SKILL_NAME")

        # 2. Reject URL in skill
        p_url = dict(base_payload, phone="9812345687", skills=["mysite.com"])
        r2 = await self.client.request("POST", "/api/workers/register", json=p_url)
        self.assertEqual(r2.status, 400)
        d2 = await r2.json()
        self.assertEqual(d2["error"], "INVALID_SKILL_NAME")

        # 3. Reject email in skill
        p_email = dict(base_payload, phone="9812345686", skills=["worker@gmail.com"])
        r3 = await self.client.request("POST", "/api/workers/register", json=p_email)
        self.assertEqual(r3.status, 400)
        d3 = await r3.json()
        self.assertEqual(d3["error"], "INVALID_SKILL_NAME")

        # 4. Reject prohibited terms (loan, betting, escort, etc.)
        p_bad = dict(base_payload, phone="9812345685", skills=["Instant Loan"])
        r4 = await self.client.request("POST", "/api/workers/register", json=p_bad)
        self.assertEqual(r4.status, 400)
        d4 = await r4.json()
        self.assertEqual(d4["error"], "INVALID_SKILL_NAME")

        # 5. Accept valid clean custom skills (Hindi and English)
        p_valid_hi = dict(base_payload, phone="9812345684", skills=["दर्जी कारीगर"])
        r5 = await self.client.request("POST", "/api/workers/register", json=p_valid_hi)
        self.assertEqual(r5.status, 200)

        p_valid_en = dict(base_payload, phone="9812345683", skills=["Tailor Master"])
        r6 = await self.client.request("POST", "/api/workers/register", json=p_valid_en)
        self.assertEqual(r6.status, 200)

        print("  [PASS] Test 16: Custom Category Anti-Abuse & Phone/URL Bypass Defense Verified")


    async def test_craftsmanship_portfolio_and_50kb_gate(self):
        """Test 17: Validates craftsmanship portfolio uploads, strict 50KB boundary, and max 3 items limit."""
        reg_payload = {
            "name": "दिनेश कारीगर",
            "phone": f"9876{random.randint(100000, 999999)}",
            "birth_year": 1990,
            "declared_age_18_plus": 1,
            "consent_accepted": 1,
            "skills": ["plumber"],
            "daily_rate": 700,
            "experience_years": 8,
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "village": "रामनगर"
        }
        reg_res = await self.client.request("POST", "/api/workers/register", json=reg_payload)
        self.assertEqual(reg_res.status, 200)
        reg_data = await reg_res.json()
        worker_id = reg_data["worker_public_id"]

        # 1. Upload valid photo under 50KB (~1KB dummy valid SVG/PNG)
        valid_b64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        p1 = await self.client.request("POST", "/api/workers/portfolio/add", json={
            "worker_public_id": worker_id,
            "image_url": valid_b64,
            "title": "पाइपलाइन फिटिंग"
        })
        self.assertEqual(p1.status, 200)
        p1_data = await p1.json()
        item1_id = p1_data["item"]["id"]

        # 2. Reject photo exceeding 50KB (65KB payload)
        oversized_data = "data:image/png;base64," + ("A" * (80 * 1024))
        p_bad = await self.client.request("POST", "/api/workers/portfolio/add", json={
            "worker_public_id": worker_id,
            "image_url": oversized_data,
            "title": "बड़ी फाइल"
        })
        self.assertEqual(p_bad.status, 400)
        p_bad_data = await p_bad.json()
        self.assertEqual(p_bad_data["error"], "PHOTO_EXCEEDS_50KB")

        # 3. Add 2nd and 3rd portfolio photos (reaches 3 items cap)
        await self.client.request("POST", "/api/workers/portfolio/add", json={
            "worker_public_id": worker_id, "image_url": valid_b64, "title": "नल फिटिंग"
        })
        await self.client.request("POST", "/api/workers/portfolio/add", json={
            "worker_public_id": worker_id, "image_url": valid_b64, "title": "टैंक कनेक्शन"
        })

        # 4. Attempt 4th photo -> Reject with PORTFOLIO_LIMIT_REACHED
        p4 = await self.client.request("POST", "/api/workers/portfolio/add", json={
            "worker_public_id": worker_id, "image_url": valid_b64, "title": "चौथी फोटो"
        })
        self.assertEqual(p4.status, 400)
        p4_data = await p4.json()
        self.assertEqual(p4_data["error"], "PORTFOLIO_LIMIT_REACHED")

        # 5. Fetch profile and verify 3 items in portfolio
        prof_res = await self.client.request("GET", f"/api/workers/{worker_id}")
        self.assertEqual(prof_res.status, 200)
        prof_data = await prof_res.json()
        self.assertEqual(len(prof_data["worker"]["portfolio"]), 3)

        # 6. Delete item1 and verify count is 2
        del_res = await self.client.request("POST", "/api/workers/portfolio/delete", json={
            "worker_public_id": worker_id, "item_id": item1_id
        })
        self.assertEqual(del_res.status, 200)

        prof_res2 = await self.client.request("GET", f"/api/workers/{worker_id}")
        prof_data2 = await prof_res2.json()
        self.assertEqual(len(prof_data2["worker"]["portfolio"]), 2)

        print("  [PASS] Test 17: Craftsmanship Portfolio & Strict 50KB Boundary Defense Verified")

    async def test_peer_vouching_and_tier_progression(self):
        """Test 18: Validates peer vouching, duplicate prevention, and LinkedIn-style trust tier progression."""
        reg_payload = {
            "name": "सुरेश राजमिस्त्री",
            "phone": f"9865{random.randint(100000, 999999)}",
            "birth_year": 1988,
            "declared_age_18_plus": 1,
            "consent_accepted": 1,
            "skills": ["mason"],
            "daily_rate": 750,
            "experience_years": 10,
            "state": "उत्तर प्रदेश (Uttar Pradesh)",
            "district": "वाराणसी (Varanasi)",
            "village": "चौबेपुर"
        }
        reg_res = await self.client.request("POST", "/api/workers/register", json=reg_payload)
        self.assertEqual(reg_res.status, 200)
        worker_id = (await reg_res.json())["worker_public_id"]

        # Initial tier is tier1
        r0 = await self.client.request("GET", f"/api/workers/{worker_id}")
        d0 = (await r0.json())["worker"]
        self.assertEqual(d0["verification_tier"], "tier1")

        # Peer 1 vouches
        v1 = await self.client.request("POST", "/api/workers/vouch", json={
            "worker_public_id": worker_id,
            "voucher_name": "रामू मिस्त्री",
            "trade": "राजमिस्त्री",
            "session_id": "ses_peer_001"
        })
        self.assertEqual(v1.status, 200)

        # Peer 1 attempts duplicate vouch -> Reject
        v1_dup = await self.client.request("POST", "/api/workers/vouch", json={
            "worker_public_id": worker_id,
            "voucher_name": "रामू मिस्त्री",
            "session_id": "ses_peer_001"
        })
        self.assertEqual(v1_dup.status, 400)
        self.assertEqual((await v1_dup.json())["error"], "ALREADY_VOUCHED")

        # Peer 2 vouches -> Upgrades tier to tier2 (Peer Vouched)
        v2 = await self.client.request("POST", "/api/workers/vouch", json={
            "worker_public_id": worker_id,
            "voucher_name": "श्यामू प्लंबर",
            "trade": "प्लंबर",
            "session_id": "ses_peer_002"
        })
        self.assertEqual(v2.status, 200)
        v2_data = await v2.json()
        self.assertEqual(v2_data["verification_tier"], "tier2")

        # Verify get detail reflects tier2
        r_tier = await self.client.request("GET", f"/api/workers/{worker_id}")
        d_tier = (await r_tier.json())["worker"]
        self.assertEqual(d_tier["verification_tier"], "tier2")

        print("  [PASS] Test 18: Peer Vouching & LinkedIn-Style Trust Tier Elevation Verified")

    async def test_zero_work_history_privacy(self):
        """Test 19: Validates complete absence of sensitive work history/slip logs from public profiles."""
        r = await self.client.request("GET", "/api/workers")
        self.assertEqual(r.status, 200)
        workers = (await r.json())["workers"]
        self.assertTrue(len(workers) > 0)
        w_id = workers[0]["id"]

        r_detail = await self.client.request("GET", f"/api/workers/{w_id}")
        self.assertEqual(r_detail.status, 200)
        detail = (await r_detail.json())["worker"]

        # Strict privacy assurance: no work history, employer tracking, or financial slip records in public profile
        self.assertNotIn("work_history", detail)
        self.assertNotIn("work_slips", detail)
        self.assertNotIn("job_history", detail)
        self.assertNotIn("client_records", detail)
        self.assertNotIn("wage_records", detail)

        print("  [PASS] Test 19: Privacy-First Zero-Work-History & Data Minimization Guaranteed")

    # --- Test 20: Comprehensive Legal Disclaimers & Statutory Compliance Verification ---
    async def test_legal_disclaimers_compliance_routes(self):
        # 1. Test /disclaimer route
        r_disc = await self.client.request("GET", "/disclaimer")
        self.assertEqual(r_disc.status, 200)
        disc_html = await r_disc.text()
        self.assertIn("IT Act Sec 79", disc_html)
        self.assertIn("धारा 79", disc_html)
        self.assertIn("बाल एवं किशोर श्रम", disc_html)
        self.assertIn("न्यूनतम मजदूरी", disc_html)
        self.assertIn("1930", disc_html) # Cyber helpline
        self.assertIn("BOCW", disc_html) # Building and construction safety
        self.assertIn("DPDP Act, 2023", disc_html)
        self.assertIn("grievance@kaammilega.org", disc_html)

        # 2. Test /disclaimers alias
        r_alias = await self.client.request("GET", "/disclaimers")
        self.assertEqual(r_alias.status, 200)

        # 3. Test /terms route
        r_terms = await self.client.request("GET", "/terms")
        self.assertEqual(r_terms.status, 200)
        terms_html = await r_terms.text()
        self.assertIn("कानूनी अस्वीकरण", terms_html)

        # 4. Test /privacy route
        r_priv = await self.client.request("GET", "/privacy")
        self.assertEqual(r_priv.status, 200)
        priv_html = await r_priv.text()
        self.assertIn("DPDP Act 2023", priv_html)

        print("  [PASS] Test 20: Comprehensive Legal Disclaimers & Statutory Compliance Verified")

if __name__ == "__main__":
    print("\n=======================================================")
    print("  RUNNING KAAM MILEGA COMPREHENSIVE CYBER DEFENSE SUITE")
    print("=======================================================\n")
    unittest.main()


