import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.users.repository import UserRepository
from app.users.schema import UserCreate, UserResponse, UserUpdate
from app.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    return UserService(UserRepository(session))


@router.get("/", response_model=list[UserResponse])
async def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    search: Annotated[str | None, Query(description="按用户名或邮箱搜索")] = None,
    order_by: Annotated[
        str, Query(description="排序字段: uid, username, created_at")
    ] = "uid",
    direction: Annotated[str, Query(description="排序方向: asc, desc")] = "asc",
    limit: Annotated[int, Query(ge=1, le=500, description="每页数量")] = 10,
    offset: Annotated[int, Query(ge=0, description="偏移量")] = 0,
):
    return await service.list_users(
        search=search,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset,
    )


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.create_user(user_data)


@router.get("/{uid}", response_model=UserResponse)
async def get_user(
    uid: Annotated[uuid.UUID, Path(..., description="用户 UID")],
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.get_user_by_uid(uid)


@router.patch("/{uid}", response_model=UserResponse)
async def update_user(
    uid: Annotated[uuid.UUID, Path(..., description="用户 UID")],
    user_data: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
):
    return await service.update_user(uid, user_data)


@router.delete("/{uid}", status_code=204)
async def delete_user(
    uid: Annotated[uuid.UUID, Path(..., description="用户 UID")],
    service: Annotated[UserService, Depends(get_user_service)],
):
    await service.delete_user(uid)
    return None
