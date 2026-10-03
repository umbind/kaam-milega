const ST = {
  hi: 'सभी|टॉप रेटेड|सत्यापित|टोली ठेकेदार|तुरंत उपलब्ध|शेयर करें|पंचायत व साथियों द्वारा सत्यापित|लोगों की टोली (टीम लीडर)|संभावित मासिक कमाई:|/माह तक',
  bho: 'सभ|टॉप रेटेड|जाँचल गइल|टोली ठेकेदार|तुरंत उपलब्ध|शेयर करीं|पंचायत आ साथी लोगन से जाँचल|लोग के टोली (टीम लीडर)|अनुमानित महीना के कमाई:|/महीना तक',
  en: 'All|Top Rated|Verified|Team Leader|Available Now|Share|Panchayat & Peer Verified|person crew (Team Leader)|Est. Monthly Earnings:|/mo max',
  bn: 'সব|শীর্ষ রেটযুক্ত|যাচাইকৃত|টিম লিডার|এখনই উপলব্ধ|শেয়ার করুন|পঞ্চায়েত ও সহকর্মী দ্বারা যাচাইকৃত|জনের দল (টিম লিডার)|আনুমানিক মাসিক আয়:|/মাস পর্যন্ত',
  mr: 'सर्व|अव्वल दर्जा|पडताळणीकृत|टीम लीडर|लगेच उपलब्ध|शेअर करा|पंचायत व सहकाऱ्यांद्वारे पडताळणीकृत|जणांचा संघ (टीम लीडर)|अंदाजे मासिक कमाई:|/महिना पर्यंत',
  te: 'అన్నీ|టాప్ రేటెడ్|ధృవీకరించబడింది|టీమ్ లీడర్|వెంటనే అందుబాటులో|షేర్ చేయండి|పంచాయతీ & తోటివారిచే ధృవీకరించబడింది|మంది బృందం (టీమ్ లీడర్)|అంచనా నెలవారీ ఆదాయం:|/నెలకు గరిష్టం',
  ta: 'அனைத்தும்|சிறந்த தொழிலாளி|சரிபார்க்கப்பட்டது|குழு தலைவர்|இப்போது கிடைக்கும்|பகிர்|பஞ்சாயத்து & சகாக்களால் சரிபார்க்கப்பட்டது|பேர் கொண்ட குழு (குழு தலைவர்)|மதிப்பிடப்பட்ட மாதாந்திர வருமானம்:|/மாதம் வரை',
  kn: 'ಎಲ್ಲಾ|ಉನ್ನತ ಶ್ರೇಣಿ|ಪರಿಶೀಲಿಸಲಾಗಿದೆ|ತಂಡದ ನಾಯಕ|ತಕ್ಷಣ ಲಭ್ಯವಿದೆ|ಹಂಚಿಕೊಳ್ಳಿ|ಪಂಚಾಯತ್ & ಸಹೋದ್ಯೋಗಿಗಳಿಂದ ಪರಿಶೀಲಿಸಲಾಗಿದೆ|ಜನರ ತಂಡ (ತಂಡದ ನಾಯಕ)|ಅಂದಾಜು ಮಾಸಿಕ ಗಳಿಕೆ:|/ತಿಂಗಳಿಗೆ ಗರಿಷ್ಠ',
  gu: 'બધા|ટોપ રેટેડ|ચકાસાયેલ|ટીમ લીડર|તરત ઉપલબ્ધ|શેર કરો|પંચાયત અને સાથીઓ દ્વારા ચકાસાયેલ|લોકોની ટીમ (ટીમ લીડર)|સંભવિત માસિક કમાણી:|/મહિના સુધી',
  pa: 'ਸਾਰੇ|ਟੌਪ ਰੇਟਿਡ|ਤਸਦੀਕਸ਼ੁਦਾ|ਟੀਮ ਲੀਡਰ|ਤੁਰੰਤ ਉਪਲਬਧ|ਸਾਂਝਾ ਕਰੋ|ਪੰਚਾਇਤ ਅਤੇ ਸਾਥੀਆਂ ਵੱਲੋਂ ਤਸਦੀਕਸ਼ੁਦਾ|ਜਣਿਆਂ ਦੀ ਟੀਮ (ਟੀਮ ਲੀਡਰ)|ਅਨੁਮਾਨਿਤ ਮਹੀਨਾਵਾਰ ਕਮਾਈ:|/ਮਹੀਨਾ ਤੱਕ',
  or: 'ସମସ୍ତ|ଶ୍ରେଷ୍ଠ କାରିଗର|ଯାଞ୍ଚ ହୋଇଛି|ଟିମ୍ ଲିଡର୍|ତୁରନ୍ତ ଉପଲବ୍ଧ|ସେୟାର କରନ୍ତୁ|ପଞ୍ଚାୟତ ଓ ସାଥୀଙ୍କ ଦ୍ୱାରା ଯାଞ୍ଚ ହୋଇଛି|ଜଣିଆ ଟିମ୍ (ଟିମ୍ ଲିଡର୍)|ଆନୁମାନିକ ମାସିକ ଆୟ:|/ମାସ ପର୍ଯ୍ୟନ୍ତ',
  ml: 'എല്ലാം|മികച്ച റേറ്റഡ്|സ്ഥിരീകരിച്ചു|ടീം ലീഡർ|ഇപ്പോൾ ലഭ്യമാണ്|ഷെയർ ചെയ്യുക|പഞ്ചായത്തും സഹപ്രവർത്തകരും സാക്ഷ്യപ്പെടുത്തിയത്|പേരടങ്ങുന്ന സംഘം (ടീം ലീഡർ)|പ്രതീക്ഷിക്കുന്ന പ്രതിമാസ വരുമാനം:|/മാസം വരെ'
};
function getSearchI18n(l) { return (ST[l] || ST.hi).split('|'); }
function updateTrustFilterLabels(l) {
  const [all, top, ver, ldr, avail] = getSearchI18n(l);
  const setOpt = (val, txt) => {
    const opt = document.querySelector(`#filter-trust option[value="${val}"]`);
    if (opt) opt.innerText = txt;
  };
  setOpt('all', all ? (all + ' (All Workers)') : 'सभी कारीगर (All Workers)');
  setOpt('top_rated', '⭐ ' + top);
  setOpt('verified', '✅ ' + ver);
  setOpt('team_leader', '👥 ' + ldr);
  setOpt('available', '🟢 ' + avail);
}

