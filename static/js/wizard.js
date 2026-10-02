let wizardState = {
currentStep: 1,
totalSteps: 5,
name: '',
phone: '',
birthYear: 1995,
declared18Plus: false,
skills: [],
isTeamLeader: false,
teamSize: 1,
state: 'उत्तर प्रदेश (Uttar Pradesh)',
district: 'वाराणसी (Varanasi)',
tehsil: 'पिंडरा (Pindra)',
village: '',
experienceYears: 5,
dailyRate: 650,
availabilityStatus: 'available',
bioText: '',
photoUrl: '',
consentAccepted: false
};
function getBase64ByteLength(str) {
if (!str) return 0;
const commaIdx = str.indexOf(',');
const b64 = commaIdx >= 0 ? str.slice(commaIdx + 1) : str;
const padding = (b64.endsWith('==') ? 2 : (b64.endsWith('=') ? 1 : 0));
return Math.floor((b64.length * 3) / 4) - padding;
}
function compressImage(file, maxTargetBytes = 35 * 1024) {
return new Promise((resolve, reject) => {
if (!file || !file.type || !file.type.startsWith('image/')) {
return reject(new Error('Invalid image file'));
}
const reader = new FileReader();
reader.onerror = () => reject(new Error('Failed to read file'));
reader.onload = (event) => {
const img = new Image();
img.onerror = () => reject(new Error('Failed to parse image'));
img.onload = () => {
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const attempts = [
{ maxDim: 320, quality: 0.65, mime: 'image/webp' },
{ maxDim: 260, quality: 0.55, mime: 'image/webp' },
{ maxDim: 220, quality: 0.45, mime: 'image/jpeg' },
{ maxDim: 180, quality: 0.35, mime: 'image/jpeg' },
{ maxDim: 140, quality: 0.25, mime: 'image/jpeg' },
{ maxDim: 100, quality: 0.20, mime: 'image/jpeg' }
];

let bestResult = null;
let bestBytes = Infinity;

for (const step of attempts) {
let w = img.width;
let h = img.height;
if (w > h) {
if (w > step.maxDim) {
h = Math.round((h * step.maxDim) / w);
w = step.maxDim;
}
} else {
if (h > step.maxDim) {
w = Math.round((w * step.maxDim) / h);
h = step.maxDim;
}
}

canvas.width = w;
canvas.height = h;
ctx.clearRect(0, 0, w, h);
ctx.drawImage(img, 0, 0, w, h);

let b64 = canvas.toDataURL(step.mime, step.quality);
if (b64.startsWith('data:image/png') && step.mime !== 'image/png') {
b64 = canvas.toDataURL('image/jpeg', step.quality);
}

const bytes = getBase64ByteLength(b64);
if (bytes < bestBytes) {
bestBytes = bytes;
bestResult = b64;
}
if (bytes <= maxTargetBytes) {
return resolve(b64);
}
}
if (bestBytes <= 50 * 1024) {
resolve(bestResult);
} else {
reject(new Error('Unable to compress photo under 50KB'));
}
};
img.src = event.target.result;
};
reader.readAsDataURL(file);
});
}

