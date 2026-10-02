import os

icons = {
    "plumber.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#0369a1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="32" cy="32" r="28" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <path d="M22 36l18-18c1.5-1.5 4-1.5 5.5 0l2.5 2.5c1.5 1.5 1.5 4 0 5.5L30 44l-8-8z" fill="#38bdf8"/>
  <path d="M46 16l4-4a3 3 0 0 1 4 4l-4 4" stroke="#0284c7" stroke-width="3"/>
  <path d="M16 48l6-6-4-4-6 6a3 3 0 0 0 4 4z" fill="#0284c7"/>
  <path d="M38 46c0 4-4 8-8 8s-8-4-8-8c0-3 8-10 8-10s8 7 8 10z" fill="#0284c7"/>
</svg>''',

    "electrician.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#b45309" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="32" cy="32" r="28" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <polygon points="34,8 14,34 30,34 26,56 50,26 34,26" fill="#fbbf24" stroke="#d97706" stroke-width="3"/>
</svg>''',

    "boring.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#0f766e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="32" cy="32" r="28" fill="#ccfbf1" stroke="#14b8a6" stroke-width="2"/>
  <rect x="26" y="16" width="12" height="28" rx="2" fill="#2dd4bf" stroke="#0f766e" stroke-width="2"/>
  <line x1="20" y1="20" x2="44" y2="20" stroke-width="3"/>
  <path d="M38 20l14 8v6l-14-4" fill="#14b8a6"/>
  <path d="M32 44v12M24 56h16" stroke-width="3"/>
  <path d="M22 32c-4 0-6 3-6 6h10" stroke-width="2"/>
  <circle cx="16" cy="46" r="3" fill="#0d9488"/>
</svg>''',

    "carpenter.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#854d0e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="32" cy="32" r="28" fill="#fef9c3" stroke="#eab308" stroke-width="2"/>
  <path d="M14 44l24-24 8 4-24 24-8-4z" fill="#facc15" stroke="#a16207" stroke-width="2"/>
  <path d="M38 20l4-4a4 4 0 0 1 6 6l-4 4" stroke-width="3"/>
  <path d="M12 42l4-2 2 2-2 4-4-4z" fill="#713f12"/>
  <line x1="24" y1="38" x2="30" y2="32" stroke="#713f12" stroke-width="2"/>
  <line x1="30" y1="44" x2="36" y2="38" stroke="#713f12" stroke-width="2"/>
</svg>''',

    "painter.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#4338ca" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="32" cy="32" r="28" fill="#e0e7ff" stroke="#6366f1" stroke-width="2"/>
  <rect x="18" y="14" width="28" height="18" rx="4" fill="#818cf8" stroke="#4338ca" stroke-width="2.5"/>
  <path d="M32 32v12c0 2-2 4-4 4h-4" stroke-width="3"/>
  <path d="M24 48v8" stroke="#312e81" stroke-width="5" stroke-linecap="round"/>
  <circle cx="40" cy="40" r="3" fill="#4f46e5"/>
  <circle cx="46" cy="48" r="2" fill="#4f46e5"/>
</svg>''',

    "welder.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#be123c" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="32" cy="32" r="28" fill="#ffe4e6" stroke="#f43f5e" stroke-width="2"/>
  <rect x="18" y="16" width="28" height="32" rx="14" fill="#fb7185" stroke="#9f1239" stroke-width="2.5"/>
  <rect x="24" y="24" width="16" height="8" rx="2" fill="#4c0519"/>
  <path d="M48 38l6 4M50 30l8-1M48 22l6-4" stroke="#f59e0b" stroke-width="3"/>
</svg>''',

    "labor.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#15803d" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="32" cy="32" r="28" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
  <path d="M18 46l20-20M34 22l8-8 6 6-8 8" stroke-width="3"/>
  <path d="M14 50l6-6-4-4-6 6a2 2 0 0 0 4 4z" fill="#15803d"/>
  <path d="M36 40c4-4 10-6 16-2l2 2c4 6 2 12-2 16-6 6-14 4-18 0" fill="#86efac" stroke="#15803d" stroke-width="2"/>
</svg>''',

    "logo.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <rect width="64" height="64" rx="16" fill="#15803d"/>
  <circle cx="32" cy="32" r="26" fill="#166534" stroke="#86efac" stroke-width="2"/>
  <path d="M22 36l18-18c1.5-1.5 4-1.5 5.5 0l2.5 2.5c1.5 1.5 1.5 4 0 5.5L30 44l-8-8z" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
  <rect x="18" y="26" width="28" height="18" rx="3" fill="#ffffff" fill-opacity="0.2" stroke="#ffffff" stroke-width="2"/>
  <path d="M20 48c6-4 18-4 24 0" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
  <circle cx="32" cy="18" r="4" fill="#facc15"/>
</svg>'''
}

target_dir = r"C:\Users\Umesh Kumar\.gemini\antigravity\scratch\kaam-milega\static\images\icons"
os.makedirs(target_dir, exist_ok=True)
for fname, content in icons.items():
    with open(os.path.join(target_dir, fname), "w", encoding="utf-8") as f:
        f.write(content)
print("Icons generated successfully!")