let activeTradeFilter = 'all';
let activeStateFilter = 'all';
let activeDistrictFilter = 'all';
let activeStatusFilter = 'all';
let activeTrustFilter = 'all';
let allLoadedWorkers = [];
const STANDARD_TRADES = [
{ key: 'all', defaultName: 'सभी काम व चालक' },
{ key: 'halwai', defaultName: 'हलवाई (मिठाई कारीगर) 🍯' },
{ key: 'event_cook', defaultName: 'शादी-विवाह भोजन कारीगर 👨‍🍳' },
{ key: 'catering_helper', defaultName: 'केटरिंग व वेटर सेवा 🍽️' },
{ key: 'tent_decorator', defaultName: 'टेंट व लाइट कारीगर 🎪' },
{ key: 'auto_driver', defaultName: 'ऑटो चालक 🛺' },
{ key: 'erickshaw_driver', defaultName: 'ई-रिक्शा चालक 🛺⚡' },
{ key: 'pickup_driver', defaultName: 'पिकअप चालक 🛻' },
{ key: 'car_driver', defaultName: 'कार/टैक्सी 🚗' },
{ key: 'tractor_driver', defaultName: 'ट्रैक्टर 🚜' },
{ key: 'mason', defaultName: 'राजमिस्त्री 🧱' },
{ key: 'plumber', defaultName: 'प्लंबर 🔧' },
{ key: 'electrician', defaultName: 'इलेक्ट्रीशियन ⚡' },
{ key: 'boring', defaultName: 'बोरिंग लेबर 🪠' },
{ key: 'carpenter', defaultName: 'बढ़ई 🪚' },
{ key: 'painter', defaultName: 'पेंटर 🎨' },
{ key: 'welder', defaultName: 'वेल्डर 👨‍🏭' },
{ key: 'labor', defaultName: 'दिहाड़ी मज़दूर 🔨' }
];
const TRADE_NAMES = Object.fromEntries(STANDARD_TRADES.map(t => [t.key, t.defaultName]));
function getLocalizedTradeName(key) {
const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
if (typeof I18N_DATA !== 'undefined' && I18N_DATA[lang]) {
const dict = I18N_DATA[lang];
if (key === 'all') return dict.all_trades || 'सभी काम व चालक';
if (dict.trades && dict.trades[key]) return dict.trades[key];
}
return TRADE_NAMES[key] || key;
}
function getCustomCategories() {
try {
const raw = localStorage.getItem('km_custom_categories');
return raw ? JSON.parse(raw) : [];
} catch (e) {
return [];
}
}
function addCustomCategory(name) {
name = (name || '').trim();
if (!name || name.length < 2) return false;
const cats = getCustomCategories();
if (!cats.includes(name)) {
cats.push(name);
localStorage.setItem('km_custom_categories', JSON.stringify(cats));
}
return true;
}
let addCategoryContext = 'search';
function openAddCategoryModal(context = 'search') {
addCategoryContext = context;
const modal = document.getElementById('add-category-modal');
const input = document.getElementById('custom-category-input');
if (input) input.value = '';
if (modal) {
modal.classList.remove('hidden');
modal.style.display = 'flex';
}
setTimeout(() => { if (input) input.focus(); }, 100);
}
function closeAddCategoryModal() {
const modal = document.getElementById('add-category-modal');
if (modal) {
modal.classList.add('hidden');
modal.style.display = 'none';
}
}
function saveCustomCategory() {
const input = document.getElementById('custom-category-input');
let name = (input ? input.value : '').trim().replace(/\s+/g, ' ');
const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
const isEn = lang === 'en';
if (!name || name.length < 2) {
alert(isEn ? 'Please enter at least 2 characters for the skill name.' : 'कृपया कम से कम 2 अक्षरों का काम या हुनर का नाम लिखें।');
return;
}
if (name.length > 25) {
alert(isEn ? 'Skill name cannot exceed 25 characters.' : 'हुनर का नाम 25 अक्षरों से अधिक नहीं हो सकता।');
return;
}
if (/\d/.test(name)) {
alert(isEn
? '❌ Numbers or phone numbers are strictly prohibited in skill names. Please enter only the trade name.'
: '❌ हुनर के नाम में संख्याएं या फोन नंबर सख्त मना हैं। कृपया केवल काम या हुनर का नाम लिखें।');
return;
}
if (/\.com|\.in|\.org|\.net|http|www|@|\.co/i.test(name)) {
alert(isEn ? '❌ Website links or emails are not allowed.' : '❌ वेबसाइट लिंक या ईमेल पता मान्य नहीं है।');
return;
}
const badWords = ['loan', 'credit', 'finance', 'betting', 'casino', 'satta', 'lottery', 'sex', 'escort', 'callgirl', 'adult', 'massage', 'drugs', 'ganja', 'sharab', 'weapon', 'gun', 'hacker', 'crypto'];
const lower = name.toLowerCase();
for (const bw of badWords) {
if (new RegExp('\\b' + bw + '\\b', 'i').test(lower)) {
alert(isEn ? `❌ Prohibited or inappropriate term: "${bw}"` : `❌ प्रतिबंधित या अमान्य शब्द: "${bw}"`);
return;
}
}
const validRegex = /^[a-zA-Z\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0A80-\u0AFF\u0B00-\u0B7F\u0B80-\u0BFF\u0C00-\u0C7F\u0C80-\u0CFF\u0D00-\u0D7F\s\-]{2,25}$/;
if (!validRegex.test(name)) {
alert(isEn
? '❌ Skill name can only contain letters (English or Indic) and spaces.'
: '❌ हुनर के नाम में केवल अक्षर (हिंदी, अंग्रेजी या स्थानीय भाषा) और स्पेस मान्य हैं।');
return;
}
addCustomCategory(name);
closeAddCategoryModal();
if (addCategoryContext === 'search') {
renderTradeFilterPills();
setTradeFilter(name);
} else if (addCategoryContext === 'wizard') {
if (typeof wizardState !== 'undefined') {
if (!wizardState.skills.includes(name)) {
wizardState.skills.push(name);
}
if (typeof renderWizardStep === 'function') renderWizardStep();
}
}
if (typeof speakPrompt === 'function') {
speakPrompt(isEn ? `New skill "${name}" added successfully.` : `नया हुनर ${name} जोड़ दिया गया है।`);
}
}
function renderTradeDropdown() {
  const select = document.getElementById('filter-trade');
  if (!select) return;
  const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
  const dict = (typeof I18N_DATA !== 'undefined' && I18N_DATA[lang]) ? I18N_DATA[lang] : (I18N_DATA['hi'] || {});
  const customCats = getCustomCategories();

  let optionsHtml = '';
  // 1. All trades
  const allLabel = dict.all_trades || 'सभी काम व चालक (All Trades)';
  optionsHtml += `<option value="all">${allLabel}</option>`;

  // 2. Standard trades
  STANDARD_TRADES.filter(t => t.key !== 'all').forEach(t => {
    const label = ((dict.trades && dict.trades[t.key]) || t.defaultName);
    optionsHtml += `<option value="${t.key}">${label}</option>`;
  });

  // 3. Custom categories
  if (customCats.length > 0) {
    customCats.forEach(cat => {
      optionsHtml += `<option value="${cat}">🛠️ ${cat}</option>`;
    });
  }

  // 4. Add new skill action
  const addPrompt = dict.btn_add_category || '➕ नया काम / हुनर जोड़ें (Add Skill)...';
  optionsHtml += `<option value="_add_new_">${addPrompt}</option>`;

  select.innerHTML = optionsHtml;
  select.value = activeTradeFilter;
}

