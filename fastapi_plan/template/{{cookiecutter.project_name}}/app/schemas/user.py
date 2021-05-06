from typing import Optional
from tortoise.contrib.pydantic.creator import (
    pydantic_model_creator,
    pydantic_queryset_creator,
)
from pydantic import BaseModel, EmailStr
from app.models import User

UserPydantic = pydantic_model_creator(User)
UserPydanticList = pydantic_queryset_creator(User)


class UserCreateMe(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserUpdateMe(BaseModel):
    password: Optional[str]
    name: Optional[str]
    family_name: Optional[str]

    class Config:
        orm_mode = True


class UserCreateBySuperuser(BaseModel):
    email: EmailStr
    password: str
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True


class UserUpdateBySuperuser(UserCreateBySuperuser):
    email: Optional[EmailStr]
    password: Optional[str]
    name: Optional[str]
    family_name: Optional[str]
