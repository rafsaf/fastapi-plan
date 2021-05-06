from typing import Dict
from fastapi.testclient import TestClient
from app.tests.conftest import default_user, default_superuser
from asyncio import AbstractEventLoop as EventLoop
from app.core.config import settings


def test_get_access_token(
    client: TestClient, event_loop: EventLoop, normal_user_token_headers: Dict[str, str]
) -> None:
    login_data = {"username": default_user.email, "password": default_user.password}
    r = client.post(f"{settings.API_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result