function renderTradeFilterPills() {
  renderTradeDropdown();
}

function handleTradeDropdownChange(val) {
  if (val === '_add_new_') {
    const select = document.getElementById('filter-trade');
    if (select) select.value = activeTradeFilter;
    openAddCategoryModal('search');
    return;
  }
  setTradeFilter(val);
}

function highlightActiveFilters() {
  const isAnyActive = activeTradeFilter !== 'all' || activeTrustFilter !== 'all' ||
                      activeStateFilter !== 'all' || activeDistrictFilter !== 'all' ||
                      activeStatusFilter !== 'all';

  const resetBtn = document.getElementById('btn-reset-filters');
  if (resetBtn) {
    if (isAnyActive) {
      resetBtn.classList.remove('text-slate-500', 'border-transparent');
      resetBtn.classList.add('text-red-700', 'bg-red-50', 'border-red-300', 'font-black');
    } else {
      resetBtn.classList.remove('text-red-700', 'bg-red-50', 'border-red-300', 'font-black');
      resetBtn.classList.add('text-slate-500', 'border-transparent');
    }
  }

  const markSelect = (id, active) => {
    const el = document.getElementById(id);
    if (!el) return;
    if (active) {
      el.classList.add('border-green-600', 'bg-green-50/50', 'text-green-950');
      el.classList.remove('border-slate-300', 'bg-white');
    } else {
      el.classList.remove('border-green-600', 'bg-green-50/50', 'text-green-950');
      el.classList.add('border-slate-300', 'bg-white');
    }
  };

  markSelect('filter-trade', activeTradeFilter !== 'all');
  markSelect('filter-trust', activeTrustFilter !== 'all');
  markSelect('filter-state', activeStateFilter !== 'all');
  markSelect('filter-district', activeDistrictFilter !== 'all');
  markSelect('filter-status', activeStatusFilter !== 'all');
}

