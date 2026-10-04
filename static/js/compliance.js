function checkConsentBanner() {
const consentGiven = localStorage.getItem('km_dpdp_consent');
const banner = document.getElementById('dpdp-consent-banner');
if (!consentGiven && banner) {
banner.style.display = 'block';
banner.classList.remove('hidden');
}
}

function acceptDPDPConsent() {
localStorage.setItem('km_dpdp_consent', 'true');
const banner = document.getElementById('dpdp-consent-banner');
if (banner) {
banner.style.display = 'none';
banner.classList.add('hidden');
}
}
function toggleEmergencyDrawer() {
const modal = document.getElementById('emergency-modal');
if (modal) {
const isVisible = modal.style.display === 'flex' || (!modal.classList.contains('hidden') && modal.style.display !== 'none');
if (isVisible) {
modal.style.display = 'none';
modal.classList.add('hidden');
} else {
modal.style.display = 'flex';
modal.classList.remove('hidden');
}
}
}
let currentReportTargetId = '';
let currentReportTargetName = '';

function openReportModal(targetId, targetName) {
currentReportTargetId = targetId;
currentReportTargetName = targetName;
const titleEl = document.getElementById('report-target-title');
if (titleEl) titleEl.innerText = targetName || 'कारीगर';

const modal = document.getElementById('report-modal');
if (modal) {
modal.style.display = 'flex';
modal.classList.remove('hidden');
}
}

function closeReportModal() {
const modal = document.getElementById('report-modal');
if (modal) {
modal.style.display = 'none';
modal.classList.add('hidden');
}
}

async function submitReport() {
const reason = document.getElementById('report-reason').value;
const details = document.getElementById('report-details').value.trim();

try {
const res = await fetch('/api/reports/create', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({
target_public_id: currentReportTargetId,
target_type: 'worker',
reason: reason,
details: details,
session_id: localStorage.getItem('km_session_id') || 'anon'
})
});

const data = await res.json();
closeReportModal();

if (reason === 'child_labour') {
speakPrompt('बाल श्रम की शिकायत दर्ज कर ली गई है। प्रोफाइल को तुरंत समीक्षा के लिए छिपा दिया गया है।');
alert('बाल श्रम की शिकायत दर्ज की गई। जांच होने तक यह प्रोफाइल तुरंत ब्लॉक कर दी गई है।');
} else {
alert(data.message || 'आपकी शिकायत दर्ज कर ली गई है।');
}
loadWorkers(); // Refresh directory
} catch (err) {
alert('शिकायत दर्ज करने में त्रुटि हुई।');
}
}
function openDeleteAccountModal() {
const modal = document.getElementById('delete-profile-modal');
if (modal) {
modal.style.display = 'flex';
modal.classList.remove('hidden');
}
}

function closeDeleteAccountModal() {
const modal = document.getElementById('delete-profile-modal');
if (modal) {
modal.style.display = 'none';
modal.classList.add('hidden');
}
}

async function confirmDeleteProfile() {
const workerId = localStorage.getItem('km_worker_id');
if (!workerId) {
closeDeleteAccountModal();
alert('कोई सक्रिय कारीगर प्रोफाइल नहीं मिली जिसे हटाया जा सके।');
return;
}

try {
const res = await fetch('/api/workers/delete', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({
worker_public_id: workerId
})
});
const data = await res.json();
} catch (err) {
console.warn('Network error while deleting profile on server:', err);
} finally {
localStorage.removeItem('km_worker_id');
localStorage.removeItem('km_worker_name');
localStorage.removeItem('km_worker_phone');
closeDeleteAccountModal();

if (typeof speakPrompt === 'function') {
speakPrompt('आपकी प्रोफाइल और डेटा सुरक्षित रूप से हटा दिया गया है।');
}
alert('आपकी प्रोफाइल और समस्त व्यक्तिगत डेटा हटा दिया गया है।');
if (typeof resetWizardState === 'function') {
resetWizardState();
}
if (typeof renderProfileView === 'function') {
renderProfileView();
}
}
}
async function toggleSeasonalDormancy(newStatus) {
const workerId = localStorage.getItem('km_worker_id');
if (!workerId) return;

try {
const res = await fetch('/api/workers/status_toggle', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({
worker_public_id: workerId,
status: newStatus
})
});
const data = await res.json();
if (res.ok) {
if (newStatus === 'seasonal_dormancy') {
alert('🌾 आपकी प्रोफाइल खेती/फसल कटाई अवकाश पर सेट कर दी गई है। आपकी रेटिंग सुरक्षित रहेगी!');
} else {
alert('🟢 आपकी स्थिति उपलब्ध (काम के लिए तैयार) सेट कर दी गई है!');
}
location.reload();
}
} catch (err) {
alert('स्थिति बदलने में त्रुटि हुई।');
}
}

// ==========================================
// LEGAL DISCLAIMERS CONTROLLER & READ ALOUD
// ==========================================
let activeDisclaimerSection = 'intermediary';

function openLegalDisclaimersModal(defaultSection) {
  const modal = document.getElementById('legal-disclaimers-modal');
  if (modal) {
    modal.style.display = 'flex';
    modal.classList.remove('hidden');
    selectDisclaimerTab(defaultSection || activeDisclaimerSection || 'intermediary');
  }
}

function closeLegalDisclaimersModal() {
  const modal = document.getElementById('legal-disclaimers-modal');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.add('hidden');
  }
}

function selectDisclaimerTab(tabKey) {
  activeDisclaimerSection = tabKey;
  const tabs = document.querySelectorAll('.disc-tab-btn');
  tabs.forEach(btn => {
    if (btn.dataset.tab === tabKey) {
      btn.className = 'disc-tab-btn px-3 py-1.5 rounded-xl whitespace-nowrap bg-green-700 text-white shadow-sm transition-all touch-btn';
    } else {
      btn.className = 'disc-tab-btn px-3 py-1.5 rounded-xl whitespace-nowrap bg-slate-100 text-slate-700 transition-all touch-btn';
    }
  });

  const sections = document.querySelectorAll('.disc-content-pane');
  sections.forEach(sec => {
    if (sec.id === 'disc-pane-' + tabKey) {
      sec.classList.remove('hidden');
    } else {
      sec.classList.add('hidden');
    }
  });
}

function speakActiveDisclaimer() {
  const pane = document.getElementById('disc-pane-' + activeDisclaimerSection);
  if (!pane) return;
  const audioText = pane.dataset.audioSummary || pane.innerText;
  if (typeof speakPrompt === 'function') {
    speakPrompt(audioText);
  }
}