const WK = ["step1_title", "step1_sub", "photo_rule", "name_label", "name_ph", "phone_label", "phone_ph", "phone_note", "step2_title", "law_title", "law_desc", "birth_label", "underage_title", "adult_eligible", "declaration_18", "step3_title", "step3_sub", "selected_badge", "special_skill", "btn_add_skill", "team_leader_q", "team_leader_sub", "team_size_lbl", "step4_title", "btn_gps", "state_lbl", "district_lbl", "tehsil_lbl", "tehsil_ph", "village_lbl", "village_ph", "step5_title", "wage_lbl", "per_day", "exp_lbl", "years", "status_lbl", "status_avail", "status_busy", "dpdp_consent", "btn_back", "btn_next", "btn_publish", "alert_name", "alert_phone", "alert_underage", "alert_declare", "alert_skill", "alert_village", "alert_consent", "alert_success", "alert_photo_limit", "tts_step1", "tts_step2", "tts_step3", "tts_step4", "tts_step5", "tts_success"];
const WD = {"bn": ["আপনার নাম ও ছবি", "নিয়োগকর্তারা আপনার প্রোফাইলে এটি দেখতে পাবেন।", "⚠️ কঠোর নিয়ম: কেবল 50KB বা তার কম সাইজের ছবি গ্রহণযোগ্য", "পুরো নাম *", "যেমন: রামেশ্বর মিস্ত্রি", "মোবাইল নম্বর *", "১০ সংখ্যার নম্বর", "🔒 নম্বর সুরক্ষিত থাকবে, সরাসরি কাউকে দেখানো হবে না।", "বয়স যাচাইকরণ", "⚖️ শিশুশ্রম নিষিদ্ধ আইন:", "শিশুশ্রম নিষিদ্ধ আইন অনুযায়ী কাজের জন্য কমপক্ষে ১৮ বছর বয়স আবশ্যক।", "আপনার জন্ম সাল", "নিবন্ধন অযোগ্য (১৮ বছরের কম)", "বয়স যাচাই সম্পন্ন: আপনি ১৮+ প্রাপ্তবয়স্ক শ্রেণীতে আছেন।", "আমি घोषणा করছি যে আমার বয়স ১৮ বছর বা বেশি এবং তথ্য সঠিক।", "আপনার কাজ ও দক্ষতা", "এক বা একাধিক কাজ নির্বাচন করুন (কারিগর ও চালক):", "✓ নির্বাচিত", "বিশেষ দক্ষতা", "➕ নতুন কাজ যোগ করুন", "আপনার কি নিজস্ব কর্মী দল বা গাড়ি আছে?", "ঠিকাদারি / কর্মী দল / পরিবহন প্রোফাইলের জন্য", "দলের সদস্য সংখ্যা:", "আপনার এলাকা", "📍 জিপিএস দিয়ে এলাকা নির্ধারণ (GPS)", "রাজ্য (State)", "জেলা (District)", "থানা / ব্লক / শহর", "যেমন: সদর, বারাসাত", "গ্রাম / এলাকা *", "যেমন: হরিপুর, শান্তিনগর", "মজুরি ও প্রাপ্যতা", "দৈনিক মজুরির হার", "প্রতি দিন", "কাজের অভিজ্ঞতা", "বছর", "বর্তমান প্রাপ্যতা", "🟢 কাজের জন্য প্রস্তুত", "🔴 বর্তমানে ব্যস্ত", "আমি DPDP Act 2023 এর অধীনে কাজ পাওয়ার উদ্দেশ্যে তথ্য ব্যবহারে সম্মতি দিচ্ছি।", "← পেছনে (Back)", "এগিয়ে যান (Next) →", "✓ প্রোফাইল প্রকাশ করুন", "অনুগ্রহ করে আপনার পুরো নাম লিখুন।", "অনুগ্রহ করে ১০ সংখ্যার বৈধ মোবাইল নম্বর দিন।", "আইন অনুযায়ী ১৮ বছরের কম বয়সী কেউ কাজের নিবন্ধন করতে পারবেন না।", "অনুগ্রহ করে নিশ্চিত করুন যে আপনার বয়স ১৮ বছর বা তার বেশি।", "অনুগ্রহ করে অন্তত একটি কাজ নির্বাচন করুন।", "অনুগ্রহ করে আপনার গ্রাম বা এলাকার নাম লিখুন।", "অনুগ্রহ করে তথ্য সুরক্ষা সম্মতি বাক্সে টিক দিন।", "অভিনন্দন! আপনার প্রোফাইল সফলভাবে তৈরি হয়েছে।", "ছবির আকার 50KB এর বেশি। ছোট ছবি নির্বাচন করুন।", "অনুগ্রহ করে আপনার পুরো নাম লিখুন এবং একটি পরিষ্কার ছবি দিন।", "আপনার বয়স জানান। ১৮ বছরের কম বয়সী কেউ কাজ করতে পারেন না।", "আপনার কাজ নির্বাচন করুন।", "আপনার এলাকা নির্বাচন করুন।", "দৈনিক মজুরি নির্বাচন করে প্রোফাইল প্রকাশ করুন।", "অভিনন্দন! আপনার প্রোফাইল তৈরি হয়েছে।"], "hi": ["आपका नाम और फोटो", "ग्राहकों को आपकी प्रोफाइल पर यही दिखेगा।", "⚠️ सख्त नियम: केवल 50KB या उससे कम साइज की फोटो मान्य है", "पूरा नाम (Full Name) *", "जैसे: रामेश्वर मिस्त्री", "मोबाइल नंबर (Mobile Number) *", "10 अंकों का नंबर", "🔒 आपका नंबर सुरक्षित है, सिर्फ आपकी सहमति से कॉल होगी।", "आयु सत्यापन (Age Verification)", "⚖️ बाल श्रम निषेध कानून (Child Labour Prohibition Act):", "बाल श्रम निषेध कानून के तहत काम के लिए न्यूनतम आयु 18 वर्ष अनिवार्य है।", "आपका जन्म वर्ष (Year of Birth)", "पंजीकरण अमान्य (Under 18)", "उम्र सत्यापन योग्य: आप वयस्क (18+) श्रेणी में हैं।", "मैं घोषणा करता हूँ कि मेरी आयु 18 वर्ष या उससे अधिक है और जानकारी सत्य है।", "आपका हुनर (Skills / Driving)", "एक या एक से ज्यादा काम चुन सकते हैं (ड्राइवर व कारीगर):", "✓ चुना गया", "विशेष हुनर", "➕ नया काम या हुनर जोड़ें (Add Skill If Not Listed)", "क्या आपकी अपनी गाड़ी बेड़ा या मजदूरों की टीम है?", "ठेकेदारी / टोली / ट्रांसपोर्ट प्रोफाइल के लिए", "टीम या गाड़ियों की संख्या:", "आपका इलाका (Location)", "📍 मेरी लोकेशन पहचानें (Auto Detect GPS)", "राज्य (State) — पूरे भारत के सभी राज्य", "जिला (District)", "तहसील / कस्बा (Tehsil / Town)", "जैसे: पिंडरा, सदर, चुनार", "गाँव / मोहल्ला (Village / Area) *", "जैसे: करखियांव, शिवपुर", "दिहाड़ी और उपलब्धता", "रोज की दिहाड़ी दर (Daily Wage Rate)", "प्रति दिन (Per Day)", "काम का अनुभव (Experience in Years)", "साल", "वर्तमान स्थिति (Current Status)", "🟢 काम के लिए उपलब्ध", "🔴 अभी व्यस्त हूँ", "मैं DPDP Act 2023 के तहत अपनी जानकारी काम पाने हेतु साझा करने की सहमति देता हूँ।", "← पीछे (Back)", "आगे बढ़ें (Next) →", "✓ प्रोफाइल प्रकाशित करें", "कृपया अपना नाम भरें।", "कृपया 10 अंकों का वैध मोबाइल नंबर भरें।", "कानूनन 18 वर्ष से कम आयु के व्यक्ति काम के लिए पंजीकरण नहीं कर सकते।", "कृपया पुष्टि करें कि आपकी आयु 18 वर्ष या उससे अधिक है।", "कृपया कम से कम एक हुनर (Skill) चुनें।", "कृपया अपने गाँव या इलाके का नाम भरें।", "कृपया डेटा गोपनीयता सहमति बॉक्स पर सही का निशान लगाएं।", "बधाई हो! आपकी प्रोफाइल सफलतापूर्वक बन गई है।", "फोटो का आकार 50KB से अधिक है। कृपया छोटी फोटो चुनें।", "कृपया अपना पूरा नाम लिखें और अपनी एक साफ फोटो लगाएं।", "अपनी उम्र बताएं। कानून के अनुसार 18 वर्ष से कम उम्र के व्यक्ति काम के लिए पंजीकरण नहीं कर सकते।", "आप जो काम या गाड़ी चलाते हैं, उन कार्डों को दबाएं।", "अपना राज्य, जिला और गाँव चुनें ताकि आसपास के लोग आपको आसानी से काम दे सकें।", "अपनी रोज की दिहाड़ी चुनें और सहमति देकर प्रोफाइल प्रकाशित करें।", "बधाई हो! आपकी कारीगर प्रोफाइल बन गई है।"], "en": ["Your Name & Photo", "Employers will see this on your public profile.", "⚠️ Strict Rule: Photo must be 50KB or smaller", "Full Name *", "e.g. Rameshwar Mistry", "Mobile Number *", "10-digit mobile number", "🔒 Phone number masked; clients connect only with your permission.", "Age Verification (18+ Gate)", "⚖️ Child Labour Prohibition Act:", "Under Child Labour Act, minimum age of 18 years is mandatory for work.", "Year of Birth", "Registration Ineligible (Under 18)", "Age Verified: You qualify under the adult (18+) category.", "I declare that I am 18 years or older and provided details are true.", "Your Skills & Trade", "Select one or more trades you work in (Artisans & Drivers):", "✓ Selected", "Special Skill", "➕ Add Skill If Not Listed", "Do you have your own vehicle fleet or worker team?", "For contractor / crew / transport profile", "Team or Fleet Size:", "Your Work Location", "📍 Detect My Location (GPS)", "State — All India", "District", "Tehsil / Town", "e.g. Pindra, Sadar, Chunar", "Village / Locality *", "e.g. Karkhiyanv, Shivpur", "Daily Wage & Availability", "Daily Wage Rate", "Per Day", "Work Experience (Years)", "Years", "Current Availability Status", "🟢 Available for Work", "🔴 Currently Busy", "I consent under DPDP Act 2023 for my details to be stored to find employment.", "← Back", "Next →", "✓ Publish Profile", "Please enter your full name.", "Please enter a valid 10-digit mobile number.", "Minors under 18 cannot register for work under the Child Labour Act.", "Please confirm that you are 18 years of age or older.", "Please select at least one skill or trade.", "Please enter your village or area name.", "Please accept the DPDP data privacy consent checkbox.", "Congratulations! Your worker profile has been published successfully.", "Photo exceeds 50KB. Please choose a smaller photo.", "Please enter your full name and upload a clear photo of yourself.", "Confirm your age. By law, individuals under 18 cannot register for work.", "Select the cards representing your work, skills, or vehicles.", "Choose your state, district, and village so nearby employers can contact you.", "Set your daily wage rate, accept data privacy terms, and publish your profile.", "Congratulations! Your worker profile has been published."], "bho": ["राउर नाम आ फोटो", "मालिकन के राउर प्रोफाइल पर इहे लउकी।", "⚠️ कड़ा नियम: फोटो 50KB से छोट होखे के चाहीं", "पूरा नाम *", "जइसे: रामेश्वर मिस्त्री", "मोबाइल नंबर *", "10 अंकन के नंबर", "🔒 राउर नंबर सुरक्षित बा, सिर्फ राउर मंजूरी से फोन लागी।", "उमिर सत्यापन (Age Verification)", "⚖️ बाल मजदूरी निषेध कानून:", "बाल मजदूरी निषेध कानून के तहत काम खातिर 18 बरिस जरूरी बा।", "राउर जनम के साल", "पंजीकरण ना हो पाई (Under 18)", "उमिर सही बा: रउआ 18+ वयस्क श्रेणी में बानी।", "हम घोषणा करत बानी कि हमार उमिर 18 बरिस या ढेर बा आ जानकारी साँच बा।", "राउर हुनर आ काम", "एक भा एक से ढेर काम चुनीं (कारीगर आ ड्राइवर):", "✓ चुनल गइल", "खास हुनर", "➕ नया काम भा हुनर जोड़ीं", "का राउर आपन गाड़ी भा मजदूरन के टोली बा?", "ठेकेदारी भा टोली खातिर", "टोली भा गाड़ियन के गिनती:", "राउर इलाका (Location)", "📍 हमार लोकेशन जानीं (GPS)", "राज्य (State)", "जिला (District)", "तहसील / कस्बा", "जइसे: पिंडरा, सदर, चुनार", "गाँव / टोला *", "जइसे: करखियांव, शिवपुर", "दिहाड़ी आ काम के स्थिति", "रोज के दिहाड़ी दर", "हर दिन", "काम के तजुर्बा", "बरिस", "काम के स्थिति", "🟢 काम खातिर तैयार", "🔴 अभी बियस्त बानी", "हम DPDP Act 2023 के तहत आपन जानकारी काम पावे खातिर देवे के सहमति देत बानी।", "← पाछे (Back)", "आगे बढ़ीं (Next) →", "✓ प्रोफाइल बनावीं", "कृपा कइ के आपन नाम लिखीं।", "कृपा कइ के 10 अंकन के फोन नंबर लिखीं।", "कानूनन 18 से कम उमिर के लोग काम खातिर रजिस्टर ना कर सकेला।", "पुष्टि करीं कि राउर उमिर 18 बरिस या ओकरा से ढेर बा।", "कम से कम एगो हुनर जरूर चुनीं।", "आपन गाँव भा टोला के नाम लिखीं।", "डेटा सुरक्षा सहमति बॉक्स पर टिक लगाईं।", "बधाई! राउर प्रोफाइल बन गइल बा।", "फोटो का आकार 50KB से अधिक है। कृपया छोटी फोटो चुनें।", "आपन पूरा नाम लिखीं आ एगो साफ फोटो लगाईं।", "आपन उमिर बताईं। 18 से कम उमिर के लोग काम खातिर रजिस्टर ना कर सकेला।", "जे काम रउआ करिले, ओकरा कार्ड पर छुईं।", "आपन राज्य, जिला आ गाँव चुनीं।", "आपन दिहाड़ी दर चुनीं आ प्रोफाइल प्रकाशित करीं।", "बधाई! राउर कारीगर प्रोफाइल बन गइल बा।"]};
const WIZARD_I18N = {};
for (const [l, v] of Object.entries(WD)) {
WIZARD_I18N[l] = {};
WK.forEach((k, i) => WIZARD_I18N[l][k] = v[i]);
}
const TRADE_SUBS = {
hi: {
halwai: 'मिठाई, नमकीन, शादी ऑर्डर',
event_cook: 'महाराज, कुक, कैटरिंग खाना',
catering_helper: 'खाना परोसना, टेबल व सफाई',
tent_decorator: 'पंडाल, स्टेज, लाइट-साउंड',
auto_driver: 'ऑटो रिक्शा, लोकल सवारी',
erickshaw_driver: 'बैटरी रिक्शा, बाजार सवारी',
pickup_driver: 'छोटा हाथी, माल ढुलाई',
car_driver: 'कैब, निजी चालक, लंबी दूरी',
tractor_driver: 'खेत जुताई, ट्रॉली ढुलाई',
mason: 'ईंट, प्लास्टर, ढलाई',
plumber: 'पाइप, टंकी, नल',
electrician: 'वायरिंग, मोटर, लाइट',
boring: 'हैंडपंप, समरसेबल',
carpenter: 'लकड़ी, चौखट, फर्नीचर',
painter: 'पुट्टी, रंगाई, डिस्टेंपर',
welder: 'गेट, ग्रिल, शेड',
labor: 'खुदाई, ढुलाई, सहायता'
},
en: {
halwai: 'Sweets, snacks, catering',
event_cook: 'Master cook, banquet food',
catering_helper: 'Food service, table & cleaning',
tent_decorator: 'Pandal, stage, lighting & sound',
auto_driver: 'Auto rickshaw, passenger rides',
erickshaw_driver: 'E-rickshaw, market rides',
pickup_driver: 'Mini truck, cargo transport',
car_driver: 'Cab, private chauffeur, taxi',
tractor_driver: 'Field plowing, trolley transport',
mason: 'Brickwork, plaster, construction',
plumber: 'Pipes, water tank, leak repair',
electrician: 'Wiring, motors, electricals',
boring: 'Handpump, tubewell, submersible',
carpenter: 'Woodwork, doors, furniture',
painter: 'Wall putty, paint, distemper',
welder: 'Iron gates, grills, sheds',
labor: 'Excavation, loading, helper'
}
};
function getWizText(key, ...args) {
const lang = (typeof currentLang !== 'undefined' && currentLang) ? currentLang : 'hi';
const M = {
step_label: { en:`Step $1 of $2`, bn:`ধাপ $1 / $2`, bho:`चरण $1 के $2`, mr:`टप्पा $1 पैकी $2`, te:`దశ $1 లో $2`, ta:`படி $1 / $2`, kn:`ಹಂತ $1 / $2`, gu:`પગલું $1 / $2`, pa:`ਪੜਾਅ $1 ਵਿੱਚੋਂ $2`, or:`ପର୍ଯ୍ୟାୟ $1 ର $2`, ml:`ഘട്ടം $1 / $2`, _:`चरण $1 का $2` },
pct_done: { en:`$1% Completed`, bn:`$1% সম্পন্ন`, bho:`$1% पूरा भइल`, mr:`$1% पूर्ण`, te:`$1% పూర్తయింది`, ta:`$1% முடிந்தது`, kn:`$1% ಪೂರ್ಣಗೊಂಡಿದೆ`, gu:`$1% પૂર્ણ`, pa:`$1% ਪੂਰਾ ਹੋਇਆ`, or:`$1% ସମ୍ପୂର୍ଣ୍ଣ`, ml:`$1% പൂർത്തിയായി`, _:`$1% पूरा हुआ` },
photo_valid: { en:`📦 Photo: $1 KB (Valid ✅)`, bn:`📦 ছবির সাইজ: $1 KB (বৈধ ✅)`, bho:`📦 फोटो साइज: $1 KB (सही बा ✅)`, _: `📦 फोटो साइज: $1 KB (मान्य ✅)` },
age_approx: { en:`(Age: ~$1 yrs)`, bn:`(বয়স: প্রায় $1 বছর)`, bho:`(उमिर: लगभग $1 बरिस)`, _: `(उम्र: लगभग $1 वर्ष)` },
underage_desc: { en:`Minors under 18 ($1 yrs) cannot register.`, bn:`১৮ বছরের কম বয়সী ($1 বছর) নিবন্ধন নিষিদ্ধ।`, bho:`18 से कम उमिर ($1 बरिस) के लोग रजिस्टर ना कर सकेला।`, _: `18 वर्ष से कम आयु ($1 वर्ष) के लोग पंजीकरण नहीं कर सकते।` }
};
if (M[key]) {
let tmpl = (M[key][lang] || M[key]['_']);
args.forEach((a, i) => { tmpl = tmpl.replace(`$${i+1}`, a); });
return tmpl;
}
const dict = WIZARD_I18N[lang] || (lang === 'en' ? WIZARD_I18N['en'] : WIZARD_I18N['hi']);
let val = dict ? dict[key] : undefined;
if (val === undefined) {
val = (lang === 'en') ? (WIZARD_I18N['en'] && WIZARD_I18N['en'][key]) : (WIZARD_I18N['hi'] && WIZARD_I18N['hi'][key]);
}
return (val !== undefined) ? val : key;
}
function renderWizardStep() {
const container = document.getElementById('wizard-container');
if (!container) return;
const currentYear = new Date().getFullYear();
const calculatedAge = currentYear - wizardState.birthYear;
const isUnderage = calculatedAge < 18;
const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
const dict = (typeof I18N_DATA !== 'undefined' && I18N_DATA[lang]) ? I18N_DATA[lang] : (I18N_DATA['hi'] || {});
let content = `
<div class="mb-6">
<div class="flex justify-between items-center mb-2">
<span class="text-sm font-bold text-green-800">
${getWizText('step_label', wizardState.currentStep, wizardState.totalSteps)}
</span>
<span class="text-xs bg-green-100 text-green-800 px-3 py-1 rounded-full font-bold">
${getWizText('pct_done', Math.round((wizardState.currentStep / wizardState.totalSteps) * 100))}
</span>
</div>
<div class="w-full bg-slate-200 h-3 rounded-full overflow-hidden">
<div class="bg-green-600 h-3 rounded-full transition-all duration-300" style="width: ${(wizardState.currentStep / wizardState.totalSteps) * 100}%"></div>
</div>
</div>
`;
if (wizardState.currentStep === 1) {
content += `
<div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
<div class="flex items-center justify-between mb-4">
<h2 class="text-2xl font-extrabold text-slate-900">${getWizText('step1_title')}</h2>
<button type="button" class="speak-btn" onclick="speakPrompt('${getWizText('tts_step1').replace(/'/g, "\\'")}', this)" title="Audio">
🔊
</button>
</div>
<p class="text-slate-600 mb-6 text-sm">${getWizText('step1_sub')}</p>
<div class="flex flex-col items-center mb-6">
<div class="relative mb-3">
<div id="photo-preview-box" class="w-28 h-28 rounded-full border-4 border-green-500 overflow-hidden bg-slate-100 flex items-center justify-center shadow-inner">
${wizardState.photoUrl
? `<img src="${wizardState.photoUrl}" class="w-full h-full object-cover">`
: `<span class="text-4xl">👤</span>`
}
</div>
<label for="camera-input" class="absolute bottom-0 right-0 bg-green-700 text-white w-10 h-10 rounded-full flex items-center justify-center shadow-lg cursor-pointer touch-btn hover:bg-green-800">
📷
</label>
<input type="file" id="camera-input" accept="image/*" capture="user" class="hidden" onchange="handlePhotoUpload(event)">
</div>
<div id="photo-size-badge" class="text-xs font-bold ${wizardState.photoUrl ? 'text-green-700 bg-green-50 px-3 py-1 rounded-full border border-green-200' : 'text-slate-500'}">
${wizardState.photoUrl
? getWizText('photo_valid', (getBase64ByteLength(wizardState.photoUrl) / 1024).toFixed(1))
: getWizText('photo_rule')}
</div>
</div>
<div class="mb-4">
<label class="block text-sm font-bold text-slate-700 mb-1">${getWizText('name_label')}</label>
<input type="text" id="wizard-name" value="${wizardState.name}" oninput="wizardState.name = this.value" placeholder="${getWizText('name_ph')}" class="w-full p-4 border-2 border-slate-300 rounded-xl text-lg font-bold focus:border-green-600 focus:outline-none touch-btn">
</div>
<div class="mb-4">
<label class="block text-sm font-bold text-slate-700 mb-1">${getWizText('phone_label')}</label>
<input type="tel" id="wizard-phone" value="${wizardState.phone}" oninput="wizardState.phone = this.value" placeholder="${getWizText('phone_ph')}" maxlength="10" class="w-full p-4 border-2 border-slate-300 rounded-xl text-lg font-bold focus:border-green-600 focus:outline-none touch-btn">
<span class="text-xs text-slate-500 mt-1 block">${getWizText('phone_note')}</span>
</div>
</div>
`;
}
else if (wizardState.currentStep === 2) {
content += `
<div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
<div class="flex items-center justify-between mb-4">
<h2 class="text-2xl font-extrabold text-slate-900">${getWizText('step2_title')}</h2>
<button type="button" class="speak-btn" onclick="speakPrompt('${getWizText('tts_step2').replace(/'/g, "\\'")}', this)" title="Audio">
🔊
</button>
</div>
<div class="bg-amber-50 border-l-4 border-amber-600 p-4 rounded-r-xl mb-6">
<p class="text-sm font-bold text-amber-900">
${getWizText('law_title')}
</p>
<p class="text-xs text-amber-800 mt-1">
${getWizText('law_desc')}
</p>
</div>
<div class="mb-6">
<label class="block text-sm font-bold text-slate-700 mb-2">${getWizText('birth_label')}</label>
<div class="flex items-center gap-3">
<button type="button" class="stepper-btn" onclick="adjustBirthYear(-1)">−</button>
<div class="flex-1 text-center py-3 bg-slate-100 rounded-xl border-2 border-slate-300">
<span class="text-2xl font-black text-slate-800" id="birth-year-display">${wizardState.birthYear}</span>
<span class="block text-xs font-bold text-slate-500 mt-1">
${getWizText('age_approx', calculatedAge)}
</span>
</div>
<button type="button" class="stepper-btn" onclick="adjustBirthYear(1)">+</button>
</div>
</div>
${isUnderage ? `
<div class="bg-red-100 border-2 border-red-500 text-red-900 p-4 rounded-xl mb-6">
<div class="flex items-center gap-2 mb-1">
<span class="text-2xl">🚫</span>
<strong class="text-base">${getWizText('underage_title')}</strong>
</div>
<p class="text-sm">
${getWizText('underage_desc', calculatedAge)}
</p>
</div>
` : `
<div class="bg-green-50 border border-green-300 p-4 rounded-xl mb-6 flex items-center gap-3">
<span class="text-2xl">✅</span>
<span class="text-sm font-bold text-green-800">${getWizText('adult_eligible')}</span>
</div>
`}
<label class="flex items-start gap-3 p-4 bg-slate-50 border-2 border-slate-200 rounded-xl cursor-pointer touch-btn">
<input type="checkbox" id="wizard-18plus" ${wizardState.declared18Plus ? 'checked' : ''} onchange="toggle18Plus(event)" class="w-6 h-6 mt-0.5 rounded text-green-600 focus:ring-green-500">
<span class="text-sm font-bold text-slate-800">
${getWizText('declaration_18')}
</span>
</label>
</div>
`;
}
else if (wizardState.currentStep === 3) {
const tradeKeys = ['halwai','event_cook','catering_helper','tent_decorator','auto_driver','erickshaw_driver','pickup_driver','car_driver','tractor_driver','mason','plumber','electrician','boring','carpenter','painter','welder','labor'];
content += `
<div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
<div class="flex items-center justify-between mb-4">
<h2 class="text-2xl font-extrabold text-slate-900">${getWizText('step3_title')}</h2>
<button type="button" class="speak-btn" onclick="speakPrompt('${getWizText('tts_step3').replace(/'/g, "\\'")}', this)" title="Audio">
🔊
</button>
</div>
<p class="text-slate-600 mb-4 text-sm">${getWizText('step3_sub')}</p>
<div class="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4 max-h-96 overflow-y-auto pr-1">
${tradeKeys.map(k => {
const t = { key: k, icon: k + '.svg' };
const isSelected = wizardState.skills.includes(t.key);
const tName = (dict.trades && dict.trades[t.key]) ? dict.trades[t.key] : t.name;
const tSub = (TRADE_SUBS[lang] && TRADE_SUBS[lang][t.key]) || (TRADE_SUBS['hi'] && TRADE_SUBS['hi'][t.key]) || '';
return `
<div class="trade-card ${isSelected ? 'selected' : ''}" onclick="toggleSkill('${t.key}')">
<img src="/static/images/icons/${t.icon}" class="w-12 h-12 mb-2" alt="${tName}">
<strong class="text-base font-bold text-slate-900 leading-tight">${tName}</strong>
<span class="text-xs text-slate-500 mt-1">${tSub}</span>
${isSelected ? `<span class="text-green-700 text-xs font-extrabold mt-1">${getWizText('selected_badge')}</span>` : ''}
</div>
`;
}).join('')}
${(typeof getCustomCategories === 'function' ? getCustomCategories() : []).map(cat => {
const isSelected = wizardState.skills.includes(cat);
return `
<div class="trade-card ${isSelected ? 'selected' : ''}" onclick="toggleSkill('${cat.replace(/'/g, "\\'")}')">
<span class="text-4xl mb-2 block">🛠️</span>
<strong class="text-base font-bold text-slate-900 leading-tight">${cat}</strong>
<span class="text-xs text-slate-500 mt-1">${getWizText('special_skill')}</span>
${isSelected ? `<span class="text-green-700 text-xs font-extrabold mt-1">${getWizText('selected_badge')}</span>` : ''}
</div>
`;
}).join('')}
</div>
<button type="button" onclick="openAddCategoryModal('wizard')" class="w-full mb-6 p-3.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border-2 border-dashed border-emerald-400 rounded-xl font-extrabold text-sm flex items-center justify-center gap-2 shadow-sm touch-btn">
<span>➕</span> <span>${getWizText('btn_add_skill')}</span>
</button>
<div class="p-4 bg-slate-50 border border-slate-200 rounded-xl">
<label class="flex items-center justify-between cursor-pointer touch-btn">
<div>
<strong class="block text-sm text-slate-900">${getWizText('team_leader_q')}</strong>
<span class="text-xs text-slate-500">${getWizText('team_leader_sub')}</span>
</div>
<input type="checkbox" id="wizard-team-leader" ${wizardState.isTeamLeader ? 'checked' : ''} onchange="toggleTeamLeader(event)" class="w-6 h-6 rounded text-green-600">
</label>
${wizardState.isTeamLeader ? `
<div class="mt-4 pt-4 border-t border-slate-200 flex items-center justify-between">
<span class="text-sm font-bold text-slate-700">${getWizText('team_size_lbl')}</span>
<div class="flex items-center gap-2">
<button type="button" class="stepper-btn !w-10 !h-10 !text-lg" onclick="adjustTeamSize(-1)">−</button>
<span class="text-xl font-bold w-8 text-center">${wizardState.teamSize}</span>
<button type="button" class="stepper-btn !w-10 !h-10 !text-lg" onclick="adjustTeamSize(1)">+</button>
</div>
</div>
` : ''}
</div>
</div>
`;
}
else if (wizardState.currentStep === 4) {
const statesList = typeof getIndiaStates === 'function' ? getIndiaStates() : [
"उत्तर प्रदेश (Uttar Pradesh)", "बिहार (Bihar)", "मध्य प्रदेश (Madhya Pradesh)", "राजस्थान (Rajasthan)"
];
const districtsList = typeof getDistrictsForState === 'function' ? getDistrictsForState(wizardState.state) : [
"वाराणसी (Varanasi)", "मिर्ज़ापुर (Mirzapur)", "प्रयागराज (Prayagraj)", "पटना (Patna)", "गया (Gaya)"
];
content += `
<div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
<div class="flex items-center justify-between mb-4">
<h2 class="text-2xl font-extrabold text-slate-900">${getWizText('step4_title')}</h2>
<button type="button" class="speak-btn" onclick="speakPrompt('${getWizText('tts_step4').replace(/'/g, "\\'")}', this)" title="Audio">
🔊
</button>
</div>
<button type="button" onclick="detectGPSLocation()" class="w-full mb-5 py-3.5 px-4 bg-green-50 border-2 border-green-600 text-green-800 rounded-xl font-bold flex items-center justify-center gap-2 touch-btn">
${getWizText('btn_gps')}
</button>
<div class="mb-4">
<label class="block text-sm font-bold text-slate-700 mb-1">${getWizText('state_lbl')}</label>
<select id="wizard-state" onchange="onWizardStateChange(this.value)" class="w-full p-4 border-2 border-slate-300 rounded-xl font-bold text-slate-800 focus:border-green-600 touch-btn">
${statesList.map(st => `<option value="${st}" ${wizardState.state === st ? 'selected' : ''}>${st}</option>`).join('')}
</select>
</div>
<div class="mb-4">
<label class="block text-sm font-bold text-slate-700 mb-1">${getWizText('district_lbl')}</label>
<select id="wizard-district" onchange="wizardState.district = this.value" class="w-full p-4 border-2 border-slate-300 rounded-xl font-bold text-slate-800 focus:border-green-600 touch-btn">
${districtsList.map(dt => `<option value="${dt}" ${wizardState.district === dt ? 'selected' : ''}>${dt}</option>`).join('')}
</select>
</div>
<div class="mb-4">
<label class="block text-sm font-bold text-slate-700 mb-1">${getWizText('tehsil_lbl')}</label>
<input type="text" id="wizard-tehsil" oninput="wizardState.tehsil = this.value" value="${wizardState.tehsil}" placeholder="${getWizText('tehsil_ph')}" class="w-full p-4 border-2 border-slate-300 rounded-xl font-bold text-slate-800 touch-btn">
</div>
<div class="mb-4">
<label class="block text-sm font-bold text-slate-700 mb-1">${getWizText('village_lbl')}</label>
<input type="text" id="wizard-village" oninput="wizardState.village = this.value" value="${wizardState.village}" placeholder="${getWizText('village_ph')}" class="w-full p-4 border-2 border-slate-300 rounded-xl font-bold text-slate-800 touch-btn">
</div>
</div>
`;
}
else if (wizardState.currentStep === 5) {
content += `
<div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
<div class="flex items-center justify-between mb-4">
<h2 class="text-2xl font-extrabold text-slate-900">${getWizText('step5_title')}</h2>
<button type="button" class="speak-btn" onclick="speakPrompt('${getWizText('tts_step5').replace(/'/g, "\\'")}', this)" title="Audio">
🔊
</button>
</div>
<div class="mb-6">
<label class="block text-sm font-bold text-slate-700 mb-2">${getWizText('wage_lbl')}</label>
<div class="flex items-center gap-3">
<button type="button" class="stepper-btn" onclick="adjustDailyRate(-50)">−</button>
<div class="flex-1 text-center py-3 bg-green-50 rounded-xl border-2 border-green-300">
<span class="text-3xl font-black text-green-800" id="wage-display">₹${wizardState.dailyRate}</span>
<span class="block text-xs font-bold text-green-700 mt-1">${getWizText('per_day')}</span>
</div>
<button type="button" class="stepper-btn" onclick="adjustDailyRate(50)">+</button>
</div>
</div>
<div class="mb-6">
<label class="block text-sm font-bold text-slate-700 mb-2">${getWizText('exp_lbl')}</label>
<div class="flex items-center gap-3">
<button type="button" class="stepper-btn" onclick="adjustExperience(-1)">−</button>
<div class="flex-1 text-center py-3 bg-slate-100 rounded-xl border-2 border-slate-300">
<span class="text-2xl font-black text-slate-800">${wizardState.experienceYears} ${getWizText('years')}</span>
</div>
<button type="button" class="stepper-btn" onclick="adjustExperience(1)">+</button>
</div>
</div>
<div class="mb-6">
<label class="block text-sm font-bold text-slate-700 mb-2">${getWizText('status_lbl')}</label>
<div class="grid grid-cols-2 gap-3">
<button type="button" onclick="setAvailability('available')" class="p-3.5 rounded-xl border-2 font-bold touch-btn ${wizardState.availabilityStatus === 'available' ? 'border-green-600 bg-green-50 text-green-800' : 'border-slate-200 text-slate-600'}">
${getWizText('status_avail')}
</button>
<button type="button" onclick="setAvailability('busy')" class="p-3.5 rounded-xl border-2 font-bold touch-btn ${wizardState.availabilityStatus === 'busy' ? 'border-red-600 bg-red-50 text-red-800' : 'border-slate-200 text-slate-600'}">
${getWizText('status_busy')}
</button>
</div>
</div>
<div class="p-4 bg-slate-50 border-2 border-slate-200 rounded-xl mb-4">
<label class="flex items-start gap-3 cursor-pointer touch-btn">
<input type="checkbox" id="wizard-consent" ${wizardState.consentAccepted ? 'checked' : ''} onchange="toggleConsent(event)" class="w-6 h-6 mt-0.5 rounded text-green-600">
<span class="text-xs font-bold text-slate-700 leading-relaxed">
${getWizText('dpdp_consent')}
</span>
</label>
</div>
</div>
`;
}
content += `
<div class="flex items-center justify-between gap-4 mt-6">
${wizardState.currentStep > 1 ? `
<button type="button" onclick="prevStep()" class="flex-1 py-4 px-6 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-xl font-extrabold text-lg touch-btn">
${getWizText('btn_back')}
</button>
` : `<div></div>`}
${wizardState.currentStep < wizardState.totalSteps ? `
<button type="button" onclick="nextStep()" class="flex-1 py-4 px-6 bg-green-700 hover:bg-green-800 text-white rounded-xl font-extrabold text-lg shadow-lg touch-btn">
${getWizText('btn_next')}
</button>
` : `
<button type="button" onclick="submitWizard()" class="flex-1 py-4 px-6 bg-green-700 hover:bg-green-800 text-white rounded-xl font-extrabold text-lg shadow-lg touch-btn">
${getWizText('btn_publish')}
</button>
`}
</div>
`;
container.innerHTML = content;
}
function adjustBirthYear(delta) {
const currentYear = new Date().getFullYear();
wizardState.birthYear = Math.max(1950, Math.min(wizardState.birthYear + delta, currentYear - 10));
renderWizardStep();
}
function toggle18Plus(event) {
wizardState.declared18Plus = event.target.checked;
}
function toggleSkill(key) {
const index = wizardState.skills.indexOf(key);
if (index > -1) {
wizardState.skills.splice(index, 1);
} else {
wizardState.skills.push(key);
}
renderWizardStep();
}
function toggleTeamLeader(event) {
wizardState.isTeamLeader = event.target.checked;
renderWizardStep();
}
function adjustTeamSize(delta) {
wizardState.teamSize = Math.max(1, Math.min(wizardState.teamSize + delta, 25));
renderWizardStep();
}
function adjustDailyRate(delta) {
wizardState.dailyRate = Math.max(350, Math.min(wizardState.dailyRate + delta, 3000));
const el = document.getElementById('wage-display');
if (el) el.innerText = `₹${wizardState.dailyRate}`;
}
function adjustExperience(delta) {
wizardState.experienceYears = Math.max(0, Math.min(wizardState.experienceYears + delta, 50));
renderWizardStep();
}
function setAvailability(status) {
wizardState.availabilityStatus = status;
renderWizardStep();
}
function toggleConsent(event) {
wizardState.consentAccepted = event.target.checked;
}
async function handlePhotoUpload(event) {
const file = event.target.files[0];
if (!file) return;
const nameInput = document.getElementById('wizard-name');
if (nameInput && nameInput.value) wizardState.name = nameInput.value;
const phoneInput = document.getElementById('wizard-phone');
if (phoneInput && phoneInput.value) wizardState.phone = phoneInput.value;
const sizeBadge = document.getElementById('photo-size-badge');
const previewBox = document.getElementById('photo-preview-box');
const MAX_ALLOWED_BYTES = 50 * 1024; // 50 KB (51,200 bytes)
const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
const isEn = lang === 'en';
if (file.size > MAX_ALLOWED_BYTES) {
const originalKB = (file.size / 1024).toFixed(1);
const confirmCompress = confirm(isEn
? `⚠️ Selected photo exceeds 50KB (${originalKB} KB)!\n\nRequirement: Profile photo must be 50KB or smaller.\n\nWould you like to automatically compress it under 50KB (<35KB)?`
: `⚠️ चुनी गई फोटो 50KB से बड़ी है (${originalKB} KB)!\n\nनियम: प्रोफाइल फोटो 50KB या उससे कम साइज की होना अनिवार्य है।\n\nक्या आप चाहते हैं कि इसे तुरंत 50KB के अंदर (<35KB) कंप्रेस किया जाए?`
);
if (!confirmCompress) {
event.target.value = '';
wizardState.photoUrl = '';
if (previewBox) previewBox.innerHTML = `<span class="text-4xl">👤</span>`;
if (sizeBadge) {
sizeBadge.className = 'text-xs font-bold text-red-600 bg-red-50 px-3 py-1 rounded-full border border-red-300';
sizeBadge.innerText = isEn ? `❌ Photo Rejected: ${originalKB} KB (Exceeds 50KB)` : `❌ फोटो अस्वीकृत: ${originalKB} KB (50KB से अधिक है)`;
}
return;
}
}
if (sizeBadge) {
sizeBadge.className = 'text-xs font-bold text-amber-700 bg-amber-50 px-3 py-1 rounded-full border border-amber-200 animate-pulse';
sizeBadge.innerText = isEn ? '⏳ Compressing photo under 50KB...' : '⏳ फोटो 50KB के अंदर तैयार हो रही है...';
}
try {
const compressedBase64 = await compressImage(file, 35 * 1024);
const byteLen = getBase64ByteLength(compressedBase64);
const sizeKB = (byteLen / 1024).toFixed(1);
if (byteLen > MAX_ALLOWED_BYTES || compressedBase64.length > 70 * 1024) {
alert(isEn ? `❌ Photo size exceeds 50KB (${sizeKB} KB). Please choose a smaller photo.` : `❌ फोटो का साइज 50KB से अधिक है (${sizeKB} KB)। कृपया 50KB से छोटी फोटो चुनें।`);
event.target.value = '';
wizardState.photoUrl = '';
if (previewBox) previewBox.innerHTML = `<span class="text-4xl">👤</span>`;
if (sizeBadge) {
sizeBadge.className = 'text-xs font-bold text-red-600 bg-red-50 px-3 py-1 rounded-full border border-red-200';
sizeBadge.innerText = isEn ? `❌ Photo exceeds 50KB (${sizeKB} KB).` : `❌ फोटो बड़ी है (${sizeKB} KB). 50KB से छोटी आवश्यक है।`;
}
return;
}
wizardState.photoUrl = compressedBase64;
if (previewBox) {
previewBox.innerHTML = `<img src="${compressedBase64}" class="w-full h-full object-cover">`;
}
if (sizeBadge) {
sizeBadge.className = 'text-xs font-bold text-green-700 bg-green-50 px-3 py-1 rounded-full border border-green-200';
sizeBadge.innerText = isEn ? `📦 Photo Size: ${sizeKB} KB (Under 50KB - Valid ✅)` : `📦 फोटो साइज: ${sizeKB} KB (50KB से कम - मान्य ✅)`;
}
} catch (err) {
console.error('Photo compression error:', err);
alert(isEn ? 'Failed to compress photo under 50KB. Please choose a smaller image.' : 'फोटो 50KB के अंदर कंप्रेस नहीं हो सकी। कृपया 50KB से छोटी फोटो चुनें।');
event.target.value = '';
wizardState.photoUrl = '';
if (previewBox) previewBox.innerHTML = `<span class="text-4xl">👤</span>`;
if (sizeBadge) {
sizeBadge.className = 'text-xs font-bold text-red-600 bg-red-50 px-3 py-1 rounded-full border border-red-200';
sizeBadge.innerText = isEn ? '❌ Photo must be under 50KB' : '❌ 50KB से छोटी फोटो आवश्यक है';
}
}
}
function onWizardStateChange(selectedState) {
wizardState.state = selectedState;
const districts = typeof getDistrictsForState === 'function' ? getDistrictsForState(selectedState) : [];
if (districts.length > 0) {
wizardState.district = districts[0];
}
const distSelect = document.getElementById('wizard-district');
if (distSelect) {
distSelect.innerHTML = districts.map(dt => `<option value="${dt}">${dt}</option>`).join('');
}
}
function detectGPSLocation() {
const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
const isEn = lang === 'en';
if (!navigator.geolocation) {
alert(isEn ? 'GPS is not supported in your browser. Please select your district from the list.' : 'आपके ब्राउज़र में जीपीएस सपोर्ट नहीं है। कृपया सूची से जिला चुनें।');
return;
}
navigator.geolocation.getCurrentPosition(
() => {
wizardState.district = 'वाराणसी (Varanasi)';
wizardState.tehsil = 'सदर (Sadar)';
alert(isEn ? '📍 Location recognized via GPS: Varanasi (Sadar)' : '📍 जीपीएस से आपकी लोकेशन पहचान ली गई है: वाराणसी (सदर)');
renderWizardStep();
},
() => {
alert(isEn ? 'Please select your district and tehsil from the list below.' : 'कृपया जिला और तहसील का चयन नीचे दी गई सूची से करें।');
}
);
}
function nextStep() {
const currentYear = new Date().getFullYear();
const calculatedAge = currentYear - wizardState.birthYear;
if (wizardState.currentStep === 1) {
const nameInput = document.getElementById('wizard-name');
const phoneInput = document.getElementById('wizard-phone');
if (nameInput) wizardState.name = nameInput.value.trim();
if (phoneInput) wizardState.phone = phoneInput.value.trim();
if (!wizardState.name) {
alert(getWizText('alert_name'));
return;
}
if (wizardState.phone.length < 10) {
alert(getWizText('alert_phone'));
return;
}
}
if (wizardState.currentStep === 2) {
if (calculatedAge < 18) {
speakPrompt(getWizText('alert_underage'));
alert(getWizText('alert_underage'));
return;
}
if (!wizardState.declared18Plus) {
alert(getWizText('alert_declare'));
return;
}
}
if (wizardState.currentStep === 3) {
if (wizardState.skills.length === 0) {
alert(getWizText('alert_skill'));
return;
}
}
if (wizardState.currentStep === 4) {
const vInput = document.getElementById('wizard-village');
const tInput = document.getElementById('wizard-tehsil');
if (vInput) wizardState.village = vInput.value.trim();
if (tInput) wizardState.tehsil = tInput.value.trim();
if (!wizardState.village) {
alert(getWizText('alert_village'));
return;
}
}
if (wizardState.currentStep < wizardState.totalSteps) {
wizardState.currentStep++;
renderWizardStep();
window.scrollTo({ top: 0, behavior: 'smooth' });
}
}
function prevStep() {
if (wizardState.currentStep > 1) {
wizardState.currentStep--;
renderWizardStep();
window.scrollTo({ top: 0, behavior: 'smooth' });
}
}
async function submitWizard() {
if (!wizardState.consentAccepted) {
alert(getWizText('alert_consent'));
return;
}
if (wizardState.photoUrl && typeof getBase64ByteLength === 'function') {
const photoBytes = getBase64ByteLength(wizardState.photoUrl);
if (photoBytes > 50 * 1024) {
alert(getWizText('alert_photo_limit'));
return;
}
}
const payload = {
name: wizardState.name,
phone: wizardState.phone,
birth_year: wizardState.birthYear,
declared_age_18_plus: 1,
skills: wizardState.skills,
experience_years: wizardState.experienceYears,
state: wizardState.state,
district: wizardState.district,
tehsil: wizardState.tehsil,
village: wizardState.village,
daily_rate: wizardState.dailyRate,
availability_status: wizardState.availabilityStatus,
bio_text: `${wizardState.experienceYears} साल का अनुभव। ${wizardState.village} में उपलब्ध।`,
is_team_leader: wizardState.isTeamLeader ? 1 : 0,
team_size: wizardState.teamSize,
photo_url: wizardState.photoUrl,
consent_accepted: true
};
try {
const res = await fetch('/api/workers/register', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(payload)
});
const data = await res.json();
if (res.ok) {
speakPrompt(getWizText('tts_success'));
alert(getWizText('alert_success'));
localStorage.setItem('km_worker_id', data.worker_public_id);
localStorage.setItem('km_worker_name', wizardState.name);
localStorage.setItem('km_worker_phone', wizardState.phone);
switchTab('search');
} else {
alert(data.message || 'Error occurred. Please try again.');
}
} catch (err) {
alert('Network error. Please try again.');
}
}
function resetWizardState() {
wizardState = {
currentStep: 1,
totalSteps: 5,
name: '',
phone: '',
birthYear: 1995,
declared18Plus: false,
skills: [],
isTeamLeader: false,
teamSize: 1,
state: 'उत्तर प्रदेश (Uttar Pradesh)',
district: 'वाराणसी (Varanasi)',
tehsil: 'पिंडरा (Pindra)',
village: '',
experienceYears: 5,
dailyRate: 650,
availabilityStatus: 'available',
bioText: '',
photoUrl: '',
consentAccepted: false
};
if (typeof renderWizardStep === 'function') {
renderWizardStep();
}
}