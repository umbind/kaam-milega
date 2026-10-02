const LANG_LOCALE_MAP = {
hi: 'hi-IN',
bho: 'hi-IN',
en: 'en-IN',
bn: 'bn-IN',
mr: 'mr-IN',
te: 'te-IN',
ta: 'ta-IN',
kn: 'kn-IN',
gu: 'gu-IN',
pa: 'pa-IN',
or: 'hi-IN',
ml: 'ml-IN'
};
class SpeechManager {
constructor() {
this.synth = window.speechSynthesis;
this.voices = [];
this.currentLanguage = 'hi';
this.isSpeaking = false;
this.activeButton = null;
if (this.synth) {
this.loadVoices();
if (speechSynthesis.onvoiceschanged !== undefined) {
speechSynthesis.onvoiceschanged = () => this.loadVoices();
}
}
}
loadVoices() {
if (this.synth) {
this.voices = this.synth.getVoices();
}
}
getBestVoice(langCode) {
if (!this.voices || this.voices.length === 0) {
this.loadVoices();
}
const targetLocale = LANG_LOCALE_MAP[langCode] || 'hi-IN';
const primaryPrefix = targetLocale.split('-')[0];
// 1. Exact match
let match = this.voices.find(v => v.lang === targetLocale);
// 2. Prefix match (e.g. bn, mr, te, ta)
if (!match) {
match = this.voices.find(v => v.lang.startsWith(primaryPrefix));
}
// 3. Fallback to any Indian voice
if (!match) {
match = this.voices.find(v => v.lang.includes('IN') || v.lang.includes('Hindi'));
}
return match || this.voices[0] || null;
}
speak(text, buttonElement = null) {
if (!this.synth) {
console.warn('Speech synthesis not supported on this browser.');
return;
}
if (this.synth.speaking) {
this.synth.cancel();
if (this.activeButton) {
this.activeButton.classList.remove('speaking-active');
}
if (this.activeButton === buttonElement) {
this.activeButton = null;
return;
}
}
if (!text || !text.trim()) return;
const utterance = new SpeechSynthesisUtterance(text.trim());
const voice = this.getBestVoice(this.currentLanguage);
if (voice) {
utterance.voice = voice;
}
utterance.lang = LANG_LOCALE_MAP[this.currentLanguage] || 'hi-IN';
utterance.rate = 0.95;
utterance.pitch = 1.0;
if (buttonElement) {
this.activeButton = buttonElement;
buttonElement.classList.add('speaking-active');
}
utterance.onend = () => {
this.isSpeaking = false;
if (this.activeButton) {
this.activeButton.classList.remove('speaking-active');
this.activeButton = null;
}
};
utterance.onerror = () => {
this.isSpeaking = false;
if (this.activeButton) {
this.activeButton.classList.remove('speaking-active');
this.activeButton = null;
}
};
this.isSpeaking = true;
this.synth.speak(utterance);
}
setLanguage(lang) {
this.currentLanguage = lang;
}
}
const speechMgr = new SpeechManager();
function speakPrompt(text, btn = null) {
speechMgr.speak(text, btn);
}
