/* Service worker MaxQuiz (version {{ version }}).
   Rôle : recevoir les notifications push et ouvrir la bonne page au toucher.
   Volontairement minimal : aucune mise en cache des pages (contenu toujours à jour). */
self.addEventListener('install', function (e) { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });

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
