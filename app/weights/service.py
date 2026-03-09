from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from app.core.exception import NotFoundException
from app.weights.repository import WeightRecordRepository
from app.weights.schema import WeightRecordCreate, WeightRecordResponse, WeightRecordUpdate


class WeightRecordService:
    """WeightRecord 服务层：封装业务逻辑并调用 repository"""

    def __init__(self, repository: WeightRecordRepository) -> None:
        self.repository = repository

    async def get_record_by_id(self, record_id: int) -> WeightRecordResponse:
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise NotFoundException("WeightRecord not found")
        return WeightRecordResponse.model_validate(record)

    async def list_records_by_profile(
        self,
        profile_id: int,
        *,
        order_by: str = "measured_at",
        direction: str = "desc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[WeightRecordResponse]:
        """查询指定宠物的体重记录列表"""
        records = await self.repository.get_by_profile_id(
            profile_id,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )
        return [WeightRecordResponse.model_validate(r) for r in records]

    async def list_records(
        self,
        *,
        order_by: str = "measured_at",
        direction: str = "desc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[WeightRecordResponse]:
        """查询所有体重记录"""
        records = await self.repository.get_all(
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )
        return [WeightRecordResponse.model_validate(r) for r in records]

    async def create_record(self, record_data: WeightRecordCreate) -> WeightRecordResponse:
        data = record_data.model_dump()
        if data.get("measured_at") is None:
            data["measured_at"] = datetime.now(tz=timezone.utc)
        try:
            record = await self.repository.create(data)
            return WeightRecordResponse.model_validate(record)
        except IntegrityError as e:
            raise NotFoundException("Profile not found") from e

    async def update_record(
        self,
        record_id: int,
        record_data: WeightRecordUpdate,
    ) -> WeightRecordResponse:
        update_data = record_data.model_dump(exclude_unset=True, exclude_none=True)
        updated = await self.repository.update(record_id, update_data)
        if not updated:
            raise NotFoundException("WeightRecord not found")
        return WeightRecordResponse.model_validate(updated)

    async def delete_record(self, record_id: int) -> bool:
        deleted = await self.repository.delete(record_id)
        if not deleted:
            raise NotFoundException("WeightRecord not found")
        return True
