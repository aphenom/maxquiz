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

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function ssGet(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function ssSet(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  var JOUR = 24 * 3600 * 1000;

  document.addEventListener('DOMContentLoaded', function () {
    var connecte = document.body && document.body.getAttribute('data-mq-auth') === '1';
    if (!connecte || !window.maxquizPushSupported()) return;

    // 1. Autorisation déjà donnée (application Android jusqu'à Android 12, nouveau compte sur le
    //    même téléphone, réinstallation…) : on abonne l'appareil sans rien demander, une fois par visite.
    if (Notification.permission === 'granted') {
      if (!ssGet('mq-push-sync')) { ssSet('mq-push-sync', '1'); window.maxquizEnablePush(); }
      return;
    }
    if (Notification.permission !== 'default') return;          // refusé : on ne harcèle pas

    // 2. Dans l'application installée : la demande s'affiche au premier toucher de l'écran
    //    (le téléphone l'exige), au plus une fois par jour tant que l'élève n'a pas répondu.
    var appli = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone
      || ssGet('mqInApp') === '1' || document.referrer.indexOf('android-app://') === 0;
    if (appli && Date.now() - (parseInt(lsGet('mq-push-asked') || '0', 10) || 0) > JOUR) {
      var ask = function () {
        document.removeEventListener('click', ask, true);
        lsSet('mq-push-asked', String(Date.now()));
        window.maxquizEnablePush();
      };
      document.addEventListener('click', ask, true);
      return;
    }

    // 3. Dans le navigateur : carte « Activer », proposée de nouveau 3 jours après « Plus tard ».
    var card = document.querySelector('[data-push-card]');
    if (!card) return;
    if (Date.now() < (parseInt(lsGet('mq-push-later') || '0', 10) || 0)) return;
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
      lsSet('mq-push-later', String(Date.now() + 3 * JOUR));
      card.hidden = true;
    });
  });
})();