function resetAllFilters() {
  activeTradeFilter = 'all';
  activeTrustFilter = 'all';
  activeStateFilter = 'all';
  activeDistrictFilter = 'all';
  activeStatusFilter = 'all';

  const tSel = document.getElementById('filter-trade');
  if (tSel) tSel.value = 'all';
  const trSel = document.getElementById('filter-trust');
  if (trSel) trSel.value = 'all';
  const sSel = document.getElementById('filter-state');
  if (sSel) sSel.value = 'all';
  const dSel = document.getElementById('filter-district');
  if (dSel) {
    dSel.innerHTML = '<option value="all">सभी जिले (All Districts)</option>';
    dSel.value = 'all';
  }
  const stSel = document.getElementById('filter-status');
  if (stSel) stSel.value = 'all';

  highlightActiveFilters();
  loadWorkers();

  if (typeof speakPrompt === 'function') {
    const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
    const isEn = lang === 'en';
    speakPrompt(isEn ? 'All filters reset.' : 'सभी फ़िल्टर साफ़ कर दिए गए हैं।');
  }
}

function initSearchFilters() {
  renderTradeDropdown();
  updateTrustFilterLabels(typeof currentLang !== 'undefined' ? currentLang : 'hi');
  const stateSelect = document.getElementById('filter-state');
  if (stateSelect && stateSelect.children.length <= 1 && typeof getIndiaStates === 'function') {
    const states = getIndiaStates();
    const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
    const dict = (typeof I18N_DATA !== 'undefined' && I18N_DATA[lang]) ? I18N_DATA[lang] : {};
    const allStatesLabel = dict.all_states || 'अखिल भारतीय (All India)';
    stateSelect.innerHTML = `<option value="all">${allStatesLabel}</option>` +
      states.map(s => `<option value="${s}">${s}</option>`).join('');
    if (activeStateFilter !== 'all') stateSelect.value = activeStateFilter;
  }
  highlightActiveFilters();
}

