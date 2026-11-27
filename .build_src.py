# Ab 27.11.2026: nur noch BM wird umgebaut. Kp, Grfhr und UOS bauen aus dem eingefrorenen Stand (template_frozen.html).
t=open('app/template_frozen.html',encoding='utf-8').read()
tb=open('app/template.html',encoding='utf-8').read()
libs='<script>'+open('libs/qrcode.min.js',encoding='utf-8').read()+'</script>\n<script>'+open('libs/jsqr.min.js',encoding='utf-8').read()+'</script>'
t=t.replace('<!--__QRLIBS__-->',libs)
b=open('demo_map.b64').read().strip()
m=t.replace('"__DEMO_MAP__"','"data:image/jpeg;base64,'+b+'"').replace('__DEMO_MAP_W__','1474').replace('__DEMO_MAP_H__','1600')
open('app/Fuehrungssystem.html','w',encoding='utf-8').write(m)
# BM-Version: wie Kp Kdt, zusätzlich Kaderselektion
mb=tb.replace('<!--__QRLIBS__-->',libs).replace('"__DEMO_MAP__"','"data:image/jpeg;base64,'+b+'"').replace('__DEMO_MAP_W__','1474').replace('__DEMO_MAP_H__','1600')
open('app/Fuehrungssystem_BM.html','w',encoding='utf-8').write(mb.replace('/*__BM_MODE__*/false','true').replace('<title>Führungssystem Kp</title>','<title>Führungssystem BM</title>'))
g=t.replace('"__DEMO_MAP__"','"data:image/jpeg;base64,'+b+'"').replace('__DEMO_MAP_W__','1474').replace('__DEMO_MAP_H__','1600').replace('/*__GR_MODE__*/false','true').replace('<title>Führungssystem Kp</title>','<title>Führungssystem Grfhr</title>')
open('app/Grfhr.html','w',encoding='utf-8').write(g)
# Web-App (PWA) für iPhone/Android: index.html + manifest + Service Worker + Icons
import os, hashlib
head='<link rel="manifest" href="manifest.webmanifest">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black">\n<meta name="apple-mobile-web-app-title" content="Grfhr">\n<meta name="theme-color" content="#1d1d1d">\n<link rel="apple-touch-icon" href="icon-180.png">\n'
pw=g.replace('<title>Führungssystem Grfhr</title>','<title>Führungssystem Grfhr</title>\n'+head,1)
reg='<script>if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) navigator.serviceWorker.register("sw.js").catch(function(){});</script>\n</body>'
pw=pw[:pw.rindex('</body>')]+reg+pw[pw.rindex('</body>')+7:]
os.makedirs('pwa',exist_ok=True)
open('pwa/index.html','w',encoding='utf-8').write(pw)
ver=hashlib.sha1(pw.encode()).hexdigest()[:10]
open('pwa/manifest.webmanifest','w').write('{"name":"Führungssystem Grfhr","short_name":"Grfhr","start_url":"./","scope":"./","display":"standalone","background_color":"#e5e5e5","theme_color":"#1d1d1d","icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]}')
open('pwa/sw.js','w').write("""const C='grfhr-%s';const F=['./','index.html','manifest.webmanifest','icon-180.png','icon-192.png','icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(F)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==location.origin)return;
e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).then(n=>{const cp=n.clone();caches.open(C).then(c=>c.put(e.request,cp));return n;}).catch(()=>caches.match('index.html'))));});
""" % ver)
# UOS-Version: Klasse (Struktur eines Zuges) mit drei Gruppen, Klassenlehrer statt Kp Kdt / Zfhr
import re as _re
# Umbenennen nur im Quelltext: Bibliotheken und eingebettete Bilder (data:-URIs) bleiben unberührt
_raw = open('app/template_frozen.html', encoding='utf-8').read()
_keep = []
def _mask(mo):
    _keep.append(mo.group(0)); return '@@DATA%d@@' % (len(_keep) - 1)
u = _re.sub(r'data:[a-z/+.-]+;base64,[A-Za-z0-9+/=]+', _mask, _raw)
u = u.replace('/*__UOS_MODE__*/false', 'true').replace('<title>Führungssystem Kp</title>', '<title>Führungssystem UOS</title>')
u = u.replace("'Führungsdokument Zfhr ' + z.name", "'Führungsdokument Klasse ' + z.name")
for _a, _b in [('Kp Kdt Stv', 'Stv Klassenlehrer'), ('Kp Kdt', 'Klassenlehrer'), ('Zfhr-Rapport', 'Klassenrapport'), ('Zfhr-Dokument', 'Klassendokument'),
             ('seines Zuges', 'seiner Klasse'), ('des Zuges', 'der Klasse'), ('eines Zuges', 'einer Klasse'), ('seinen Zug', 'seine Klasse'), ('eigener Zug', 'eigene Klasse'),
             ('einen Zug', 'eine Klasse'), ('ein Zug', 'eine Klasse'), ('Ein Zug', 'Eine Klasse'), ('den Zug', 'die Klasse'), ('dem Zug', 'der Klasse'), ('Der Zug', 'Die Klasse'), ('der Zug', 'die Klasse'),
             ('Stv Zfhr', 'Stv Klassenlehrer')]:
    u = u.replace(_a, _b)
u = _re.sub(r'\bZfhr\b', 'Klassenlehrer', u)
u = _re.sub(r'\bZuges\b', 'Klasse', u)
u = _re.sub(r'\bZüge\b', 'Klassen', u)
u = _re.sub(r'\bZug\b', 'Klasse', u)
u = _re.sub(r'\bKp\b', 'Klasse', u)
u = _re.sub(r'@@DATA(\d+)@@', lambda mo: _keep[int(mo.group(1))], u)
u = u.replace('<!--__QRLIBS__-->', libs).replace('"__DEMO_MAP__"', '"data:image/jpeg;base64,' + b + '"').replace('__DEMO_MAP_W__', '1474').replace('__DEMO_MAP_H__', '1600')
open('app/Fuehrungssystem_UOS.html', 'w', encoding='utf-8').write(u)
