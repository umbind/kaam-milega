import shutil
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANDROID_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'kaam-milega-android', 'app', 'src', 'main', 'assets', 'www'))

shutil.copyfile(
    os.path.join(BASE_DIR, 'static', 'css', 'app.css'),
    os.path.join(ANDROID_DIR, 'static', 'css', 'app.css')
)

shutil.copyfile(
    os.path.join(BASE_DIR, 'static', 'js', 'search.js'),
    os.path.join(ANDROID_DIR, 'static', 'js', 'search.js')
)

shutil.copyfile(
    os.path.join(BASE_DIR, 'static', 'js', 'app.js'),
    os.path.join(ANDROID_DIR, 'static', 'js', 'app.js')
)

with open(os.path.join(BASE_DIR, 'templates', 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

html_offline = html.replace('href="/static/', 'href="static/').replace('src="/static/', 'src="static/')

with open(os.path.join(ANDROID_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_offline)

print("SYNC_SUCCESSFUL: All updated CSS, JS and index.html copied to Android assets.")
