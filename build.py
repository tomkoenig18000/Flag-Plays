#!/usr/bin/env python3
"""Build Flag Plays from src/app.html + src/plays.json -> docs/ (served by GitHub Pages).

docs/plays/NN.webp are made once from the playbook PDF by tools/pdf_to_images.py.
"""
import json, pathlib, re
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).parent
SRC = (ROOT / 'src' / 'app.html').read_text()
PLAYS = json.loads((ROOT / 'src' / 'plays.json').read_text())
VERSION = int((ROOT / 'src' / 'VERSION').read_text().strip())
site = ROOT / 'docs'
(site / 'icons').mkdir(parents=True, exist_ok=True)

SW_REG = '''<script>
  // Offline support: the service worker caches the app shell + every play image.
  if ('serviceWorker' in navigator) {
    const hadController = !!navigator.serviceWorker.controller;
    navigator.serviceWorker.register('sw.js').then((reg) => {
      document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') reg.update().catch(() => {}); });
    }).catch(() => {});
    if (hadController) navigator.serviceWorker.addEventListener('controllerchange', () => document.dispatchEvent(new Event('swupdated')));
  }
</script>
'''
html = SRC.replace('{{VERSION}}', str(VERSION)).replace('{{PLAYS}}', json.dumps(PLAYS, separators=(',', ':')))
html = html.replace('</body>', SW_REG + '</body>')
(site / 'index.html').write_text(html)

(site / 'manifest.webmanifest').write_text(json.dumps({
    "name": "Flag Plays", "short_name": "Flag Plays",
    "description": "Fast play-calling reference for flag football.",
    "start_url": "./", "scope": "./", "display": "standalone", "orientation": "any",
    "background_color": "#0f3d24", "theme_color": "#0f3d24",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, indent=2) + '\n')

imgs = [f'./{d}/{p["id"]:02d}.webp' for d in ('plays', 'thumbs') for p in PLAYS]
shell = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'] + imgs
(site / 'sw.js').write_text(f'''// Flag Plays service worker — v{VERSION}
const CACHE = 'flagplays-v{VERSION}';
const SHELL = {json.dumps(shell)};
self.addEventListener('install', (e) => {{
  // cache: 'reload' bypasses the HTTP cache so a new worker never pre-caches a stale shell
  e.waitUntil(caches.open(CACHE).then((c) => Promise.all(SHELL.map((u) => fetch(u, {{ cache: 'reload' }}).then((r) => {{ if (!r.ok) throw new Error(u); return c.put(u, r); }})))).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', (e) => {{
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener('fetch', (e) => {{
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url); if (url.origin !== self.location.origin) return;
  // play images never change for a given version: cache-first
  if (url.pathname.includes('/plays/') || url.pathname.includes('/thumbs/')) {{
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => {{ const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); return res; }})));
    return;
  }}
  // app shell: network-first so a launch with signal gets the newest version; falls back to cache offline
  e.respondWith(fetch(req, {{ cache: 'no-cache' }}).then((res) => {{ const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); return res; }})
    .catch(() => caches.match(req).then((hit) => hit || (req.mode === 'navigate' ? caches.match('./index.html') : undefined))));
}});
''')

def icon(size, path, rounded=True):
    im = Image.new('RGBA', (size, size), (15, 61, 36, 255))
    d = ImageDraw.Draw(im); s = size / 100.0
    if rounded: pass
    for y in (22, 50, 78):  # yard lines
        d.line([(8 * s, y * s), (92 * s, y * s)], fill=(255, 255, 255, 200), width=max(2, int(1.6 * s)))
    # route: from QB up and across, with arrowhead
    pts = [(30 * s, 78 * s), (30 * s, 42 * s), (68 * s, 42 * s), (68 * s, 24 * s)]
    d.line(pts, fill=(255, 228, 92, 255), width=int(5 * s), joint='curve')
    d.polygon([(60 * s, 28 * s), (76 * s, 28 * s), (68 * s, 14 * s)], fill=(255, 228, 92, 255))
    for (x, y) in [(30, 78), (68, 62)]:
        d.ellipse([(x - 8) * s, (y - 8) * s, (x + 8) * s, (y + 8) * s], fill=(255, 255, 255, 255), outline=(20, 32, 26, 255), width=max(2, int(2 * s)))
    im.convert('RGB').save(path)
icon(512, site / 'icons' / 'icon-512.png'); icon(192, site / 'icons' / 'icon-192.png'); icon(180, site / 'icons' / 'apple-touch-icon.png')
print('built v%d, %d plays' % (VERSION, len(PLAYS)))