function setTrustFilter(filter) {
  activeTrustFilter = filter;
  const select = document.getElementById('filter-trust');
  if (select && select.value !== filter) {
    select.value = filter;
  }
  highlightActiveFilters();
  loadWorkers();
}
let isVoiceListening = false;
let speechRecognitionInstance = null;
function startVoiceSearch() {
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (!SpeechRecognition) {
alert('आपके ब्राउज़र में आवाज़ पहचान (Voice Search) सुविधा उपलब्ध नहीं है। कृपया गूगल क्रोम का उपयोग करें अथवा फ़िल्टर से चुनें।');
return;
}
const micBtn = document.getElementById('voice-search-btn');
const micStatus = document.getElementById('voice-status-text');
if (isVoiceListening && speechRecognitionInstance) {
speechRecognitionInstance.stop();
return;
}
try {
const recognition = new SpeechRecognition();
speechRecognitionInstance = recognition;
recognition.lang = (typeof currentLang !== 'undefined' && currentLang === 'en') ? 'en-IN' : 'hi-IN';
recognition.interimResults = false;
recognition.maxAlternatives = 1;
recognition.onstart = () => {
isVoiceListening = true;
if (micBtn) {
micBtn.classList.add('animate-pulse', '!bg-red-600', '!text-white');
}
if (micStatus) {
micStatus.innerText = '🔴 सुन रहे हैं... बोलिए जैसे "हलवाई" या "ड्राइवर"';
micStatus.classList.remove('hidden');
}
};
recognition.onresult = (event) => {
const transcript = event.results[0][0].transcript.toLowerCase();
if (micStatus) micStatus.innerText = `🗣️ आपने कहा: "${transcript}"`;
const tradeMap = {
'हलवाई': 'halwai',
'मिठाई': 'halwai',
'कुक': 'event_cook',
'खाना': 'event_cook',
'रसोइया': 'event_cook',
'केटरिंग': 'catering_helper',
'वेटर': 'catering_helper',
'टेंट': 'tent_decorator',
'लाइट': 'tent_decorator',
'ऑटो': 'auto_driver',
'रिक्शा': 'erickshaw_driver',
'पिकअप': 'pickup_driver',
'गाड़ी': 'car_driver',
'ड्राइवर': 'car_driver',
'टैक्सी': 'car_driver',
'ट्रैक्टर': 'tractor_driver',
'मिस्त्री': 'mason',
'राजमिस्त्री': 'mason',
'प्लंबर': 'plumber',
'नल': 'plumber',
'इलेक्ट्रीशियन': 'electrician',
'बिजली': 'electrician',
'बोरिंग': 'boring',
'बढ़ई': 'carpenter',
'लकड़ी': 'carpenter',
'पेंटर': 'painter',
'रंग': 'painter',
'वेल्डर': 'welder',
'मजदूर': 'labor',
'लेबर': 'labor'
};
let matchedKey = null;
for (const [kw, key] of Object.entries(tradeMap)) {
if (transcript.includes(kw)) {
matchedKey = key;
break;
}
}
if (matchedKey) {
setTradeFilter(matchedKey);
if (typeof speakPrompt === 'function') {
speakPrompt(`${transcript} के लिए खोज रहे हैं।`);
}
} else {
const customCats = getCustomCategories();
const foundCustom = customCats.find(c => transcript.includes(c.toLowerCase()));
if (foundCustom) {
setTradeFilter(foundCustom);
} else {
loadWorkers();
}
}
};
recognition.onerror = (event) => {
console.log('Voice recognition error:', event.error);
if (micStatus) micStatus.innerText = 'आवाज नहीं पहचानी जा सकी। कृपया पुनः बोलें।';
};
recognition.onend = () => {
isVoiceListening = false;
if (micBtn) {
micBtn.classList.remove('animate-pulse', '!bg-red-600', '!text-white');
}
setTimeout(() => {
if (micStatus && !isVoiceListening) micStatus.classList.add('hidden');
}, 3500);
};
recognition.start();
} catch (e) {
console.error('Voice search start error:', e);
}
}
function getSkeletonCardsHtml(count = 4) {
  let skeletons = '';
  for (let i = 0; i < count; i++) {
    skeletons += `
    <div class="card-elevation bg-white rounded-2xl p-5 border border-slate-100 flex flex-col justify-between">
      <div>
        <div class="flex items-center gap-3 mb-4">
          <div class="w-14 h-14 rounded-full skeleton-box flex-shrink-0"></div>
          <div class="flex-1 space-y-2">
            <div class="w-3/4 h-5 skeleton-box rounded-md"></div>
            <div class="w-1/2 h-3.5 skeleton-box rounded-md"></div>
          </div>
        </div>
        <div class="flex gap-2 mb-4">
          <div class="w-20 h-6 skeleton-box rounded-md"></div>
          <div class="w-16 h-6 skeleton-box rounded-md"></div>
        </div>
        <div class="w-full h-12 skeleton-box rounded-xl mb-4"></div>
      </div>
      <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100">
        <div class="h-11 skeleton-box rounded-xl"></div>
        <div class="h-11 skeleton-box rounded-xl"></div>
      </div>
    </div>`;
  }
  return skeletons;
}

