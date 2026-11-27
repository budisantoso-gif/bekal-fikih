// Dibuat oleh tools/build.py. Jangan disunting langsung.
const CACHE='bekal-fikih-v0.36';
const ASSETS=["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-maskable-512.png", "./icons/apple-touch-icon.png", "./fonts/amiri-arabic-400.woff2", "./fonts/amiri-arabic-700.woff2", "./fonts/jakarta-latin-400.woff2", "./fonts/jakarta-latin-500.woff2", "./fonts/jakarta-latin-700.woff2", "./fonts/jakarta-latin-ext-400.woff2", "./fonts/jakarta-latin-ext-500.woff2", "./fonts/jakarta-latin-ext-700.woff2", "./fonts/naskh-arabic-500.woff2", "./fonts/naskh-arabic-600.woff2", "./fonts/naskh-arabic-700.woff2"];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const r=e.request;
  if(r.method!=='GET')return;
  const u=new URL(r.url);
  // Hanya tangani berkas milik sendiri; halaman /review/ tetap lewat jaringan.
  if(u.origin!==location.origin||u.pathname.indexOf('/review/')!==-1)return;
  if(r.mode==='navigate'){
    // Jaringan dulu (agar pembaruan sampai), cadangan dari cache bila offline atau lambat.
    e.respondWith(Promise.race([
      fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put('./index.html',cp));}return res;}),
      new Promise((_,rej)=>setTimeout(()=>rej(new Error('timeout')),3000))
    ]).catch(()=>caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));}return res;})));
});
