#!/bin/bash
export DJANGO_SETTINGS_MODULE=feinstaub.settings.production
export PYTHONUNBUFFERED=0
mkdir -p /home/uid1000/feinstaub
mkdir -p /home/uid1000/feinstaub/logs
mkdir -p /home/uid1000/feinstaub/run
python3 manage.py migrate
python3 manage.py collectstatic --noinput
uwsgi --socket /home/uid1000/feinstaub/run/server.sock --wsgi-file /opt/code/feinstaub/feinstaub/wsgi.py --master --processes 4 --threads 2