async function loadWorkers() {
  initSearchFilters();
  const container = document.getElementById('workers-grid');
  if (!container) return;
  const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
  const dict = (typeof I18N_DATA !== 'undefined' && I18N_DATA[lang]) ? I18N_DATA[lang] : (I18N_DATA['hi'] || {});
  
  // Render animated skeleton loaders immediately for 0 Cumulative Layout Shift (CLS)
  container.innerHTML = getSkeletonCardsHtml(4);
  
  let url = `/api/workers?skill=${encodeURIComponent(activeTradeFilter)}&state=${encodeURIComponent(activeStateFilter)}&district=${encodeURIComponent(activeDistrictFilter)}&status=${encodeURIComponent(activeStatusFilter)}&trust_filter=${encodeURIComponent(activeTrustFilter)}`;
  try {
    const res = await fetch(url);
    const data = await res.json();
    allLoadedWorkers = data.workers || [];
    renderWorkerCards(allLoadedWorkers);
  } catch (err) {
    container.innerHTML = `
      <div class="col-span-full py-8 text-center text-red-600 font-bold bg-red-50 rounded-2xl border border-red-200 p-6">
        <span class="text-3xl block mb-2">⚠️</span>
        <p class="text-base mb-2">कारीगर लोड करने में समस्या हुई। कृपया इंटरनेट कनेक्शन जांचें।</p>
        <button onclick="loadWorkers()" class="mt-2 px-4 py-2 bg-red-600 text-white rounded-xl font-bold text-sm touch-scale">पुनः प्रयास करें</button>
      </div>
    `;
  }
}

