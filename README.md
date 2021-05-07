# Project description

[![GitHub license](https://img.shields.io/github/license/rafsaf/fastapi-plan)](https://github.com/rafsaf/fastapi-plan/blob/master/LICENSE)
![PyPI](https://img.shields.io/pypi/v/fastapi-plan)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-plan)
![example workflow](https://github.com/rafsaf/fastapi-plan/actions/workflows/python-package.yml/badge.svg)

## about

dead simple but powerful template manager for FastAPI applications.

## quickstart

NOTE: you will need [docker](https://www.docker.com/get-started) and optional but recommended [poetry](https://python-poetry.org/docs/) installed!

install via pip (or poetry):

```bash
pip install fastapi-plan
```

initialize new FastAPI project:

```bash
fastapi-plan
```

enter project name and other information and after noticing SUCCESS your project is ready, enter project with `cd project_name` and continue installing dependencies:

```bash
poetry install

# optional if you selected "requirements.txt" (with venv installed)
pip install -r requirements.txt
```

since we wanna use uvicorn in development, create only postgres container using docker-compose:

```bash
docker-compose up -d db
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

## short project structure

```
|── app
|    ├── api                                 # endpoints/dependecies
|    |
|    ├── core                                # settings and security algorithms
|    |
|    ├── crud                                # CRUD operations
|    |
|    ├── migrations                          # for aerich migrations
|    |
|    ├── models                              # tortoise models
|    |
|    ├── schemas                             # pandatic schemas
|    |
|    ├── tests                               # tests
|    |
|    ├── initial.sh                          # initial shell script used by docker
|    ├── initial_data.py                     # init database and add first superuser
|    ├── main.py                             # main fastapi application file
|
├── config                                   # nginx server config file
|
├── .env                                     # .env file with settings
|
├── Dockerfile                               # dockerfile for web app
|
├── aerich.ini                               # aerich (migrations) configuration
|
├── docker-compose.yml                       # puts it all together
|
├── pytest.ini                               # Pytest configurations
|
├── pyproject.toml                           # python dependencies (poetry)
|
├── poetry.lock                              # python dependencies (poetry)
|
├── (optional) requirements.txt              # python dependencies (pip)
```

## why such a structure of the project
