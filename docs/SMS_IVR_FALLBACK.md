# SMS / IVR Fallback Architecture: "काम मिलेगा" for Feature Phones (Un-Smartphone Users)

While smartphones are widespread, many older rural artisans still use basic keypad feature phones (JioBharat, Nokia 105, etc.). This architecture note details how "काम मिलेगा" extends access to non-smartphone users via **Missed Call + Interactive Voice Response (IVR)**.

---

## 1. Core Workflow: Missed Call Registration

```
[Keypad Phone Worker]
        │
        ▼ (Gives missed call to Toll-Free / Virtual Number)
┌──────────────────────────────────────┐
│  Cloud Telephony Gateway             │
│  (Exotel / Awaaz.De / Twilio India)  │
└──────────────────────────────────────┘
        │
        ▼ (Webhook triggered: Caller Phone Number, Circle)
┌──────────────────────────────────────┐
│  Kaam Milega IVR Dispatcher          │
│  Schedules automated return call     │
└──────────────────────────────────────┘
        │
        ▼ (Within 60 seconds: Automated Call Back)
┌──────────────────────────────────────┐
│  Automated Voice Menu (IVR) in Hindi │
│  "काम मिलेगा में आपका स्वागत है।"   │
└──────────────────────────────────────┘
```

---

## 2. Interactive Voice Menu Script (DTMF Keypad Input)

### Step 1: Language & Age Confirmation
> *"काम मिलेगा में आपका स्वागत है। हिन्दी के लिए 1 दबाएं। भोजपुरी खातिर 2 दबाएं।"*  
> (User presses 1)  
> *"कानून के अनुसार काम के लिए आपकी उम्र 18 वर्ष या उससे अधिक होनी चाहिए। यदि आपकी उम्र 18 वर्ष या उससे अधिक है, तो 1 दबाएं।"*  
> (User presses 1 -> Validated as Adult)

### Step 2: Skill Selection (DTMF)
> *"अपने काम का चयन करें:*  
> *राजमिस्त्री के लिए 1 दबाएं,*  
> *प्लंबर के लिए 2 दबाएं,*  
> *बिजली मिस्त्री के लिए 3 दबाएं,*  
> *बोरिंग या हैंडपंप के लिए 4 दबाएं,*  
> *बढ़ई के लिए 5 दबाएं,*  
> *पेंटर के लिए 6 दबाएं,*  
> *वेल्डर के लिए 7 दबाएं,*  
> *मजदूर के लिए 8 दबाएं।"*  
> (User presses 1 -> Mason)

### Step 3: Location (Pincode / District voice prompt)
> *"अपने इलाके का 6 अंकों का पिनकोड दबाएं।"*  
> (User enters 221001 -> Varanasi)

### Step 4: Name Voice Recording
> *"बीप की आवाज के बाद अपना नाम बोलें।"*  
> (User speaks: *"रामेश्वर मिस्त्री"*)  
> (Audio stored as `.wav` and transcribed via Bhashini / Whisper API)

---

## 3. Job Alerts via Outbound SMS & Automated Calls
* When an employer posts a job in that district matching their skill:
  * An automated SMS is sent: *"नया काम: शिवपुर में 3 राजमिस्त्री चाहिए। दिहाड़ी ₹750। बात करने के लिए 1 दबाएं या कॉल करें।"*
  * Feature phone workers receive an automated voice call connecting them directly to the employer.
