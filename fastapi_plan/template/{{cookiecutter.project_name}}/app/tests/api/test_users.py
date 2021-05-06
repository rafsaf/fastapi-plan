from app import crud
from typing import Dict
from app.tests.conftest import default_user, default_superuser
from app.core.config import settings
from asyncio import AbstractEventLoop as EventLoop
from fastapi.testclient import TestClient
from app.tests.utils.utils import random_lower_string
from app.tests.utils.user import get_random_user_me, get_random_user_by_superuser


def test_read_users_superuser(
    client: TestClient,
    event_loop: EventLoop,
    normal_user_token_headers: Dict[str, str],
    superuser_token_headers: Dict[str, str],
) -> None:
    r = client.get(f"{settings.API_STR}/users/", headers=superuser_token_headers)
    users = r.json()
    assert len(users) >= 2
    for user in users:
        assert "email" in user
        assert "created_at" in user


def test_create_user_superuser(
    client: TestClient,
    event_loop: EventLoop,
    superuser_token_headers: Dict[str, str],
) -> None:
    data = get_random_user_by_superuser().dict()

    r = client.post(
        f"{settings.API_STR}/users/", headers=superuser_token_headers, json=data
    )

    current_user = r.json()
    assert r.status_code == 200
    assert current_user["email"] == data["email"]


def test_read_user_me_superuser(
    client: TestClient,
    event_loop: EventLoop,
    superuser_token_headers: Dict[str, str],
) -> None:
    r = client.get(f"{settings.API_STR}/users/me/", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] == default_superuser.is_active
    assert current_user["is_superuser"] == default_superuser.is_superuser
    assert current_user["email"] == default_superuser.email


def test_read_user_by_id_superuser(
    client: TestClient, event_loop: EventLoop, superuser_token_headers: Dict[str, str]
):
    normal_user = event_loop.run_until_complete(
        crud.user.get_by_email(default_user.email)
    )

    r = client.get(
        f"{settings.API_STR}/users/{normal_user.id}", headers=superuser_token_headers
    )
    assert r.status_code == 200
    current_user = r.json()
    assert current_user
    assert current_user["email"] == default_user.email


def test_update_user_by_id_superuser(
    client: TestClient, event_loop: EventLoop, superuser_token_headers: Dict[str, str]
):
    normal_user = event_loop.run_until_complete(
        crud.user.get_by_email(default_user.email)
    )

    data = {"is_active": False, "name": random_lower_string()}

    r = client.put(
        f"{settings.API_STR}/users/{normal_user.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] == data["is_active"]
    assert current_user["name"] == data["name"]
    ## cleaup to previous attributes
    event_loop.run_until_complete(normal_user.save())


def test_read_users_user(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_STR}/users/", headers=normal_user_token_headers)
    assert r.status_code == 400


def test_create_user_user(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    data = get_random_user_by_superuser().dict()
    r = client.post(
        f"{settings.API_STR}/users/", headers=normal_user_token_headers, json=data
    )
    assert r.status_code == 400


def test_read_user_me_user(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_STR}/users/me/", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] == default_user.is_active
    assert current_user["is_superuser"] == default_user.is_superuser
    assert current_user["email"] == default_user.email


def test_update_user_me_user(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    name = random_lower_string()
    family_name = random_lower_string()
    data = {"name": name, "family_name": family_name}

    r = client.put(
        f"{settings.API_STR}/users/me", headers=normal_user_token_headers, json=data
    )
    assert r.status_code == 200
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] == default_user.is_active
    assert current_user["name"] == name
    assert current_user["family_name"] == family_name
    assert current_user["is_superuser"] == default_user.is_superuser
    assert current_user["email"] == default_user.email


def test_create_user_open(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    data = get_random_user_me().dict()

    r = client.post(
        f"{settings.API_STR}/users/open", headers=normal_user_token_headers, json=data
    )

    assert r.status_code == 200
    current_user = r.json()
    assert current_user
    assert current_user["email"] == data["email"]
    assert current_user["name"] == None
    assert current_user["family_name"] == None
    assert current_user["is_active"] == True
    assert current_user["is_superuser"] == False

    created = event_loop.run_until_complete(crud.user.get_by_email(data["email"]))
    event_loop.run_until_complete(created.delete())


def test_create_user_open_already_created(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    data = {"email": default_user.email, "password": default_user.password}

    r = client.post(
        f"{settings.API_STR}/users/open", headers=normal_user_token_headers, json=data
    )

    assert r.status_code == 400
