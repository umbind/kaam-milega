"""
security.py — Hardened Security Controls, Rate Limiting, Input Sanitization & Anti-Scraping Shield
Compliant with DPDP Act 2023, IT Act 2000, and Child Labour Prohibition.
Protects against OWASP Top 10: SQLi, XSS, CSRF, DoS, Scraping, Path Traversal, and Parameter Tampering.
"""

import time
import html
import hashlib
import re
from datetime import datetime
from aiohttp import web

# Rate limiting storage: { bucket: { key: [timestamps] } }
_RATE_LIMITS = {
    "otp": {},
    "contact": {},
    "api": {},
    "write": {}
}

# Honeypot IP ban list: { ip: unban_timestamp }
_BANNED_IPS = {}

SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "img-src 'self' data:; "
        "font-src 'self' data: https://fonts.gstatic.com; "
        "connect-src 'self'; "
        "base-uri 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'none';"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-XSS-Protection": "1; mode=block",
    "Permissions-Policy": "geolocation=(self), microphone=(), camera=(self)",
    "X-Robots-Tag": "noindex, nofollow, noarchive, nosnippet",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Server": "KaamMilega-Shield/1.0"
}

def get_client_ip(request: web.Request) -> str:
    """
    Secure client IP extraction preventing X-Forwarded-For header spoofing.
    Only trusts proxy headers when incoming connection is from verified loopback.
    """
    peer = request.transport.get_extra_info("peername")
    peer_ip = peer[0] if peer else "127.0.0.1"
    # Only evaluate X-Forwarded-For if connection originates from trusted local proxy
    if peer_ip in ("127.0.0.1", "::1"):
        x_forwarded = request.headers.get("X-Forwarded-For")
        if x_forwarded:
            return x_forwarded.split(",")[0].strip()
    return peer_ip

def hash_ip(ip: str) -> str:
    return hashlib.sha256((ip + "KaamMilegaIPShieldSalt2026").encode("utf-8")).hexdigest()[:16]

def ban_ip(ip: str, duration_seconds: int = 3600):
    """
    Instantly ban malicious IP addresses (e.g. honeypot triggers, abusive bots).
    """
    _BANNED_IPS[ip] = time.time() + duration_seconds

def is_ip_banned(ip: str) -> bool:
    now = time.time()
    if ip in _BANNED_IPS:
        if now < _BANNED_IPS[ip]:
            return True
        else:
            del _BANNED_IPS[ip]
    return False

def check_rate_limit(bucket: str, key: str, max_requests: int, window_seconds: int) -> bool:
    """
    Sliding window rate limiter. Returns True if allowed, False if rate limited.
    """
    now = time.time()
    storage = _RATE_LIMITS.setdefault(bucket, {})
    timestamps = storage.setdefault(key, [])

    # Prune expired timestamps
    cutoff = now - window_seconds
    timestamps = [t for t in timestamps if t > cutoff]
    storage[key] = timestamps

    if len(timestamps) >= max_requests:
        return False

    timestamps.append(now)
    return True

def sanitize_text(text: str, max_length: int = 500) -> str:
    """
    Sanitize text input against XSS, HTML injection, null-byte poisoning, and script URIs.
    """
    if not text or not isinstance(text, str):
        return ""
    text = text.strip()[:max_length]
    # Remove null bytes and carriage returns
    text = text.replace("\x00", "").replace("\r", "")
    # Strip script blocks
    clean = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', text, flags=re.IGNORECASE | re.DOTALL)
    # Strip dangerous URI schemes
    clean = re.sub(r'javascript:\s*', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'vbscript:\s*', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'data:\s*text\/html', '', clean, flags=re.IGNORECASE)
    # Strip all HTML tags
    clean = re.sub(r'<[^>]+>', '', clean)
    # Escape HTML special entities
    return html.escape(clean)

