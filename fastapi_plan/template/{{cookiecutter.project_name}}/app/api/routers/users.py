from app.schemas.user import UserPydanticList
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from app import crud, models, schemas
from app.schemas import UserPydantic
from app.api import deps

router = APIRouter()


@router.get("/", response_model=UserPydanticList)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = await crud.user.get_multi(skip=skip, limit=limit)
    return await UserPydanticList.from_queryset(users)


@router.post("/", response_model=UserPydantic)
async def create_user(
    user_in: schemas.UserCreateBySuperuser,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create_by_superuser(obj_in=user_in)
    return UserPydantic.from_orm(user)


@router.put("/me", response_model=UserPydantic)
async def update_user_me(
    user_in: schemas.UserUpdateMe,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    user = await crud.user.update_me(db_obj=current_user, obj_in=user_in)
    return schemas.UserPydantic.from_orm(user)


@router.get("/me", response_model=UserPydantic)
async def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return UserPydantic.from_orm(current_user)


@router.post("/open", response_model=UserPydantic)
async def create_user_open(user_in: schemas.UserCreateMe):
    """
    Create new user without the need to be logged in.
    """
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = await crud.user.create_me(obj_in=user_in)
    return UserPydantic.from_orm(user)


@router.get("/{user_id}", response_model=UserPydantic)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await crud.user.get(id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return UserPydantic.from_orm(user)


@router.put("/{user_id}", response_model=UserPydantic)
async def update_user(
    user_id: int,
    user_in: schemas.UserUpdateBySuperuser,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = await crud.user.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update_by_superuser(db_obj=user, obj_in=user_in)
    return UserPydantic.from_orm(user)
