import os

driver_icons = {
    "auto_driver.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#047857" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="64" height="64" rx="16" fill="#f0fdf4"/>
  <circle cx="20" cy="48" r="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <circle cx="48" cy="48" r="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <path d="M12 40h42v-8a4 4 0 0 0-4-4H38l-4-14h-8l-8 14H12a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2z" fill="#facc15" stroke="#ca8a04" stroke-width="2.5"/>
  <rect x="28" y="18" width="10" height="8" rx="1" fill="#e2e8f0"/>
  <line x1="10" y1="36" x2="54" y2="36" stroke="#15803d" stroke-width="2.5"/>
  <circle cx="14" cy="38" r="2" fill="#fbbf24"/>
</svg>''',

    "erickshaw_driver.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#0284c7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="64" height="64" rx="16" fill="#f0f9ff"/>
  <circle cx="18" cy="48" r="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <circle cx="46" cy="48" r="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <path d="M14 42h36l2-16a4 4 0 0 0-4-4H28l-4-8h-6l-4 12v14a2 2 0 0 0 2 2z" fill="#38bdf8" stroke="#0284c7" stroke-width="2.5"/>
  <polygon points="34,16 28,26 36,26 30,36" fill="#facc15" stroke="#ca8a04" stroke-width="2"/>
  <line x1="28" y1="18" x2="48" y2="18" stroke="#0369a1" stroke-width="2.5"/>
</svg>''',

    "pickup_driver.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#b45309" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="64" height="64" rx="16" fill="#fffbeb"/>
  <circle cx="20" cy="48" r="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <circle cx="48" cy="48" r="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <rect x="28" y="24" width="24" height="18" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="2"/>
  <path d="M12 42h16V22h-6l-6 10v10z" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
  <rect x="16" y="26" width="6" height="6" rx="1" fill="#e2e8f0"/>
  <line x1="30" y1="28" x2="50" y2="28" stroke="#78350f" stroke-width="2"/>
  <line x1="30" y1="34" x2="50" y2="34" stroke="#78350f" stroke-width="2"/>
</svg>''',

    "car_driver.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#4338ca" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="64" height="64" rx="16" fill="#eef2ff"/>
  <circle cx="18" cy="46" r="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <circle cx="46" cy="46" r="6" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <path d="M10 40h44a2 2 0 0 0 2-2l-3-12a4 4 0 0 0-4-3H19a4 4 0 0 0-4 3l-3 12a2 2 0 0 0 2 2z" fill="#818cf8" stroke="#4338ca" stroke-width="2.5"/>
  <rect x="20" y="26" width="24" height="7" rx="1" fill="#e0e7ff"/>
  <circle cx="14" cy="36" r="2" fill="#facc15"/>
  <circle cx="50" cy="36" r="2" fill="#facc15"/>
</svg>''',

    "tractor_driver.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" stroke="#15803d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="64" height="64" rx="16" fill="#f0fdf4"/>
  <circle cx="18" cy="48" r="5" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  <circle cx="46" cy="44" r="9" fill="#1e293b" stroke="#0f172a" stroke-width="2.5"/>
  <path d="M14 44h18v-8l-8-8h-6l-4 8v8z" fill="#22c55e" stroke="#15803d" stroke-width="2"/>
  <rect x="30" y="24" width="8" height="20" rx="1" fill="#16a34a"/>
  <line x1="20" y1="20" x2="20" y2="28" stroke="#0f172a" stroke-width="3"/>
  <circle cx="46" cy="44" r="4" fill="#facc15"/>
</svg>'''
}

target_dir = r"C:\Users\Umesh Kumar\.gemini\antigravity\scratch\kaam-milega\static\images\icons"
for fname, content in driver_icons.items():
    with open(os.path.join(target_dir, fname), "w", encoding="utf-8") as f:
        f.write(content)
print("Driver icons created successfully!")
