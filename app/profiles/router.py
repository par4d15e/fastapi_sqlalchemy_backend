from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.exception import NotFoundException
from app.profiles.schema import ProfileCreate, ProfileRead, ProfileUpdate
from app.profiles.service import ProfileService

router = APIRouter()


async def get_profile_service(
    session: AsyncSession = Depends(get_session),
) -> ProfileService:
    return ProfileService(session)


@router.post("/profile/", response_model=ProfileRead, status_code=201)
async def create_profile(
    profile: ProfileCreate, service: ProfileService = Depends(get_profile_service)
):
    return await service.create(profile)


@router.get("/profile/{profile_name}", response_model=ProfileRead)
async def read_profile(
    profile_name: str, service: ProfileService = Depends(get_profile_service)
):
    profile = await service.get_by_name(profile_name)
    if not profile:
        raise NotFoundException("Profile not found")
    return profile


@router.patch("/profile/{profile_id}", response_model=ProfileRead)
async def update_profile(
    profile_id: int,
    profile: ProfileUpdate,
    service: ProfileService = Depends(get_profile_service),
):
    return await service.update(profile_id, profile)


@router.delete("/profile/{profile_id}", status_code=204)
async def delete_profile(
    profile_id: int, service: ProfileService = Depends(get_profile_service)
):
    await service.delete(profile_id)
    return None
