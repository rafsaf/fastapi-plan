from app.schemas.user import UserCreateBySuperuser
import pytest
from asyncio import AbstractEventLoop as EventLoop
from typing import Generator
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer
from app.main import create_app
from app.tests.utils.utils import user_authentication_headers

app = create_app()

default_superuser = UserCreateBySuperuser(
    email="admin@admin.com",
    password="admin",
    is_superuser=True,
    is_active=True,
)

default_user = UserCreateBySuperuser(
    email="user@user.com",
    password="user",
    is_superuser=False,
    is_active=True,
)


@pytest.fixture(scope="module")
def client() -> Generator:
    initializer(["app.models"])
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient, event_loop: EventLoop) -> Generator:
    headers = user_authentication_headers(
        client=client,
        event_loop=event_loop,
        email=default_superuser.email,
        password=default_superuser.password,
        is_superuser=default_superuser.is_superuser or True,
        is_active=default_superuser.is_active or True,
    )
    yield headers


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, event_loop: EventLoop) -> Generator:
    headers = user_authentication_headers(
        client=client,
        event_loop=event_loop,
        email=default_user.email,
        password=default_user.password,
        is_superuser=default_user.is_superuser or False,
        is_active=default_user.is_active or True,
    )
    yield headers
