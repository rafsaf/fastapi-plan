from typing import Optional

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app import models, schemas
from tortoise.exceptions import DoesNotExist


class CRUDUser(CRUDBase[models.User, schemas.UserCreateMe, schemas.UserUpdateMe]):
    async def get_by_email(self, email: str) -> Optional[models.User]:
        try:
            user = await models.User.get(email=email)
        except DoesNotExist:
            return None
        else:
            return user

    async def create_me(self, obj_in: schemas.UserCreateMe) -> models.User:
        db_obj = await models.User.create(
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
        )
        return db_obj

    async def create_by_superuser(
        self, obj_in: schemas.UserCreateBySuperuser
    ) -> models.User:

        db_obj = await models.User.create(
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
            is_active=obj_in.is_active,
        )
        return db_obj

    async def update_me(
        self, db_obj: models.User, obj_in: schemas.UserUpdateMe
    ) -> models.User:
        db_obj.name = obj_in.name
        db_obj.family_name = obj_in.family_name
        if obj_in.password:
            new_password = get_password_hash(obj_in.password)
            db_obj.password_hash = new_password
        await db_obj.save()
        await db_obj.refresh_from_db()
        return db_obj

    async def update_by_superuser(
        self, db_obj: models.User, obj_in: schemas.UserUpdateBySuperuser
    ) -> models.User:

        db_obj.name = obj_in.name
        db_obj.family_name = obj_in.family_name
        if obj_in.password:
            new_password = get_password_hash(obj_in.password)
            db_obj.password_hash = new_password
        db_obj.is_superuser = obj_in.is_superuser  # type: ignore

        db_obj.is_active = obj_in.is_active  # type: ignore
        await db_obj.save()
        await db_obj.refresh_from_db()
        return db_obj

    async def authenticate(self, email: str, password: str) -> Optional[models.User]:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def is_active(self, user: models.User) -> bool:
        return user.is_active  # type: ignore

    def is_superuser(self, user: models.User) -> bool:
        return user.is_superuser  # type: ignore


user = CRUDUser(models.User)
