import os, re, shutil, json, zipfile
ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, 'src/template.html')).read()
head, body = src.split('<!--BODY-->', 1)
DESC = 'iStand and iStand Pro: a two-tier standing desk that turns any table into a correct workstation and folds like a book. Concept deck.'
FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23000'/%3E%3Crect x='17' y='18' width='30' height='4' rx='2' fill='%23d9dadc'/%3E%3Crect x='13' y='34' width='38' height='4' rx='2' fill='%23d9dadc'/%3E%3Crect x='20' y='18' width='3' height='30' fill='%23d9dadc'/%3E%3Crect x='41' y='18' width='3' height='30' fill='%23d9dadc'/%3E%3Crect x='40' y='26' width='5' height='5' rx='1' fill='%23ff5a1f'/%3E%3C/svg%3E"
def vendor(local):
    v = {'three':'vendor/three.min.js','orbit':'vendor/OrbitControls.js','room':'vendor/RoomEnvironment.js'} if local else \
        {'three':'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','orbit':'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js','room':'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/environments/RoomEnvironment.js'}
    return '<script>window.__VENDOR__=' + json.dumps(v) + '</script>'
og = os.environ.get('OG_BASE', '').rstrip('/')
ogimg = (og + '/img/og.jpg') if og else 'img/og.jpg'
static = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  f'<meta name="description" content="{DESC}">\n<meta name="robots" content="noindex">\n<meta name="theme-color" content="#000000">\n'
  f'<meta property="og:type" content="website">\n<meta property="og:title" content="iStand Concept Deck">\n<meta property="og:description" content="{DESC}">\n'
  f'<meta property="og:image" content="{ogimg}">\n<meta name="twitter:card" content="summary_large_image">\n'
  f'<link rel="icon" href="{FAV}">\n<link rel="preload" as="image" href="img/a2_istand_black.webp" fetchpriority="high">\n'
  + head.strip() + '\n</head>\n<body>\n' + body.replace('<!--VENDOR-->', vendor(True)).strip() + '\n</body>\n</html>\n')
dist = os.path.join(ROOT, 'dist')
open(os.path.join(dist, 'index.html'), 'w').write(static)
json.dump({"cleanUrls": True, "headers": [
  {"source": "/img/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
  {"source": "/vendor/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
  {"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]}]}, open(os.path.join(dist, 'vercel.json'), 'w'), indent=2)
open(os.path.join(dist, '_headers'), 'w').write("/img/*\n  Cache-Control: public, max-age=31536000, immutable\n/vendor/*\n  Cache-Control: public, max-age=31536000, immutable\n/*\n  X-Robots-Tag: noindex\n")
# artifact fragment (the host adds doctype/head/body)
art = os.path.join(ROOT, 'artifact'); os.makedirs(art, exist_ok=True)
open(os.path.join(art, 'istand-deck.html'), 'w').write(head.strip() + '\n' + body.replace('<!--VENDOR-->', vendor(False)).strip() + '\n')
# zip
zp = os.path.join(os.path.dirname(ROOT), 'istand-deck-site.zip')
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    for d, _, fs in os.walk(dist):
        for f in fs:
            full = os.path.join(d, f); z.write(full, os.path.relpath(full, dist))
tot = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(dist) for f in fs)
print('dist', tot//1024, 'KB; index.html', os.path.getsize(os.path.join(dist,'index.html'))//1024, 'KB; zip', os.path.getsize(zp)//1024, 'KB')
