# Welcome to Dockerized Django with Postgres and frontends

This repository is based on the work of https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

## How to run this project

Main requirements

- install the last stable python (3.7.4 when this was written)
- install pipenv
- install Docker

```bash
$ git clone https://github.com/miquelnez/django-js-fullstack-with-docker.git django-fullstack
$ cd django-fullstack
$ docker-compose down -v
$ docker-compose up -d --build
$ docker-compose exec web python manage.py migrate --noinput
```

## How this Project was Set up

- install pipenv
- install Docker

```bash
$ mkdir django-on-docker && cd django-on-docker
$ mkdir app && cd app
$ pipenv install django==2.2.5
$ pipenv install django-safedelete
$ pipenv shell
(app)$ django-admin.py startproject hello_django .
(app)$ python manage.py migrate
(app)$ python manage.py runserver
```

It should be working on http://localhost:8000/

## Setup Docker

```bash
(app)$ deactivate # exits from the current pipenv
$ vim app/Dockerfile
```

fill the app/Dockerfile like this:

```bash
# pull official base image
FROM python:3.7.4-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 # python -B
ENV PYTHONUNBUFFERED 1 # python -u

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY . /usr/src/app/
```

Then add a docker-compose.yml to the project root (edit the services/web/environment/SECRET_KEY value with the one on app/hello_django/settings.py ):

```bash
$ vim docker-compose.yml
```

```bash
version: '3.7'

services:
  web:
    build: ./app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./app/:/usr/src/app/
    ports:
      - 8000:8000
    environment:
      - DEBUG=1
      - SECRET_KEY=foo
```

Go to app/hello_django/settings.py and edit the SECRET_KEY, DEBUG and ALLOWED_HOSTS values

```bash
$ vim app/hello_django/settings.py
```

```bash
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = int(os.environ.get('DEBUG', default=0))

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

Build the image and once the image is built, run the container:

```bash
$ docker-compose build
$ docker-compose up -d
```

If everything was ok, you should be able to go to http://localhost:8000/

## Setup Postgres

To configure Postgres, we'll need to add a new service (db) to the docker-compose.yml file, update the Django settings (with the new database based on this env values), and install Psycopg2.

```bash
$ vim docker-compose.yml
```

```bash
version: '3.7'

services:
  web:
    build: ./app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./app/:/usr/src/app/
    ports:
      - 8000:8000
    environment:
      - DEBUG=1
      - SECRET_KEY=foo
      - SQL_ENGINE=django.db.backends.postgresql
      - SQL_DATABASE=hello_django_dev
      - SQL_USER=hello_django
      - SQL_PASSWORD=hello_django
      - SQL_HOST=db
      - SQL_PORT=5432
    depends_on:
      - db
  db:
    image: postgres:11.5-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=hello_django
      - POSTGRES_PASSWORD=hello_django
      - POSTGRES_DB=hello_django_dev

volumes:
  postgres_data:
```

To persist the data beyond the life of the container we configured a volume. This config will bind _postgres_data_ to the "/var/lib/postgresql/data/" directory in the container.

Remember to edit the django settings.py to use this database

```bash
$ vim app/hello_django/settings.py
```

```bash
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}
```

The next step is to update the app/Dockerfile to install the appropriate packages along with Psycopg2:

```bash
$ vim app/Dockerfile
```

fill the app/Dockerfile like this:

```bash
# pull official base image
FROM python:3.7.4-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 # python -B
ENV PYTHONUNBUFFERED 1 # python -u

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY . /usr/src/app/
```

Finally, build the new image and spin up the two containers and do the migrations:

```bash
$ docker-compose up -d --build
$ docker-compose exec web python manage.py migrate --noinput
```

You should get something like this:

```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK
```

If you get and error **django.db.utils.OperationalError: FATAL: database "hello_django_dev" does not exist** then try to remove the docker volumes first:

```bash
$ docker-compose down -v
$ docker-compose build
$ docker-compose up -d
# or use docker-compose up -d --build
$ docker-compose exec web python manage.py migrate --noinput
```

You can also enter on the database to check if all is ok (but don't edit any schema):

```bash
docker-compose exec db psql --username=hello_django --dbname=hello_django_dev
WARNING: The b_jgc variable is not set. Defaulting to a blank string.
psql (11.5)
Type "help" for help.

