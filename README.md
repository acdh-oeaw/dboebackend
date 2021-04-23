# DBÖ Annotation REST Service

## About

REST service to create collections from documents coming from elasticsearch index and annotate them.
Service also handles the authentication and user management system.

## Technical setup

The application is implemented using Python, [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/).
It stores the data in PostgreSQL database.

Use `pipenv install` to get all dependencies.
The installed environment can be selected for example in Visual Studion Code.

If you want to save local environment settings use a `.env` file in `dboeannotation/settings`
For example

```bash
DATABASE_URL=postgres://dboeannotation:dboeannotation@localhost:5432/dboeannotation
```

If you don't set a `DATABASE_URL` a sqlite3 database will be used (`db.sqlite3`)

We do not git migrations. A database is updated using ad-hoc migrations which are generated using

```bash
python manage.py makemigrations
python manage.py migrate
```

## Recognized environment variables and defaults

```bash
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
DJANGO_SECRET_KEY=random string generated on start,
DJANGO_CORS_ORIGIN_WHITELIST=('127.0.0.1','127.0.0.1:8080','localhost:8000','localhost:8080')
DATABASE_URL=sqlite:///$(pwd)/db.sqlite3
```
