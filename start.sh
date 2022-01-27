#!/bin/sh
python manage.py migrate &&\
exec gunicorn dboeannotation.wsgi