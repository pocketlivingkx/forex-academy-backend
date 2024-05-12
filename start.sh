#!/bin/sh

. /app/.env
echo $DJANGO_SETTINGS_MODULE
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:80 -w 4 --limit-request-line 6094 --access-logfile - src.wsgi:application
exec "$@"
