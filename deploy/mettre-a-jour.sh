#!/usr/bin/env bash
# Mise à jour du serveur après un push sur GitHub : sudo /opt/maxquiz/deploy/mettre-a-jour.sh
set -euo pipefail
cd /opt/maxquiz
sudo -u maxquiz git pull --ff-only
sudo -u maxquiz .venv/bin/pip install -q -r requirements.txt
sudo -u maxquiz bash -c 'set -a; . /etc/maxquiz.env; set +a; .venv/bin/python manage.py migrate --noinput && .venv/bin/python manage.py collectstatic --noinput'
systemctl restart maxquiz
echo "MaxQuiz à jour : $(git log -1 --format='%h %s')"
