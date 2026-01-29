from sqlalchemy.exc import IntegrityError

from app.core.exception import AlreadyExistsException, NotFoundException
from app.reminders.repository import ReminderRepository
from app.reminders.schema import ReminderCreate, ReminderResponse, ReminderUpdate


class ReminderService:
    """Reminder 服务层：封装业务逻辑并调用 repository"""
    def __init__(self, repository: ReminderRepository) -> None:
        self.repository = repository

    async def get_reminder_by_title(self, reminder_title: str) -> ReminderResponse:
        reminder = await self.repository.get_by_title(reminder_title)
        if not reminder:
            raise NotFoundException("Reminder not found")

        return ReminderResponse.model_validate(reminder)
    
    async def get_reminder_by_id(self, reminder_id: int) -> ReminderResponse:
        reminder = await self.repository.get_by_id(reminder_id)
        if not reminder:
            raise NotFoundException("Reminder not found")

        return ReminderResponse.model_validate(reminder)
    
    async def list_reminders(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[ReminderResponse]:
        """查询所有提醒"""
        reminders = await self.repository.get_all(
            search=search,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )

        return [ReminderResponse.model_validate(reminder) for reminder in reminders]
    
    async def create_reminder(self, reminder_data: ReminderCreate) -> ReminderResponse:
        data = reminder_data.model_dump()
        try:
            reminder = await self.repository.create(data)

            return ReminderResponse.model_validate(reminder)
        except IntegrityError as e:
            raise AlreadyExistsException("Reminder with this title already exists") from e

    async def update_reminder(
        self,
        reminder_id: int,
        reminder_data: ReminderUpdate,
    ) -> ReminderResponse:
        try:
            update_data = reminder_data.model_dump(exclude_unset=True, exclude_none=True)
            updated = await self.repository.update(reminder_id, update_data)
            if not updated:
                raise NotFoundException("Reminder not found")

            return ReminderResponse.model_validate(updated)
        except IntegrityError as e:
            raise AlreadyExistsException("Reminder with this title already exists") from e
        
    async def delete_reminder(self, reminder_id: int) -> bool:
        deleted = await self.repository.delete(reminder_id)
        if not deleted:
            raise NotFoundException("Reminder not found")

        return True