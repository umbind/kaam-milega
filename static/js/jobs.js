async function loadJobs() {
const container = document.getElementById('jobs-list-container');
if (!container) return;

container.innerHTML = `
<div class="py-8 text-center text-slate-500 font-bold">
काम की मांग लोड हो रही है...
</div>
`;

try {
const res = await fetch('/api/jobs');
const data = await res.json();
const jobs = data.jobs || [];

if (jobs.length === 0) {
container.innerHTML = `
<div class="bg-white p-8 rounded-2xl text-center border-2 border-dashed border-slate-200">
<p class="text-slate-500 font-bold">फिलहाल कोई नया काम पोस्ट नहीं है। नीचे दिए फॉर्म से नया काम पोस्ट करें।</p>
</div>
`;
return;
}

container.innerHTML = jobs.map(j => `
<div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 mb-3">
<div class="flex items-start justify-between mb-2">
<div>
<span class="bg-green-100 text-green-900 text-xs px-2.5 py-1 rounded-md font-bold inline-block mb-1">
${TRADE_NAMES[j.skill_needed] || j.skill_needed} की आवश्यकता
</span>
<h4 class="text-base font-extrabold text-slate-900">${j.employer_name}</h4>
</div>
<span class="text-sm font-black text-green-800 bg-green-50 px-2.5 py-1 rounded-lg border border-green-200">
₹${j.daily_wage_offered}/दिन
</span>
</div>

<div class="grid grid-cols-2 gap-2 text-xs text-slate-600 mb-3 font-semibold">
<p>👥 <strong>${j.num_workers}</strong> कारीगर चाहिए</p>
<p>⏳ <strong>${j.duration_days}</strong> दिन का काम</p>
<p class="col-span-2">📍 ${j.village}, ${j.district}</p>
</div>

<div class="pt-3 border-t border-slate-100 flex items-center justify-between">
<span class="text-xs text-slate-400 font-medium">पोस्ट किया: ${j.created_at}</span>
<span class="text-xs font-bold text-slate-700">संपर्क: ${j.employer_phone_masked}</span>
</div>
</div>
`).join('');
} catch (err) {
container.innerHTML = `<div class="text-red-500 text-center font-bold">लोड नहीं हो सका।</div>`;
}
}

async function submitJobPost(event) {
event.preventDefault();

const disclaimer = document.getElementById('job-child-labour-disclaimer');
if (!disclaimer || !disclaimer.checked) {
speakPrompt('चेतावनी: 18 वर्ष से कम उम्र के बच्चों को काम पर लगाना गैर कानूनी है। कृपया नियम स्वीकार करें।');
alert('कृपया बाल श्रम निषेध नियम स्वीकार करें। 18 वर्ष से कम उम्र के बच्चों को काम पर नहीं लगाया जा सकता।');
return;
}

const payload = {
employer_name: document.getElementById('job-employer-name').value.trim(),
phone: document.getElementById('job-phone').value.trim(),
skill_needed: document.getElementById('job-skill').value,
num_workers: parseInt(document.getElementById('job-workers-needed').value) || 1,
duration_days: parseInt(document.getElementById('job-duration').value) || 1,
daily_wage_offered: parseInt(document.getElementById('job-wage').value) || 600,
district: document.getElementById('job-district').value,
village: document.getElementById('job-village').value.trim(),
child_labour_disclaimer_accepted: 1
};

try {
const res = await fetch('/api/jobs/create', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify(payload)
});
const data = await res.json();

if (res.ok) {
speakPrompt('काम की आवश्यकता सफलतापूर्वक पोस्ट कर दी गई है।');
alert('काम की आवश्यकता पोस्ट कर दी गई है! आसपास के कारीगर जल्द संपर्क करेंगे।');
document.getElementById('job-post-form').reset();
loadJobs();
} else {
alert(data.message || 'त्रुटि हुई।');
}
} catch (err) {
alert('नेटवर्क समस्या।');
}
}

function onJobStateChange(selectedState) {
const districts = typeof getDistrictsForState === 'function' ? getDistrictsForState(selectedState) : [];
const distSelect = document.getElementById('job-district');
if (distSelect) {
distSelect.innerHTML = districts.map(d => `<option value="${d}">${d}</option>`).join('');
}
}

function initJobFormStates() {
const stateSelect = document.getElementById('job-state');
if (stateSelect && stateSelect.children.length <= 1 && typeof getIndiaStates === 'function') {
const states = getIndiaStates();
stateSelect.innerHTML = states.map(s => `<option value="${s}">${s}</option>`).join('');
onJobStateChange(states[0]);
}
}
function initJobSkillOptions() {
const sel = document.getElementById('job-skill');
if (!sel || typeof STANDARD_TRADES === 'undefined') return;
const currentVal = sel.value || 'mason';
sel.innerHTML = STANDARD_TRADES.filter(t => t.key !== 'all').map(t =>
`<option value="${t.key}" ${t.key === currentVal ? 'selected' : ''}>${t.defaultName}</option>`
).join('');
}
document.addEventListener('DOMContentLoaded', initJobSkillOptions);