function renderWorkerCards(workers) {
  const container = document.getElementById('workers-grid');
  const countBadge = document.getElementById('worker-count-badge');
  const lang = (typeof currentLang !== 'undefined') ? currentLang : 'hi';
  const dict = (typeof I18N_DATA !== 'undefined' && I18N_DATA[lang]) ? I18N_DATA[lang] : (I18N_DATA['hi'] || {});
  const [t_all, t_top, t_ver, t_ldr, t_avail, t_share, t_panchayat, t_crew, t_earn, t_max] = getSearchI18n(lang);
  
  if (countBadge) countBadge.innerText = `${workers.length} ${dict.workers_found || 'कारीगर मिले'}`;
  
  if (workers.length === 0) {
    container.innerHTML = `
      <div class="col-span-full bg-white p-8 rounded-2xl text-center border-2 border-dashed border-slate-300 card-elevation">
        <span class="text-5xl mb-3 block">🔍</span>
        <h3 class="text-xl font-black text-slate-800 mb-1">${dict.no_workers_found || 'कोई कारीगर नहीं मिला'}</h3>
        <p class="text-slate-500 text-sm mb-4">${dict.no_workers_sub || 'कृपया फ़िल्टर बदलें या किसी अन्य जिले में खोजें।'}</p>
        <button onclick="resetAllFilters()" class="px-5 py-2.5 bg-green-700 text-white rounded-xl font-bold text-sm touch-scale shadow-sm">फ़िल्टर रीसेट करें</button>
      </div>
    `;
    return;
  }
  
  container.innerHTML = workers.map(w => {
    let statusClass = 'status-available';
    let statusText = dict.available || '🟢 उपलब्ध';
    let dotColor = 'bg-emerald-500';
    if (w.availability_status === 'busy') {
      statusClass = 'status-busy';
      statusText = dict.busy || '🔴 व्यस्त';
      dotColor = 'bg-rose-500';
    } else if (w.availability_status === 'seasonal_dormancy') {
      statusClass = 'status-dormancy';
      statusText = dict.dormancy || '🌾 खेती/छुट्टी पर';
      dotColor = 'bg-amber-500';
    }

    let tierBadge = '';
    if (w.verification_tier === 'tier3') {
      tierBadge = `<span class="inline-flex items-center gap-1 bg-gradient-to-r from-amber-50 to-amber-100 text-amber-900 border border-amber-300 text-xs px-2.5 py-0.5 rounded-full font-black shadow-sm">🥇 ${t_panchayat}</span>`;
    } else if (w.verification_tier === 'tier2') {
      tierBadge = `<span class="inline-flex items-center gap-1 bg-gradient-to-r from-blue-50 to-indigo-50 text-indigo-900 border border-blue-200 text-xs px-2.5 py-0.5 rounded-full font-black shadow-sm">🥈 सहकर्मी प्रमाणित</span>`;
    } else if (w.is_verified) {
      tierBadge = `<span class="inline-flex items-center gap-1 bg-gradient-to-r from-emerald-50 to-green-50 text-green-900 border border-green-300 text-xs px-2.5 py-0.5 rounded-full font-black shadow-sm">🥉 ${t_ver}</span>`;
    }

    const topRatedBadge = (w.is_top_rated || w.rating_avg >= 4.5)
      ? `<span class="inline-flex items-center gap-0.5 bg-amber-100 text-amber-900 border border-amber-300 text-xs px-2 py-0.5 rounded-full font-black">⭐ ${t_top}</span>`
      : '';

    const tradePills = w.skills.map(s => {
      return `<span class="bg-slate-100 text-slate-800 text-xs px-2.5 py-1 rounded-lg font-bold border border-slate-200/60">${getLocalizedTradeName(s)}</span>`;
    }).join(' ');

    const callText = dict.btn_call || '📞 कॉल करें';
    const waText = dict.btn_whatsapp || '💬 WhatsApp';
    const slipText = dict.btn_work_slip || '📋 काम की पर्ची बनाएँ';
    const reportText = dict.btn_report || '⚠️ रिपोर्ट करें';
    const dailyWageLabel = dict.daily_wage || 'रोज की दिहाड़ी';
    const perDayLabel = dict.per_day || '/दिन';
    const expLabel = dict.experience || 'साल अनुभव';

    const earnabilityBadge = w.estimated_monthly_earnings
      ? `<div class="mb-3 px-3 py-1.5 bg-emerald-50 text-emerald-900 border border-emerald-200 rounded-xl text-xs font-extrabold flex items-center justify-between">
          <span class="flex items-center gap-1"><span>💰</span> ${t_earn}</span>
          <span class="text-emerald-800 font-black">₹${w.estimated_monthly_earnings.toLocaleString('en-IN')}${t_max}</span>
        </div>`
      : '';

    return `
    <div class="card-elevation bg-white rounded-2xl border border-slate-200/90 overflow-hidden flex flex-col justify-between transition-all duration-200">
      <div class="p-5 flex-1">
        <div class="flex items-start gap-3.5 mb-3.5">
          <div class="relative w-14 h-14 rounded-full bg-slate-100 border-2 border-emerald-600 overflow-hidden flex-shrink-0 flex items-center justify-center">
            <img src="${w.photo_url || '/static/images/icons/mason.svg'}" class="w-full h-full object-cover" alt="${w.name}" loading="lazy" onerror="this.src='/static/images/icons/mason.svg'">
            <span class="absolute bottom-0 right-0 ${dotColor} w-3.5 h-3.5 rounded-full border-2 border-white ring-1 ring-black/5" title="${statusText}"></span>
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1 flex-wrap">
              <h3 class="text-lg font-black text-slate-900 truncate tracking-tight">${w.name}</h3>
              <button type="button" class="speak-btn !w-6 !h-6 !text-xs touch-scale" onclick="speakPrompt('${w.name}, ${w.village}, रोज की दिहाड़ी ₹${w.daily_rate}', this)" aria-label="कारीगर का विवरण सुनें" title="कारीगर का विवरण सुनें">🔊</button>
              ${topRatedBadge}
            </div>
            <p class="text-xs text-slate-600 mb-1.5 flex items-center gap-1 font-semibold truncate">
              <span>📍</span> ${w.village}, ${w.district}
            </p>
            ${tierBadge}
          </div>
        </div>

        <div class="flex flex-wrap gap-1.5 mb-3">
          ${tradePills}
          <span class="bg-blue-50 text-blue-800 text-xs px-2 py-1 rounded-lg font-bold border border-blue-200/60">
            ${w.experience_years} ${expLabel}
          </span>
          ${w.is_team_leader ? `<span class="bg-purple-100 text-purple-900 text-xs px-2 py-1 rounded-lg font-bold border border-purple-200/60">👥 ${w.team_size} ${t_crew}</span>` : ''}
        </div>

        ${earnabilityBadge}

        <div class="flex items-center justify-between py-2.5 px-3 bg-slate-50/80 rounded-xl border border-slate-100 mb-3">
          <div>
            <span class="text-[11px] text-slate-500 font-bold block uppercase tracking-wide">${dailyWageLabel}</span>
            <div class="flex items-baseline gap-1">
              <strong class="text-2xl font-black text-green-800">₹${w.daily_rate}</strong>
              <span class="text-xs text-slate-500 font-medium">${perDayLabel}</span>
            </div>
          </div>
          <div class="text-right">
            <span class="${statusClass} status-pill mb-1 inline-block">${statusText}</span>
            <div class="text-xs text-slate-600 font-bold">
              ⭐ ${w.rating_avg} <span class="text-slate-400 font-medium">(${w.review_count})</span>
            </div>
          </div>
        </div>

        ${w.bio_text ? `<p class="text-xs text-slate-600 line-clamp-2 mb-3 italic font-medium">"${w.bio_text}"</p>` : ''}
      </div>

      <div class="p-5 pt-0">
        <div class="grid grid-cols-2 gap-2 mb-2.5">
          <button type="button" onclick="unlockContact('${w.id}', 'call')" class="touch-scale py-3 px-2 bg-gradient-to-r from-green-700 to-emerald-700 hover:from-green-800 hover:to-emerald-800 text-white rounded-xl font-black text-sm flex items-center justify-center gap-1.5 shadow-sm">
            <span>📞</span> ${callText.replace(/^📞\s*/, '')}
          </button>
          <button type="button" onclick="unlockContact('${w.id}', 'whatsapp')" class="touch-scale py-3 px-2 bg-gradient-to-r from-emerald-600 to-teal-700 hover:from-emerald-700 hover:to-teal-800 text-white rounded-xl font-black text-sm flex items-center justify-center gap-1.5 shadow-sm">
            <span>💬</span> ${waText.replace(/^💬\s*/, '')}
          </button>
        </div>

        <div class="flex justify-between items-center pt-2.5 border-t border-slate-100 text-xs">
          <button type="button" onclick="openWorkSlip('${w.id}')" class="text-slate-600 hover:text-green-800 font-bold flex items-center gap-1 transition-colors">
            <span>📋</span> ${slipText.replace(/^📋\s*/, '')}
          </button>
          <button type="button" onclick="shareWorkerWhatsApp('${w.name}', '${w.skills[0] || 'कारीगर'}', '${w.district}', '${w.id}')" class="text-emerald-700 hover:text-emerald-900 font-black flex items-center gap-1 transition-colors" title="WhatsApp पर शेयर करें">
            <span>📲</span> ${t_share}
          </button>
          <button type="button" onclick="openReportModal('${w.id}', '${w.name}')" class="text-slate-400 hover:text-red-700 font-bold transition-colors">
            <span>⚠️</span> ${reportText.replace(/^⚠️\s*/, '')}
          </button>
        </div>
      </div>
    </div>
    `;
  }).join('');
}
async function unlockContact(workerId, contactType) {
try {
const res = await fetch('/api/workers/unlock_contact', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({
worker_public_id: workerId,
contact_type: contactType,
session_id: localStorage.getItem('km_session_id') || 'emp_web'
})
});
const data = await res.json();
if (res.status === 429) {
speakPrompt('सुरक्षा के लिए आप थोड़े समय बाद ही अगला नंबर देख सकते हैं।');
alert(data.message || 'दर सीमा पार। कृपया 10 मिनट बाद प्रयास करें।');
return;
}
if (res.ok) {
if (contactType === 'call') {
window.location.href = data.call_url;
} else if (contactType === 'whatsapp') {
window.open(data.whatsapp_url, '_blank');
}
} else {
alert(data.message || 'संपर्क जानकारी लोड करने में समस्या हुई।');
}
} catch (err) {
alert('नेटवर्क त्रुटि हुई।');
}
}
function setTradeFilter(trade) {
  activeTradeFilter = trade;
  const select = document.getElementById('filter-trade');
  if (select && select.value !== trade) {
    if (!Array.from(select.options).some(o => o.value === trade)) {
      renderTradeDropdown();
    }
    select.value = trade;
  }
  highlightActiveFilters();
  loadWorkers();
}
function setStateFilter(state) {
  activeStateFilter = state;
  const distSelect = document.getElementById('filter-district');
  if (distSelect) {
    if (state === 'all') {
      distSelect.innerHTML = '<option value="all">सभी जिले (All Districts)</option>';
      activeDistrictFilter = 'all';
    } else {
      const districts = typeof getDistrictsForState === 'function' ? getDistrictsForState(state) : [];
      distSelect.innerHTML = '<option value="all">सभी जिले (All Districts)</option>' +
        districts.map(d => `<option value="${d}">${d}</option>`).join('');
      activeDistrictFilter = 'all';
    }
  }
  highlightActiveFilters();
  loadWorkers();
}
function setDistrictFilter(district) {
  activeDistrictFilter = district;
  highlightActiveFilters();
  loadWorkers();
}
function setStatusFilter(status) {
  activeStatusFilter = status;
  highlightActiveFilters();
  loadWorkers();
}