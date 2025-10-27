from uuid import UUID

from fastapi import APIRouter, Depends

from identity.src.dependencies import get_user_service
from identity.src.domain.user import User, UsersSearch, UserUpdate
from identity.src.service.user import UserService

router = APIRouter(tags=["Users"])


@router.get("", response_model=list[User])
async def get_many(
        data: UsersSearch = Depends(),
        user_service: UserService = Depends(get_user_service),
):
    """Get all users by provided fields."""
    return await user_service.get_many(
        **data.model_dump(exclude_none=True)
    )


@router.get("/{user_id}", response_model=User)
async def get(
        user_id: UUID,
        user_service: UserService = Depends(get_user_service),
):
    """Get specified user. """
    return await user_service.get(id=user_id)


@router.patch("/{user_id}", response_model=User, status_code=202)
async def update(
        user_id: UUID,
        data: UserUpdate,
        user_service: UserService = Depends(get_user_service)
):
    """ Update specified user. """
    document = await user_service.update(
        user_id,
        **data.model_dump(exclude_none=True)
    )
    return document


@router.delete("/{user_id}", status_code=204)
async def delete(
        user_id: UUID,
        user_service: UserService = Depends(get_user_service),
):
    """ Delete specified user. """
    await user_service.delete(user_id)
