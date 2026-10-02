# "काम मिलेगा" (Kaam Milega) — Bharat Blue-Collar LinkedIn (ग्रामीण कुशल कारीगर व मजदूर मंच)

> **मकसद (Vision):** भारत के गाँव-कस्बों के राजमिस्त्री, प्लंबर, इलेक्ट्रीशियन, बढ़ई, पेंटर, वेल्डर, चालक और मजदूरों को उनकी असली **कारीगरी और हुनर** के आधार पर सीधी पहचान और रोज़गार मिले — बिना किसी बिचौलिए या कमीशन के (0% Commission)।

---

## 🌟 Core Features (मुख्य विशेषताएं)

### 🤝 1. Bharat Blue-Collar LinkedIn (कारीगर डिजिटल पहचान)
- **साथी कारीगरों की मुहर (Peer Vouching)**: साथी कारीगर एक-दूसरे के काम को प्रमाणित करते हैं (Skill Endorsements)।
- **कारीगरी एल्बम (Proof of Craftsmanship)**: पारंपरिक रिज्यूमे की जगह असली काम की 3 कंप्रेस्ड तस्वीरें (चिनवाई, प्लंबिंग, गाड़ी आदि)।
- **3-स्तरीय पहचान बैज (Trust Tiers)**:
  - 🥉 **Tier 1 (ब्रॉन्ज)**: मोबाइल ओटीपी सत्यापित।
  - 🥈 **Tier 2 (सिल्वर)**: 2+ साथी कारीगरों द्वारा प्रमाणित।
  - 🥇 **Tier 3 (मास्टर कारीगर)**: 5+ मुहर और 4.5★ रेटिंग।
- **काम की स्थिति (Status)**:
  - 🟢 तुरंत उपलब्ध (Available)
  - 🔴 व्यस्त (Busy)
  - 🌾 खेती / फसल कटाई अवकाश (Seasonal Agricultural Dormancy)

### 🗣️ 2. Low-Literacy, Voice-First & 12 Languages
- **12 भारतीय भाषाएं**: हिन्दी, भोजपुरी, English, বাংলা, मराठी, తెలుగు, தமிழ், ಕನ್ನಡ, ગુજરાતી, ਪੰਜਾਬੀ, ଓଡ଼ିଆ, മലയാളം।
- **आवाज़ में सुनें (Voice Playback)**: हर निर्देश, बटन और प्रोफ़ाइल के लिए 🔊 स्पीकर बटन।
- **चित्र व आइकन आधारित इंटरफ़ेस**: बड़े टच-फ्रेंडली कार्ड्स (न्यूनतम 48px)।

### 🛡️ 3. Privacy, DPDP Act 2023 & Child Labour Protection
- **सेंसिटिव फोटो चेतावनी (Sensitive Upload Warning)**: आधार कार्ड, पैन कार्ड या बैंक पासबुक अपलोड करने पर सख्त चेतावनी।
- **निगरानी मुक्त (Zero Work History Surveillance)**: साहूकारों और अनुचित निगरानी से बचाने के लिए पुरानी पर्चियों और कमाई का सार्वजनिक इतिहास संग्रहित नहीं किया जाता।
- **कड़ा बाल श्रम निषेध (18+ Age Gate)**: बाल एवं किशोर श्रम अधिनियम के तहत 18 वर्ष से कम आयु का पंजीकरण पूरी तरह प्रतिबंधित।
- **डेटा मिटाने का अधिकार (Right to Erasure)**: DPDP Act 2023 के तहत 1-क्लिक में प्रोफ़ाइल पूरी तरह हटाने की सुविधा।
- **एंटी-स्क्रैपिंग शील्ड**: फ़ोन नंबर केवल सिंगल-यूज़ टोकन और रेट-लिमिटिंग के बाद ही दिखाई देते हैं।

### ⚡ 4. Rural Network Optimized (< 300 KB)
- संपूर्ण क्लाइंट बंडल 300 KB से कम (299.9 KB), जो 2G/3G ग्रामीण नेटवर्क पर 1 सेकंड में लोड होता है।
- स्वचालित ब्राउज़र-साइड 50 KB फोटो कंप्रेशन।
- ऑफलाइन PWA सहायता।

### 📄 5. काम की पर्ची (Digital Work Slip) & आपातकालीन हेल्पलाइन
- मजदूरी विवाद रोकने हेतु व्हाट्सएप पर तुरंत डिजिटल काम की पर्ची (Work Agreement)।
- राष्ट्रीय आपातकालीन हेल्पलाइन: **112** (पुलिस), **1098** (चाइल्डलाइन), **181** (महिला सुरक्षा), **14434** (श्रम मंत्रालय)।

---

## 🚀 Quick Start (शुरुआत कैसे करें)

### Prerequisites
- Python 3.9+
- Pip

### 1. Run Locally
```bash
pip install -r requirements.txt
python server.py
```
Open browser at: `http://localhost:8080` (or `http://<your-ip>:8080` on mobile)

### 2. Run with Docker
```bash
docker compose up -d --build
```

### 3. Run Automated Cyber Defense Tests
```bash
python test_kaam_milega.py
```
*(All 20/20 Security & Privacy Tests)*

### 4. Run Performance & Concurrency Benchmarks
```bash
python benchmark_suite.py
```
*(All 5/5 Scale & Latency Benchmarks)*

---

## 📁 Project Structure

```
kaam-milega/
├── api.py                 # REST API endpoints & security logic
├── database.py            # SQLite schema, migrations & seed data
├── server.py              # Async HTTP application server (Port 8080)
├── security.py            # Rate limiting, anti-scraping & XSS sanitization
├── test_kaam_milega.py    # 20 automated cyber defense & privacy tests
├── benchmark_suite.py     # 5 scale, latency & payload benchmarks
├── templates/
│   └── index.html         # Responsive, accessible mobile-first UI
├── static/
│   ├── css/app.css        # Responsive Tailwind & lightweight styles
│   └── js/
│       ├── app.js         # Core application logic & profile views
│       ├── i18n.js        # 12-language translation dictionary
│       ├── search.js      # Filter & worker search engine
│       ├── wizard.js      # 18+ worker registration wizard
│       ├── speech.js      # Web Speech API & voice prompt playback
│       ├── jobs.js        # Job posting & employer compliance
│       ├── work_slip.js   # WhatsApp agreement slip generator
│       ├── compliance.js  # DPDP consent & child labour gates
│       └── geo_data.js    # All India state & district mapping
├── Dockerfile             # Container build definition
├── docker-compose.yml     # Container orchestration
└── requirements.txt       # Minimal dependencies (aiohttp)
```

---

## 📜 License & Compliance
Built in compliance with:
- Digital Personal Data Protection (DPDP) Act, 2023
- Child and Adolescent Labour (Prohibition and Regulation) Act, 1986
- Information Technology Act, 2000
