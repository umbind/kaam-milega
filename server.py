"""
server.py — Production-Grade Async Server for "काम मिलेगा" (Kaam Milega)
Runs on Python 3.10 + aiohttp with zero cloud dependencies.
Applies Security Middleware, Hardened Headers, and Static Routing.
"""

import os
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from aiohttp import web
from database import init_db
from security import security_middleware
from api import routes as api_routes

# Ensure app package is importable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

async def handle_home(request: web.Request):
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return web.Response(
            text=f.read(),
            content_type="text/html",
            charset="utf-8",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
        )

async def handle_privacy(request: web.Request):
    p_path = os.path.join(TEMPLATES_DIR, "privacy_policy.html")
    with open(p_path, "r", encoding="utf-8") as f:
        return web.Response(text=f.read(), content_type="text/html", charset="utf-8")

async def handle_terms(request: web.Request):
    t_path = os.path.join(TEMPLATES_DIR, "terms.html")
    with open(t_path, "r", encoding="utf-8") as f:
        return web.Response(text=f.read(), content_type="text/html", charset="utf-8")

async def handle_disclaimer(request: web.Request):
    d_path = os.path.join(TEMPLATES_DIR, "disclaimer.html")
    with open(d_path, "r", encoding="utf-8") as f:
        return web.Response(text=f.read(), content_type="text/html", charset="utf-8")

async def handle_robots(request: web.Request):
    r_path = os.path.join(STATIC_DIR, "robots.txt")
    with open(r_path, "r", encoding="utf-8") as f:
        return web.Response(text=f.read(), content_type="text/plain", charset="utf-8")

async def handle_sw(request: web.Request):
    sw_path = os.path.join(STATIC_DIR, "sw.js")
    with open(sw_path, "r", encoding="utf-8") as f:
        return web.Response(
            text=f.read(),
            content_type="application/javascript",
            charset="utf-8",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
        )

def create_app():
    # 1. Initialize SQLite Database & Seed Data
    init_db()

    # 2. Configure aiohttp application with security middleware & 5MB max payload (DoS Shield)
    app = web.Application(middlewares=[security_middleware], client_max_size=5 * 1024 * 1024)

    # 3. HTML & Service Worker Routes
    app.router.add_get("/", handle_home)
    app.router.add_get("/privacy", handle_privacy)
    app.router.add_get("/terms", handle_terms)
    app.router.add_get("/disclaimer", handle_disclaimer)
    app.router.add_get("/disclaimers", handle_disclaimer)
    app.router.add_get("/robots.txt", handle_robots)
    app.router.add_get("/sw.js", handle_sw)

    # 4. Attach API Routes
    app.add_routes(api_routes)

    # 5. Static Files Route
    app.router.add_static("/static/", path=STATIC_DIR, name="static")

    return app

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))
    app = create_app()
    print(f"===========================================================")
    print(f"  Kaam Milega Server Running on:")
    print(f"  http://{host}:{port}")
    print(f"  Press Ctrl+C to terminate.")
    print(f"===========================================================")
    web.run_app(app, host=host, port=port)
