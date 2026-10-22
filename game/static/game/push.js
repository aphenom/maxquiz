/* Notifications MaxQuiz côté page.
   - enregistre le service worker (application installable) ;
   - window.maxquizEnablePush() : demande l'autorisation puis abonne l'appareil ;
   - window.maxquizSetFcmToken(jeton) : point d'entrée pour un APK WebView/natif. */
(function () {
  function csrf() { var m = document.cookie.match(/csrftoken=([^;]+)/); return m ? m[1] : ''; }
  function post(url, body) {
    return fetch(url, { method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() }, body: JSON.stringify(body) });
  }
  function keyBytes(b64) {
    var s = (b64 + '='.repeat((4 - b64.length % 4) % 4)).replace(/-/g, '+').replace(/_/g, '/');
    var raw = atob(s), out = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) out[i] = raw.charCodeAt(i);
    return out;
  }
  var swReady = ('serviceWorker' in navigator)
    ? navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(function () { return null; })
    : Promise.resolve(null);

  window.maxquizPushSupported = function () {
    return 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;
  };
  window.maxquizEnablePush = function () {
    if (!window.maxquizPushSupported()) return Promise.resolve('unsupported');
    return fetch('/api/push/config/').then(function (r) { return r.json(); }).then(function (cfg) {
      if (!cfg.webpush) return 'unconfigured';
      return Notification.requestPermission().then(function (perm) {
        if (perm !== 'granted') return perm;
        return swReady.then(function (reg) {
          reg = reg || navigator.serviceWorker.ready;
          return Promise.resolve(reg).then(function (r) {
            return r.pushManager.getSubscription().then(function (sub) {
              return sub || r.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: keyBytes(cfg.vapidPublicKey) });
            });
          }).then(function (sub) { return post('/api/push/subscribe/', sub.toJSON()); }).then(function () { return 'granted'; });
        });
      });
    });
  };
  // Appelé par un APK WebView/natif qui a obtenu un jeton Firebase
  window.maxquizSetFcmToken = function (token) { if (token) post('/api/push/fcm/', { token: token }); };

  // Carte « Activer les notifications » : visible seulement si utile
  document.addEventListener('DOMContentLoaded', function () {
    var card = document.querySelector('[data-push-card]');
    if (!card) return;
    if (!window.maxquizPushSupported() || Notification.permission !== 'default') return;
    try { if (localStorage.getItem('mq-push-later') === '1') return; } catch (e) {}
    card.hidden = false;
    card.querySelector('[data-push-yes]').addEventListener('click', function (e) {
      var btn = e.currentTarget; btn.disabled = true;
      window.maxquizEnablePush().then(function (res) {
        card.classList.add(res === 'granted' ? 'push-ok' : 'push-no');
        card.querySelector('[data-push-msg]').textContent = res === 'granted'
          ? 'C’est activé : tu seras prévenu des nouveaux cours et des séances.'
          : 'Notifications non activées. Tu peux changer d’avis dans les réglages du téléphone.';
        setTimeout(function () { card.hidden = true; }, 3500);
      });
    });
    card.querySelector('[data-push-no]').addEventListener('click', function () {
      try { localStorage.setItem('mq-push-later', '1'); } catch (e) {}
      card.hidden = true;
    });
  });
})();
