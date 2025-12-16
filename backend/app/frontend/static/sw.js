// Service Worker for Hangman PWA
const CACHE_NAME = 'hangman-pwa-v1';
const ASSETS = [
  '/frontend/static/index.html',
  '/frontend/static/game.html',
  '/frontend/static/login.html',
  '/frontend/static/register.html',
  '/frontend/static/css/layout.css',
  '/frontend/static/manifest.json',
  '/frontend/static/javascript/game.js',
  '/frontend/static/javascript/index.js',
  '/frontend/static/javascript/login.js',
  '/frontend/static/javascript/register.js',
  '/frontend/static/javascript/theme.js',
  '/frontend/static/icons/icon-192.png',
  '/frontend/static/icons/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response =>
      response || fetch(event.request).catch(() => caches.match('/frontend/static/index.html'))
    )
  );
});

