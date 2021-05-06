from app.schemas import UserCreateMe, UserCreateBySuperuser
from app.tests.utils.utils import random_email, random_lower_string


def get_random_user_me() -> UserCreateMe:
    return UserCreateMe(
        email=random_email(),
        password=random_lower_string(),
    )


def get_random_user_by_superuser() -> UserCreateBySuperuser:
    return UserCreateBySuperuser(
        email=random_email(),
        password=random_lower_string(),
    )