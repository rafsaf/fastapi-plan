from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.UserPydanticList)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Retrieve users.
    """
    users = await crud.user.get_multi(skip=skip, limit=limit)
    return await schemas.UserPydanticList.from_queryset(users)


@router.post("/", response_model=schemas.UserPydantic)
async def create_user(
    user_in: schemas.UserCreateBySuperuser,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Create new user.
    """
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create_by_superuser(obj_in=user_in)
    return await schemas.UserPydantic.from_tortoise_orm(user)


@router.put("/me", response_model=schemas.UserPydantic)
async def update_user_me(
    user_in: schemas.UserUpdateMe,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update own user.
    """
    user = await crud.user.update_me(db_obj=current_user, obj_in=user_in)
    return await schemas.UserPydantic.from_tortoise_orm(user)


@router.get("/me", response_model=schemas.UserPydantic)
async def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get current user.
    """
    return await schemas.UserPydantic.from_tortoise_orm(current_user)


@router.post("/open", response_model=schemas.UserPydantic)
async def create_user_open(user_in: schemas.UserCreateMe):
    """
    Create new user without the need to be logged in.
    """
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )
    user = await crud.user.create_me(obj_in=user_in)
    return await schemas.UserPydantic.from_tortoise_orm(user)


@router.get("/{user_id}", response_model=schemas.UserPydantic)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get a specific user by id.
    """
    user = await crud.user.get(id=user_id)
    if user == current_user:
        return user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user does not exist"
        )
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return await schemas.UserPydantic.from_tortoise_orm(user)


@router.put("/{user_id}", response_model=schemas.UserPydantic)
async def update_user(
    user_id: int,
    user_in: schemas.UserUpdateBySuperuser,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """
    Update a user.
    """
    user = await crud.user.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update_by_superuser(db_obj=user, obj_in=user_in)
    return await schemas.UserPydantic.from_tortoise_orm(user)
