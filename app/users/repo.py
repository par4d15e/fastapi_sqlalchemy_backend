"""User CRUD operations (async) - SQLAlchemy"""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.users.model import User
from app.users.schema import UserCreate, UserUpdate


class UserRepository:
    """User CRUD operations class - Complete JWT Auth (async)"""

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await db.get(User, user_id)
        return result

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username"""
        statement = select(User).where(User.username == username)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Getalluser"""
        statement = select(User).offset(skip).limit(limit)
        result = await db.execute(statement)
        return list(result.scalars().all())

    @staticmethod
    async def create(db: AsyncSession, user_create: UserCreate) -> User:
        """Createnewuser"""
        hashed_password = get_password_hash(user_create.password)

        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            is_verified=False,
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def update(
        db: AsyncSession, user_id: int, user_update: UserUpdate
    ) -> Optional[User]:
        """updateuserinformation"""
        db_user = await UserRepository.get_by_id(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db_user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """Deleteuser"""
        db_user = await UserRepository.get_by_id(db, user_id)
        if not db_user:
            return False

        await db.delete(db_user)
        await db.commit()
        return True

    @staticmethod
    async def authenticate(
        db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """Authenticate user credentials"""
        user = await UserRepository.get_by_username(db, username)

        if not user:
            user = await UserRepository.get_by_email(db, username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        user.last_login_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def verify_email(db: AsyncSession, user_id: int) -> Optional[User]:
        """ValidateuserEmail"""
        db_user = await UserRepository.get_by_id(db, user_id)
        if not db_user:
            return None

        db_user.is_verified = True
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def change_password(
        db: AsyncSession, user_id: int, new_password: str
    ) -> Optional[User]:
        """modifyuserPassword"""
        db_user = await UserRepository.get_by_id(db, user_id)
        if not db_user:
            return None

        db_user.hashed_password = get_password_hash(new_password)
        db_user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_user)
        return db_user


# Createglobalinstance
user_repository = UserRepository()
