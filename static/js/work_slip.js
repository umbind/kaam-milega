let activeSlipWorker = null;
function openWorkSlip(workerId) {
activeSlipWorker = allLoadedWorkers.find(w => w.id === workerId);
if (!activeSlipWorker) return;
const modal = document.getElementById('work-slip-modal');
const titleEl = document.getElementById('slip-worker-name');
const rateInput = document.getElementById('slip-daily-wage');
const locInput = document.getElementById('slip-location');
if (titleEl) titleEl.innerText = activeSlipWorker.name;
if (rateInput) rateInput.value = activeSlipWorker.daily_rate;
if (locInput) locInput.value = `${activeSlipWorker.village}, ${activeSlipWorker.district}`;
if (modal) {
modal.style.display = 'flex';
modal.classList.remove('hidden');
}
}
function closeWorkSlip() {
const modal = document.getElementById('work-slip-modal');
if (modal) {
modal.style.display = 'none';
modal.classList.add('hidden');
}
}
function generateWhatsAppSlip() {
if (!activeSlipWorker) return;
const employerName = document.getElementById('slip-employer-name').value.trim() || 'ग्राहक';
const wage = document.getElementById('slip-daily-wage').value.trim();
const days = document.getElementById('slip-days').value.trim();
const advance = document.getElementById('slip-advance').value.trim() || 'शून्य (0)';
const location = document.getElementById('slip-location').value.trim();
const today = new Date().toLocaleDateString('hi-IN');
const message = `📋 *काम की पर्ची (Work Agreement Slip)*
-----------------------------------
📅 दिनांक: ${today}
👷 कारीगर: ${activeSlipWorker.name}
👤 नियोक्ता (ग्राहक): ${employerName}
📍 काम का स्थान: ${location}
💰 तय दिहाड़ी: ₹${wage} प्रति दिन
⏳ काम की अवधि: ${days} दिन
💵 अग्रिम (Advance): ₹${advance}
-----------------------------------
⚖️ दोनों पक्षों की आपसी सहमति से तय हुआ।
⚠️ वैधानिक अस्वीकरण: काम मिलेगा केवल मध्यस्थ है (0% कमीशन, 18+ अनिवार्य)। कार्यस्थल सुरक्षा व मजदूरी अदायगी की जिम्मेदारी पक्षों की है।
🔗 प्लेटफॉर्म: काम मिलेगा (Kaam Milega) https://kaammilega.org`;
const encoded = encodeURIComponent(message);
window.open(`https://api.whatsapp.com/send?text=${encoded}`, '_blank');
closeWorkSlip();
}
