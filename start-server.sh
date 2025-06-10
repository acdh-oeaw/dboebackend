#!/usr/bin/env bash
echo "Hello from Project dboeannotation"
uv run manage.py collectstatic --no-input
echo "running migrations"
uv run manage.py migrate --no-input
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (echo "creating superuser ${DJANGO_SUPERUSER_USERNAME}" && uv run manage.py createsuperuser --no-input --noinput --email 'blank@email.com')
fi
uv run gunicorn dboeannotation.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 & nginx -g "daemon off;"