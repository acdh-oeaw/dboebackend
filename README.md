# dboebackend

REST-Service to expose, curate and enrich DBÖ-Belegzettel

## About

REST service to create collections from documents coming from elasticsearch index and annotate them.
Service also handles the authentication and user management system.

## Technical setup

The application is implemented using Python, [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/).
It stores the data in PostgreSQL database using PostgreSQL's native XML field to store TEI/XML modelled Belegzettel.

### install

The project uses [uv](https://docs.astral.sh/uv/).

- clone the repo
- create a PostgreSQL database `dboebackend`
- provide database credentials e.g. via

```shell
DATABASE_URL=postgres://dboeannotation:dboeannotation@localhost:5432/dboeannotation
```

- run the usual django-commands

```shell
uv run manage.py migrate
uv run manage.py runserver
```

### data import

In case you have access to the DBOE-TEI/XML files you can populate the database by adapting [belege/management/commands/import.py](belege/management/commands/import.py) and running

```shell
uv run manage.py import
```

After this is done, run

```shell
uv run manage.py update
```

## implementation details

### XMLField

The project implements a custom [XMLField](belege/fields.py) to store valid XML data into PostgreSQL's XML Field. This ensures well formed XML snippets.

### custom properties for models fields

It is possible to declare custom properties to Django's model fields, e.g. like

```python
definition = models.TextField(
    blank=True, null=True, verbose_name="definition"
).set_extra(xpath="./tei:def", node_type="text")
```

### customized save methods for some classes

The classes `Belege` and `Citation` have customized save methods. On save, given some parameters are set, information from the XMLField are extracted and saved in their respective fields.

## Docker

### building the image

```shell
docker build -t dboeannotation:latest .
```

### running the image

```shell
docker run -it --network="host" --rm --env-file .env dboeanntoation:latest
```