hello_django_dev=# \l
                                          List of databases
       Name       |    Owner     | Encoding |  Collate   |   Ctype    |       Access privileges
------------------+--------------+----------+------------+------------+-------------------------------
 hello_django_dev | hello_django | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres         | hello_django | UTF8     | en_US.utf8 | en_US.utf8 |
 template0        | hello_django | UTF8     | en_US.utf8 | en_US.utf8 | =c/hello_django              +
                  |              |          |            |            | hello_django=CTc/hello_django
 template1        | hello_django | UTF8     | en_US.utf8 | en_US.utf8 | =c/hello_django              +
                  |              |          |            |            | hello_django=CTc/hello_django
(4 rows)

hello_django_dev=# \c hello_django_dev
You are now connected to database "hello_django_dev" as user "hello_django".
hello_django_dev=# \dt
                     List of relations
 Schema |            Name            | Type  |    Owner
--------+----------------------------+-------+--------------
 public | auth_group                 | table | hello_django
 public | auth_group_permissions     | table | hello_django
 public | auth_permission            | table | hello_django
 public | auth_user                  | table | hello_django
 public | auth_user_groups           | table | hello_django
 public | auth_user_user_permissions | table | hello_django
 public | django_admin_log           | table | hello_django
 public | django_content_type        | table | hello_django
 public | django_migrations          | table | hello_django
 public | django_session             | table | hello_django
(10 rows)

hello_django_dev=# \q
```

Also, we can check that our database volume was created

```bash
$ docker volume inspect django-on-docker_postgres_data
[
    {
        "CreatedAt": "2019-09-08T19:14:18Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "django-on-docker",
            "com.docker.compose.version": "1.23.2",
            "com.docker.compose.volume": "postgres_data"
        },
        "Mountpoint": "/var/lib/docker/volumes/django-on-docker_postgres_data/_data",
        "Name": "django-on-docker_postgres_data",
        "Options": null,
        "Scope": "local"
    }
]
```

Next, add an entrypoint.sh file to the "app" directory to verify that Postgres is healthy before applying the migrations and running the Django development server:

```bash
$ vim app/entrypoint.sh
```

```bash
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"
```

And update the file permissions locally to allow it to be executed:

```bash
$ chmod +x app/entrypoint.sh
```

Then, we should update the Dockerfile to copy over the entrypoint.sh file and run it as the Docker entrypoint command:

```bash
$ vim app/Dockerfile
```

```bash
# pull official base image
FROM python:3.7.4-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 # python -B
ENV PYTHONUNBUFFERED 1 # python -u

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
```

And finnaly, we only need to add the database to our docker-compose

Add the DATABASE environment variable to docker-compose.yml:

```bash
$ vim docker-compose.yml
```

```bash
version: '3.7'

services:
  web:
    build: ./app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./app/:/usr/src/app/
    ports:
      - 8000:8000
    environment:
      - DEBUG=1
      - SECRET_KEY=foo
      - SQL_ENGINE=django.db.backends.postgresql
      - SQL_DATABASE=hello_django_dev
      - SQL_USER=hello_django
      - SQL_PASSWORD=hello_django
      - SQL_HOST=db
      - SQL_PORT=5432
      - DATABASE=postgres
    depends_on:
      - db
  db:
    image: postgres:11.5-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=hello_django
      - POSTGRES_PASSWORD=hello_django
      - POSTGRES_DB=hello_django_dev

volumes:
  postgres_data:
```

If everything was correct, we should be able to rebuild our images and work on http://localhost:8000/

```bash
$ docker-compose down -v
$ docker-compose up -d --build
$ docker-compose exec web python manage.py migrate --noinput
```
