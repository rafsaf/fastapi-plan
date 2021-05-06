import pytest
from app.schemas.user import UserUpdateBySuperuser, UserUpdateMe
from asyncio import AbstractEventLoop as EventLoop
from fastapi.testclient import TestClient
from app.models import User
from app import crud
from app.schemas import UserCreateMe, UserCreateBySuperuser
from app.tests.utils.utils import random_email, random_lower_string
from app.core.security import verify_password
import logging


logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
async def drop() -> None:
    yield
    await User.all().delete()


def test_user_create_me(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateMe(email=email, password=password)
    user = event_loop.run_until_complete(crud.user.create_me(user_in))

    assert user.email == email
    assert hasattr(user, "password_hash")
    assert user.is_superuser == False


def test_user_create_by_superuser(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password = random_lower_string()
    is_superuser = True
    is_active = False
    user_in = UserCreateBySuperuser(
        email=email,
        password=password,
        is_superuser=is_superuser,
        is_active=is_active,
    )
    user = event_loop.run_until_complete(crud.user.create_by_superuser(user_in))
    assert user.email == email
    assert hasattr(user, "password_hash")
    assert user.is_superuser == is_superuser
    assert user.is_active == is_active


def test_user_authenticate(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateMe(email=email, password=password)
    user = event_loop.run_until_complete(crud.user.create_me(user_in))
    assert verify_password(password, user.password_hash)


def test_user_update_me(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password_hash = random_lower_string()
    user = event_loop.run_until_complete(
        User.create(email=email, password_hash=password_hash)
    )

    name = random_lower_string()
    family_name = random_lower_string()
    new_password = random_lower_string()

    user_in = UserUpdateMe(name=name, family_name=family_name, password=new_password)
    updated_user = event_loop.run_until_complete(crud.user.update_me(user, user_in))
    assert updated_user.name == name
    assert updated_user.family_name == family_name
    assert verify_password(new_password, updated_user.password_hash)


def test_user_update_by_superuser(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password_hash = random_lower_string()
    user = event_loop.run_until_complete(
        User.create(email=email, password_hash=password_hash)
    )

    name = random_lower_string()
    family_name = random_lower_string()
    new_password = random_lower_string()
    new_is_superuser = True
    new_is_active = False

    user_in = UserUpdateBySuperuser(
        name=name,
        family_name=family_name,
        password=new_password,
        is_active=new_is_active,
        is_superuser=new_is_superuser,
    )
    updated_user = event_loop.run_until_complete(
        crud.user.update_by_superuser(user, user_in)
    )
    assert updated_user.name == name
    assert updated_user.family_name == family_name
    assert verify_password(new_password, updated_user.password_hash)
    assert updated_user.is_active == new_is_active
    assert updated_user.is_superuser == new_is_superuser


# Above 5 tests are slow (and should be), becouse of hash/verfiy inside takes a lot of time!


def test_user_is_active_not(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password_hash = random_lower_string()
    user = event_loop.run_until_complete(
        User.create(email=email, password_hash=password_hash)
    )
    assert crud.user.is_active(user) == True


def test_user_is_active_active(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password_hash = random_lower_string()
    user = event_loop.run_until_complete(
        User.create(email=email, password_hash=password_hash, is_active=False)
    )
    assert crud.user.is_active(user) == False


def test_user_is_superuser_not(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password_hash = random_lower_string()
    user = event_loop.run_until_complete(
        User.create(email=email, password_hash=password_hash, is_superuser=False)
    )
    assert crud.user.is_superuser(user) == False


def test_user_is_superuser_superuser(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password_hash = random_lower_string()
    user = event_loop.run_until_complete(
        User.create(email=email, password_hash=password_hash, is_superuser=True)
    )
    assert crud.user.is_superuser(user) == True
