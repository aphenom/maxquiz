/* Service worker MaxQuiz (version {{ version }}).
   Rôle : notifications push, page « hors connexion », et fichiers statiques (styles,
   icônes) gardés sur le téléphone pour économiser les données en 3G.
   Les pages elles-mêmes viennent toujours du réseau : contenu toujours à jour. */
var CACHE = 'maxquiz-{{ version }}';
var OFFLINE = '/hors-ligne/';

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.add(OFFLINE); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (event) {
  var req = event.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (req.mode === 'navigate') {
    event.respondWith(fetch(req).catch(function () { return caches.match(OFFLINE); }));
    return;
  }
  if (url.pathname.indexOf('/static/') === 0) {
    event.respondWith(caches.match(req).then(function (hit) {
      return hit || fetch(req).then(function (resp) {
        if (resp.ok) { var copy = resp.clone(); caches.open(CACHE).then(function (c) { c.put(req, copy); }); }
        return resp;
      });
    }));
  }
});

self.addEventListener('push', function (event) {
  var data = {};
  try { data = event.data ? event.data.json() : {}; } catch (err) { data = { title: 'MaxQuiz', body: event.data && event.data.text() }; }
  var title = data.title || 'MaxQuiz';
  event.waitUntil(self.registration.showNotification(title, {
    body: data.body || '',
    icon: '/static/game/icons/icon-192.png',
    badge: '/static/game/icons/badge-96.png',
    tag: data.tag || 'maxquiz',
    renotify: true,
    data: { url: data.url || '/' }
  }));
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  var url = new URL((event.notification.data && event.notification.data.url) || '/', self.location.origin).href;
  event.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (wins) {
    for (var i = 0; i < wins.length; i++) {
      if ('focus' in wins[i]) { wins[i].navigate(url); return wins[i].focus(); }
    }
    return self.clients.openWindow(url);
  }));
});