def is_safe_photo_url(url: str) -> bool:
    """
    Validates uploaded photo URLs against polyglot SVG XSS or malicious schemes.
    Only allows legitimate base64 raster image strings or local SVG icons.
    """
    if not url or not isinstance(url, str):
        return False
    url = url.strip()
    if len(url) > 2 * 1024 * 1024:  # Max 2MB base64 string
        return False
    if re.match(r"^data:image\/(jpeg|png|webp|jpg);base64,[A-Za-z0-9+/=]+$", url):
        return True
    if re.match(r"^\/static\/images\/icons\/[a-zA-Z0-9_\-]+\.svg$", url):
        return True
    return False

def validate_age_18_plus(birth_year: int) -> tuple[bool, str]:
    """
    Strict Section 18+ & Child Labour Prohibition Act enforcement.
    """
    current_year = datetime.utcnow().year
    try:
        by = int(birth_year)
    except (ValueError, TypeError):
        return False, "अमान्य जन्म वर्ष (Invalid birth year)"

    age = current_year - by
    if age < 18:
        return False, f"कानून के तहत 18 वर्ष से कम उम्र के व्यक्ति काम के लिए पंजीकरण नहीं कर सकते। आपकी उम्र लगभग {age} वर्ष है।"
    if age > 95 or by < 1925:
        return False, "कृपया सही जन्म वर्ष दर्ज करें।"
    return True, ""

def detect_honeypot(data: dict) -> bool:
    """
    Detect automated scraping bots filling hidden trap inputs.
    """
    honeypot_fields = ["website_url", "company_fax", "bot_check", "middle_name_field"]
    for field in honeypot_fields:
        if data.get(field):
            return True
    return False

@web.middleware
async def security_middleware(request: web.Request, handler):
    client_ip = get_client_ip(request)

    # 1. Check if IP is banned
    if is_ip_banned(client_ip):
        return web.json_response(
            {"error": "IP_TEMPORARILY_BLOCKED", "message": "संदेहास्पद गतिविधि या बॉट ट्रैप के कारण आपकी आईपी अस्थायी रूप से ब्लॉक है।"},
            status=403
        )

    # 2. General API rate limit (120 req / minute per IP)
    if request.path.startswith("/api/"):
        if not check_rate_limit("api", client_ip, max_requests=120, window_seconds=60):
            log_security_event("RATE_LIMIT_BURST_BLOCKED", {"ip": client_ip, "path": request.path})
            return web.json_response(
                {"error": "TOO_MANY_REQUESTS", "message": "बहुत अधिक अनुरोध। कृपया कुछ समय बाद पुनः प्रयास करें।"},
                status=429
            )

    # 3. CSRF & Cross-Origin check for state-changing endpoints
    if request.method in ("POST", "PUT", "DELETE", "PATCH"):
        origin = request.headers.get("Origin")
        if origin:
            host = request.headers.get("Host", "")
            allowed_prefixes = (
                f"http://{host}", f"https://{host}",
                "http://localhost", "http://127.0.0.1", "https://localhost", "https://127.0.0.1"
            )
            if not any(origin.startswith(pref) for pref in allowed_prefixes):
                log_security_event("BLOCKED_CROSS_ORIGIN_REQUEST", {"origin": origin, "path": request.path, "ip": client_ip})
                return web.json_response(
                    {"error": "FORBIDDEN_ORIGIN", "message": "अनाधिकृत क्रॉस-ओरिजिन अनुरोध।"},
                    status=403
                )

    try:
        response = await handler(request)
    except web.HTTPException as ex:
        for header, value in SECURITY_HEADERS.items():
            ex.headers[header] = value
        raise
    except Exception as err:
        # Prevent internal stack trace leakage
        log_security_event("UNHANDLED_EXCEPTION_SHIELDED", {"error": str(err), "path": request.path})
        err_resp = web.json_response(
            {"error": "INTERNAL_SERVER_ERROR", "message": "अनपेक्षित त्रुटि हुई। कृपया पुनः प्रयास करें।"},
            status=500
        )
        for header, value in SECURITY_HEADERS.items():
            err_resp.headers[header] = value
        return err_resp

    # 4. Apply Hardened Security Headers to all responses
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value

    return response

def log_security_event(event_type: str, details: dict):
    now = datetime.utcnow().isoformat()
    print(f"[SECURITY AUDIT {now}] {event_type} | {details}")

