from app.core.config import settings
import random
import string
from asyncio import AbstractEventLoop as EventLoop
from typing import Dict
from app import crud
from fastapi.testclient import TestClient
from app.schemas import UserCreateBySuperuser


def random_integer_below_100() -> int:
    return random.randint(0, 99)


def random_lower_string(length=20) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email(length=10) -> str:
    return f"{random_lower_string(length)}@{random_lower_string(length)}.com"


def user_authentication_headers(
    client: TestClient,
    event_loop: EventLoop,
    email: str,
    password: str,
    is_superuser: bool = False,
    is_active: bool = True,
) -> Dict[str, str]:

    data = {"username": email, "password": password}
    user_in = UserCreateBySuperuser(
        email=email, password=password, is_superuser=is_superuser, is_active=is_active
    )
    event_loop.run_until_complete(crud.user.create_by_superuser(user_in))
    r = client.post(f"{settings.API_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
