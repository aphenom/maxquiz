"""Version du service worker : elle change à chaque mise à jour du code.

Le service worker garde une copie des CSS et JS sur les téléphones ; quand son numéro
de version change, il jette l'ancienne copie. On combine APP_VERSION (réglage manuel)
avec une empreinte des fichiers statiques (chemins, tailles, dates), pour que chaque
mise à jour arrive sur les téléphones sans changer APP_VERSION à la main.
"""
import hashlib
import os

from django.conf import settings

_EMPREINTE = None


def static_version():
    global _EMPREINTE
    if _EMPREINTE is None:
        h = hashlib.sha1()
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        for folder, _dirs, files in sorted(os.walk(root)):
            for name in sorted(files):
                st = os.stat(os.path.join(folder, name))
                h.update(f"{os.path.relpath(folder, root)}/{name}:{st.st_size}:{int(st.st_mtime)}".encode())
        _EMPREINTE = h.hexdigest()[:10]
    return _EMPREINTE


def sw_version():
    return f"{getattr(settings, 'APP_VERSION', '1')}-{static_version()}"
