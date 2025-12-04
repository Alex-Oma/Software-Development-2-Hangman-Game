self.addEventListener('install', function(event) {
  self.skipWaiting();
});
self.addEventListener('fetch', function(event) {
  // Basic offline fallback when no connection is available
  event.respondWith(fetch(event.request).catch(() => caches.match('/static/index.html')));
});

