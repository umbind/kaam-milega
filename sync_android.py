import shutil
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANDROID_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'kaam-milega-android', 'app', 'src', 'main', 'assets', 'www'))

# 1. Sync CSS
shutil.copyfile(
    os.path.join(BASE_DIR, 'static', 'css', 'app.css'),
    os.path.join(ANDROID_DIR, 'static', 'css', 'app.css')
)

# 2. Sync JS Files
js_files = ['search.js', 'app.js', 'compliance.js', 'jobs.js', 'work_slip.js', 'wizard.js', 'i18n.js', 'speech.js', 'geo_data.js']
for jf in js_files:
    src_f = os.path.join(BASE_DIR, 'static', 'js', jf)
    dst_f = os.path.join(ANDROID_DIR, 'static', 'js', jf)
    if os.path.exists(src_f):
        shutil.copyfile(src_f, dst_f)

# 3. Sync Legal HTML Pages
legal_pages = ['disclaimer.html', 'privacy_policy.html', 'terms.html']
for lp in legal_pages:
    src_p = os.path.join(BASE_DIR, 'templates', lp)
    dst_p = os.path.join(ANDROID_DIR, lp)
    if os.path.exists(src_p):
        with open(src_p, 'r', encoding='utf-8') as f:
            c = f.read()
        c_offline = c.replace('href="/static/', 'href="static/').replace('src="/static/', 'src="static/').replace('href="/disclaimer"', 'href="disclaimer.html"').replace('href="/privacy"', 'href="privacy_policy.html"').replace('href="/terms"', 'href="terms.html"')
        with open(dst_p, 'w', encoding='utf-8') as f:
            f.write(c_offline)

# 4. Sync Index HTML
with open(os.path.join(BASE_DIR, 'templates', 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

html_offline = html.replace('href="/static/', 'href="static/').replace('src="/static/', 'src="static/').replace('href="/disclaimer"', 'href="disclaimer.html"').replace('href="/privacy"', 'href="privacy_policy.html"').replace('href="/terms"', 'href="terms.html"')

with open(os.path.join(ANDROID_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_offline)

print("SYNC_SUCCESSFUL: All updated CSS, JS and index.html + legal docs copied to Android assets.")
