[![GitHub license](https://img.shields.io/github/license/rafsaf/fastapi-plan)](https://github.com/rafsaf/fastapi-plan/blob/master/LICENSE)
![PyPI](https://img.shields.io/pypi/v/fastapi-plan)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-plan)
![tests](https://github.com/rafsaf/fastapi-plan/actions/workflows/tests.yml/badge.svg)

Dead simple but powerful template manager for FastAPI applications.

- [About](#about)
- [Quickstart](#quickstart)
  - [Initialization](#0-initialization)
  - [Development](#1-development)
  - [Debug (http)](#2-debug-http)
  - [Production (https)](#3-production-https-own-domain)
- [Project structure](#project-structure)
- [High level overview](#high-level-overview)
- [How to add new endpoint (step by step)](#how-to-add-new-endpoint)

## About

Features:

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

Furthermore:

- full [project structure schema](#project-structure)
- [high level overview](#high-level-overview) how this project is organised and why, questions like where do the settings live or what every variable in `.env` file is used for
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

Plesae also note that to get no-test certificate, you should comment line `"--certificatesresolvers.myresolver.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"` in `docker-compose.prod.yml` file, by default you will use test certifactes (to be sure that everything works, there are some hard limits on number of certifiactes you can ask per week!). You should comment line `"--log.level=DEBUG"` also (but it can be useful when debugging traefik). There would probably be problems anyway, just be sure that everything works via http using **2. DEBUG** apropach. If it then doesn't with the https, you should refer to traefik docs.

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

This project strucutre is mostly based on the [official template](#https://github.com/tiangolo/full-stack-fastapi-postgresql) (but not only) which is really great but unfortunatly does not support Tortoise ORM and is... (too?) complicated. All the security or problematic stuff (`app/core/security.py` with `verify_password` function, login and token routes, JWT token schemas) are just copied from there, so you can be pretty sure it will work as expected.

The main thougts are:

- There two sorts of settings, first one located in `.env` file for the ENTIRE project, and python-specific settings which lives in `app/core/config.py`, the file is based on pydantic solution (using dotenv lib). Why? Well, that's simple, this is due to [12factor methodology](https://12factor.net/), python-specific settings inherit from `.env` file, so this is the only place where you actually change something. If you have any problems understanding mentioned `config.py` file, just refer to [pydantic - settings management](https://pydantic-docs.helpmanual.io/usage/settings/), it's pretty clear.

- Models, crud, schemas, api routes, tests... it might be confusing how to actually ADD SOMETHING NEW here, but after following next section (learn by doing, step by step), it should be pretty easy

- Database-related stuff is very convinient, taken mostly from [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/index.html) docs and just _working_. There is `register_tortoise` function in `main.py`, `TORTOISE_ORM` variable in `app/core/config.py`. Please, be aware that if you don't run `initial_data.py` SOMEHOW (in development- you have to do it yourself, in debug/production it is handled by shell script `initial.sh`, which also runs tests and migrations), you won't be able to connect to database. `initial_data.py` is hearbly based on the same named file in **official template** mentioned earlier. It has two responsibilities, first is running `init` function from Tortoise to initialize connection, and the second - creating first superuser (defined in `.env`) if one doesn't yet exists.

- Migrations are also provided by Tortiose (the tool is aerich), docs can be found [here in aerich repo](https://github.com/tortoise/aerich). The default migration (default user model) file is already included. After changes in models (e.g. new model `Cars`), just run `aerich migrate`, `aerich upgrade` and you are good to go.

- All tests lives in `tests` folder, with some pytest-specific content included. If you feel unconfortable with pytest, feel free to read articles about using it, and if you just want to see how to test new enpoints/models, just read next section.

## How to add new endpoint

Let's imagine we need to create API for a website where users brag about their dogs... or whatever, they just can crud dogs in user panel for some reason. We will add dummy model `Dog` to our API, with relation to the default table `User` and crud auth endpoints, then test it shortly.

1. Create file `dog.py` in `app/models` folder:

```python
from tortoise import fields
from tortoise.models import Model


class Dog(Model):
    name = fields.CharField(max_length=100)
    age = fields.IntField(null=True, default=None)
    breed = fields.CharField(max_length=100, null=True, default=None)
    owner = fields.ForeignKeyField("models.User", related_name="dogs")
```

2. Add import in `app/models.__init__.py`:

```python
from .dog import Dog # type: ignore
```

3. Migrate changes

```bash
aerich migrate
aerich upgrade
```

4. Create file `dog.py` in `app/schemas` folder (pydantic schemas with typing support):

```python
from typing import Optional
from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import (
    pydantic_model_creator,
    pydantic_queryset_creator,
)
from pydantic import BaseModel
from app.models import Dog


# Pydantic models from Tortoise models, pls refer
# https://tortoise-orm.readthedocs.io/en/latest/examples/pydantic.html#basic-pydantic

Tortoise.init_models(["app.models"], "models")
DogPydantic = pydantic_model_creator(Dog, exclude=("owner",))
DogPydanticList = pydantic_queryset_creator(Dog, exclude=("owner",))

# Unfortunately, it doesn't work the other way around


class DogCreate(BaseModel):
    name: str
    age: Optional[int]
    breed: Optional[str]


class DogUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    breed: Optional[str]

```

5. Add import in `app/schemas.__init__.py`:

```python
from .dog import DogUpdate, DogCreate, DogPydantic, DogPydanticList # type: ignore
```

6. Create `crud_dog.py` in `app/crud` folder

```python
from app.schemas import DogCreate, DogUpdate
from app.crud.base import CRUDBase
from app.models import Dog, User


class CRUDDog(CRUDBase[Dog, DogCreate, DogUpdate]):
    def get_dogs_by_user(self, user: User, skip: int = 0, limit: int = 100):
        return Dog.filter(owner=user).offset(offset=skip).limit(limit=limit)

    async def create_dog_me(self, dog_in: DogCreate, user: User):
        new_dog = await Dog.create(
            name=dog_in.name, age=dog_in.age, breed=dog_in.breed, owner=user
        )
        return new_dog

    async def get_by_id_and_user(self, dog_id: int, user: User):
        return await Dog.get(id=dog_id, owner=user)

    async def remove_all_user_dogs(self, user: User):
        await Dog.filter(owner=user).delete()
        return


dog = CRUDDog(Dog)

```

7. Add import in `app/crud.__init__.py`:

```python
from .crud_dog import dog # type: ignore
```

8. Create `dogs.py` with endpoints in `app/api/routers` folder

```python
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, models, schemas
from app.api import deps
from app.models import Dog

router = APIRouter()


@router.get("/{dog_id}", response_model=schemas.DogPydantic)
async def read_dog(
    dog_id: int,
):
    dog = await crud.dog.get(dog_id)
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The dog does not exist in the system",
        )
    return await schemas.DogPydantic.from_tortoise_orm(dog)


@router.post(
    "/", response_model=schemas.DogPydantic, status_code=status.HTTP_201_CREATED
)
async def create_dog_me(
    dog_in: schemas.DogCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    dog: Dog = await crud.dog.create_dog_me(dog_in, current_user)
    return await schemas.DogPydantic.from_tortoise_orm(dog)


@router.put("/", response_model=schemas.DogPydantic)
async def update_dog_me(
    dog_id: int,
    dog_in: schemas.DogUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    dog = await crud.dog.get_by_id_and_user(dog_id, current_user)
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The dog does not exist in the system",
        )
    new_dog = await crud.dog.update(dog, dog_in)
    return await schemas.DogPydantic.from_tortoise_orm(new_dog)


@router.delete("/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_dog_me(
    dog_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    dog = await crud.dog.get_by_id_and_user(dog_id, current_user)
    if not dog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The dog does not exist in the system",
        )
    await crud.dog.remove(dog_id)
    return None


@router.delete("/all", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_dogs_me(
    current_user: models.User = Depends(deps.get_current_active_user),
):
    await crud.dog.remove_all_user_dogs(current_user)
    return None


@router.get("/all", response_model=schemas.DogPydanticList)
async def read_all_dogs_me(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    dogs = crud.dog.get_dogs_by_user(current_user, skip, limit)
    return await schemas.DogPydanticList.from_queryset(dogs)


@router.get("/all/{user_id}", response_model=schemas.DogPydanticList)
async def read_all_dogs(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
):
    user = await crud.user.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not exist",
        )
    dogs = crud.dog.get_dogs_by_user(user, skip, limit)

    return await schemas.DogPydanticList.from_queryset(dogs)

```

9. Finally add those enpoints to the app with label "dogs", add this line in `app/api/api.py` file:

```python
api_router.include_router(dogs.router, prefix="/dogs", tags=["dogs"])
```

10. API endpoints are ready to go, you can play with them at `localhost:8000` by default

11. Now we gonna create tests for crud and endpoints, let's first create utils for dog model (we can use it in multiple places in tests then), add `dog.py` in `app/tests/utils` folder:

```python
from asyncio import AbstractEventLoop as EventLoop
from app import models
import app.tests.utils.utils as utils


def create_random_dog(user: models.User, event_loop: EventLoop) -> models.Dog:
    name = utils.random_lower_string()
    breed = utils.random_lower_string()
    age = utils.random_integer_below_100()
    dog: models.Dog = event_loop.run_until_complete(
        models.Dog.create(name=name, breed=breed, age=age, owner=user)
    )
    return dog
```

12. Then add `test_dog.py` in `app/tests/crud` folder:

```python
import pytest
from asyncio import AbstractEventLoop as EventLoop
from typing import List
from app import crud, models, schemas
from app.tests.utils.utils import (
    random_lower_string,
    random_integer_below_100,
)
from app.tests.utils.dog import create_random_dog


@pytest.fixture(autouse=True)
def drop_dogs(event_loop: EventLoop) -> None:
    yield
    event_loop.run_until_complete(models.Dog.all().delete())


def test_get_dogs_by_user(event_loop: EventLoop, normal_user: models.User):

    dog0 = create_random_dog(normal_user, event_loop)
    dog1 = create_random_dog(normal_user, event_loop)
    dog_lst: List[models.Dog] = list(
        event_loop.run_until_complete(crud.dog.get_dogs_by_user(normal_user))
    )

    assert len(dog_lst) == 2
    assert dog_lst[0].name == dog0.name
    assert dog_lst[1].name == dog1.name
    assert dog_lst[0].age == dog0.age
    assert dog_lst[1].age == dog1.age
    assert dog_lst[0].breed == dog0.breed
    assert dog_lst[1].breed == dog1.breed


def test_create_dog_me(event_loop: EventLoop, normal_user: models.User):
    name = random_lower_string()
    breed = random_lower_string()
    age = random_integer_below_100()
    dog_in = schemas.DogCreate(name=name, breed=breed, age=age)
    dog: models.Dog = event_loop.run_until_complete(
        crud.dog.create_dog_me(dog_in, normal_user)
    )

    assert dog.name == name
    assert dog.breed == breed
    assert dog.age == age
    assert dog.owner == normal_user


def test_get_dog_by_user(event_loop: EventLoop, normal_user: models.User):

    dog0 = create_random_dog(normal_user, event_loop)

    dog: models.Dog = event_loop.run_until_complete(
        crud.dog.get_by_id_and_user(dog0.pk, normal_user)
    )
    assert dog == dog0


def test_remove_all_user_dogs(event_loop: EventLoop, normal_user: models.User):

    create_random_dog(normal_user, event_loop)
    create_random_dog(normal_user, event_loop)
    dog_number0: int = event_loop.run_until_complete(
        models.Dog.filter(owner=normal_user).count()
    )
    assert dog_number0 == 2
    event_loop.run_until_complete(crud.dog.remove_all_user_dogs(normal_user))
    dog_number1: int = event_loop.run_until_complete(
        models.Dog.filter(owner=normal_user).count()
    )
    assert dog_number1 == 0
```

13. And then `test_dogs.py` for endpoints in `app/tests/api` folder
