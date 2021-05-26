[![GitHub license](https://img.shields.io/github/license/rafsaf/fastapi-plan)](https://github.com/rafsaf/fastapi-plan/blob/master/LICENSE)
![PyPI](https://img.shields.io/pypi/v/fastapi-plan)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-plan)
![tests](https://github.com/rafsaf/fastapi-plan/actions/workflows/tests.yml/badge.svg)

## About

dead simple but powerful template manager for FastAPI applications.

features:
- postgresql database with [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/index.html) as ORM
- well organised, rock solid project structure (see section [Project structure](#project-structure))
- ready-to-use user model, authentiaction system (JWT), hashing with Bcrypt
- easy to undarstand config.py with settings (there is only one file for changes: `.env`)
- out-of-the-box well-tested routes for login and user (register, read, read_me, update etc.)
- aerich for migrations
- well-designed tests folder filled with tests for existing user model/user endpoints
- auto-generated strong passwords for database, secret_key and superuser password
- poetry or pip
- deployment ready docker-compose.prod.yml file with poetry, you will only need own domain

furthermore:
- step by step explanation how to add new endpoint in this README, from creating new model, adding schemas and routes to writting tests after (it's always better to have it and optionally adopt it than wasting time trying to guess the best dev path)


## Quickstart

NOTE: you will need [docker](https://www.docker.com/get-started) and optional but recommended [poetry](https://python-poetry.org/docs/) installed!

install via pip (or poetry) **globally**:

```bash
pip install fastapi-plan
```

there are 3 docker-compose files available, one for development, one for running project via http, and the last one is for production with enabled https using traefic as a proxy (and letsencrypt for ssl), steps to initialize new project are the same for every approach, you can then choose from 1-3.

### 0. INITIALIZATION

initialize new FastAPI project:

```bash
fastapi-plan
```

enter project_name and other information and after project is ready, `cd project_name` and continue installing dependencies:

```bash
poetry install

# optional if you selected "requirements.txt" (with venv installed)
pip install -r requirements.txt
```

### 1. DEVELOPMENT


since we wanna use uvicorn in development, create only postgres container using docker-compose.yml file like that:

```bash
docker-compose up -d
```

now run aerich migrations and configure tortoise (and add first superuser)

```bash
aerich upgrade
python app/initial_data.py
```

finally you can run this command to start uvicorn server

```bash
uvicorn app.main:app --reload
```

### 2. DEBUG (http)

To make it available from http://localhost on your local machine or http://your-host-name on VM just run

```bash
docker-compose -f docker-compose.debug.yml up -d
```

The diffrence between development approach is that web server automatically runs aerich and initial_data.py using shell script (`app/initial.sh`), so you don't have to do anything except changing some lines in `.env` file:

1. `PROJECT_NAME` - it will show up in docs view as a name of project.
2. `FIRST_SUPER_USER_EMAIL` - first account email
3. `DEBUG` - when it's false, the `POSTGRES_SERVER` is set to `localhost` for development, so change it to `DEBUG=true` to use `db` postgres server.

  
### 3. PRODUCTION (https, own domain)

To make it available from https://your_domain.com on VM run

```bash
docker-compose -f docker-compose.prod.yml up -d
```

The diffrence between development approach is that web server automatically runs aerich and initial_data.py using shell script (`app/initial.sh`), so you don't have to do anything except changing some lines in `.env` file:

1. `PROJECT_NAME` - it will show up in docs view as a name of project.
2. `FIRST_SUPER_USER_EMAIL` - first account email
3. `DEBUG` - when it's false, the `POSTGRES_SERVER` is set to `localhost` for development, so change it to `DEBUG=true` to use `db` postgres server.
4. `DEFAULT_FROM_EMAIL` - your private email for ssl purposes, e.g. they will inform you shortly after some problems with you certificate.
5. `MAIN_DOMAIN` - your own domain e.g. `example.com`

Plesae also note that to get no-test certificate, you should comment line `"--certificatesresolvers.myresolver.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"` in `docker-compose.prod.yml` file, by default you will use test certifactes (to be sure that everything works, there are some hard limits on number of certifiactes you can ask per week! You should comment line `"--log.level=DEBUG"` also (but it can be useful when debugging traefik). There would probably be problems anyway, just be sure that everything works via http using **2. DEBUG** apropach. If it then doesn't with https, you should refer to traefik docs.

## Project structure

```
|── app
|    ├── api                              # endpoints/dependecies
|    |
|    ├── core                             # settings and security algorithms
|    |
|    ├── crud                             # CRUD operations
|    |
|    ├── migrations                       # for aerich migrations
|    |
|    ├── models                           # tortoise models
|    |
|    ├── schemas                          # pandatic schemas
|    |
|    ├── tests                            # tests
|    |
|    ├── initial.sh                       # initial shell script used by docker
|    ├── initial_data.py                  # init database and add first superuser
|    ├── main.py                          # main fastapi application file
|
├── config                                # nginx server config file
|
├── .env                                  # .env file with settings
|
├── Dockerfile                            # dockerfile for web app
|
├── aerich.ini                            # aerich (migrations) configuration
|
├── docker-compose.prod.yml               # puts it all together in prod (https)
|
├── docker-compose.debug.yml              # puts it all together in debug (http)
|
├── docker-compose.yml                    # puts it all together (development)
|
├── (optional) pyproject.toml             # python dependencies (poetry)
|
├── (optional) poetry.lock                # python dependencies (poetry)
|
├── requirements.txt                      # python dependencies (pip)
```
