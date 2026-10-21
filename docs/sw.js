// Flag Plays service worker — v1
const CACHE = 'flagplays-v1';
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/apple-touch-icon.png", "./plays/01.webp", "./plays/02.webp", "./plays/03.webp", "./plays/04.webp", "./plays/05.webp", "./plays/06.webp", "./plays/07.webp", "./plays/08.webp", "./plays/09.webp", "./plays/10.webp", "./plays/11.webp", "./plays/12.webp", "./plays/13.webp", "./plays/14.webp", "./plays/15.webp", "./plays/16.webp", "./plays/17.webp", "./plays/18.webp", "./plays/19.webp", "./plays/20.webp", "./plays/21.webp", "./plays/22.webp", "./plays/23.webp", "./plays/24.webp", "./plays/25.webp", "./plays/26.webp", "./plays/27.webp", "./plays/28.webp", "./plays/29.webp", "./plays/30.webp", "./plays/31.webp", "./plays/32.webp", "./plays/33.webp", "./plays/34.webp", "./plays/35.webp", "./plays/36.webp", "./plays/37.webp", "./plays/38.webp", "./plays/39.webp", "./plays/40.webp", "./plays/41.webp", "./plays/42.webp", "./plays/43.webp", "./plays/44.webp", "./plays/45.webp", "./plays/46.webp", "./plays/47.webp", "./plays/48.webp", "./plays/49.webp", "./plays/50.webp"];
self.addEventListener('install', (e) => {
  // cache: 'reload' bypasses the HTTP cache so a new worker never pre-caches a stale shell
  e.waitUntil(caches.open(CACHE).then((c) => Promise.all(SHELL.map((u) => fetch(u, { cache: 'reload' }).then((r) => { if (!r.ok) throw new Error(u); return c.put(u, r); })))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url); if (url.origin !== self.location.origin) return;
  // play images never change for a given version: cache-first
  if (url.pathname.includes('/plays/')) {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); return res; })));
    return;
  }
  // app shell: network-first so a launch with signal gets the newest version; falls back to cache offline
  e.respondWith(fetch(req, { cache: 'no-cache' }).then((res) => { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); return res; })
    .catch(() => caches.match(req).then((hit) => hit || (req.mode === 'navigate' ? caches.match('./index.html') : undefined))));
});
