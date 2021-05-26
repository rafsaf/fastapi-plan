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
- full [project structure schema](#project-structure)
- [high level overview](#high-level-overview) how this project is organised and why, questions like where do the settings live or what every variable in `.env` file 
- step by step explanation [how to add new endpoint](#how-to-add-new-endpoint), from creating new model, adding schemas and routes to migrating database and writting tests (it's always better to have it and optionally adopt it, than wasting time trying to figure out the best dev path)


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

## High level overview

This project strucutre is mostly based on [official template](#https://github.com/tiangolo/full-stack-fastapi-postgresql) (but not only) which is really great but unfortunatly does not support Tortoise ORM and is... (too?) complicated. All the security or problematic stuff (`app/core/security.py` with `verify_password` function, login and token routes, JWT token schemas) are just copied from there, so you can be preety sure it will work as expected.

The main thougts are:

- There two sorts of settings, first one located in `.env` file for ENTIRE project, and python-specific settings which lives in `app/core/config.py`, it's based on pydantic docs (using dotenv lib). Why? Well, that's simple, this is due to [12factor methodology](https://12factor.net/), python-specific settings inheritance from `.env` file, so this is the only place where you actually change something. If you have any problems how to understand mentioned `config.py` file, just refer to [pydantic - settings management](https://pydantic-docs.helpmanual.io/usage/settings/), it's preety clear.

- Models, crud, schemas, api routes, tests... it might be confusing how to actually ADD SOMETHING NEW here, but after following next section (learn by doing, step by step), it should be pretty easy

- Database-related stuff is very convinient, taken mostly from [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/index.html) docs and just *working*. There is `register_tortoise` function in `main.py`, defined `TORTOISE_ORM` variable in `app/core/config.py`. Please, be aware that if you don't run `initial_data.py` SOMEHOW (in development- you have to do it yourself, in debug/production it is handled by shell script `initial.sh`, which also runs tests and migrations). `initial_data.py` is hearbly based on the same named file in **official template** mentioned earlier. It has two responsibilities, first is running `init` function from Tortoise to initialize connection, and the second - creating first superuser (defined in `.env`) if one doesn't yet exists.

- Migrations are also provided by Tortiose (the tool is aerich), docs can be found [here in aerich repo](https://github.com/tortoise/aerich). The default migration (default user model) file is already included. After changes in models (e.g. new model `Cars`), just run `aerich migrate`, `aerich upgrade` and you are good to go.

- All tests lives in `tests` folder, with some pytest-specific content included. If you feel unconfortable with pytest, feel free to read articles about using it, and if you just want to see how to test new enpoints/models, just read next section.

## How to add new endpoint