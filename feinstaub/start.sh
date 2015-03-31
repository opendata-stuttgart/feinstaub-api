#!/bin/bash
export DJANGO_SETTINGS_MODULE=feinstaub.settings.production
export PYTHONUNBUFFERED=0
mkdir -p /home/uid1000/feinstaub
mkdir -p /home/uid1000/feinstaub/logs
mkdir -p /home/uid1000/feinstaub/run
chmod -R 777 /home/uid1000/feinstaub/run
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn feinstaub.wsgi:application --log-level=info --bind=unix:/home/uid1000/feinstaub/run/server.sock
