from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import RefreshToken, VerificationCode
from app.auth.repo import (
    RefreshTokenCRUD as refresh_token_crud,
)
from app.auth.repo import (
    VerificationCodeCRUD as verification_code_crud,
)
from app.auth.schemas import RefreshTokenCreate
from app.core.exception import NotFoundException


class AuthService:
    """Auth 服务层：封装与令牌/验证码相关的业务逻辑并调用 repo"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # Refresh token related
    async def create_refresh_token(self, payload: RefreshTokenCreate) -> RefreshToken:
        # 这里不强制去重 token（token 应由调用方保证唯一），直接创建
        return await refresh_token_crud.create(
            self._session,
            user_id=payload.user_id,
            token=payload.token,
            expires_at=payload.expires_at,
            device_name=payload.device_name,
            device_type=payload.device_type,
            ip_address=payload.ip_address,
            user_agent=payload.user_agent,
        )

    async def get_refresh_token(self, token: str) -> Optional[RefreshToken]:
        return await refresh_token_crud.get_by_token(self._session, token)

    async def revoke(self, token: str) -> bool:
        db_token = await refresh_token_crud.get_by_token(self._session, token)
        if not db_token:
            raise NotFoundException("Refresh token not found")
        db_token.revoke()
        await self._session.commit()
        return True

    async def revoke_user_tokens(self, user_id: int) -> int:
        return await refresh_token_crud.revoke_user_tokens(self._session, user_id)

    async def cleanup_expired_refresh_tokens(self) -> int:
        return await refresh_token_crud.cleanup_expired(self._session)

    # Verification code related
    async def create_verification_code(
        self,
        user_id: int,
        code_type: str,
        expiration_minutes: int = 60,
        max_attempts: int = 5,
    ) -> VerificationCode:
        return await verification_code_crud.create(
            self._session,
            user_id=user_id,
            code_type=code_type,
            expiration_minutes=expiration_minutes,
            max_attempts=max_attempts,
        )

    async def get_verification_code(
        self, user_id: int, code: str, code_type: str
    ) -> Optional[VerificationCode]:
        return await verification_code_crud.get(self._session, user_id, code, code_type)

    async def verify_code(
        self, user_id: int, code: str, code_type: str
    ) -> VerificationCode | None:
        db_code = await verification_code_crud.get(
            self._session, user_id, code, code_type
        )
        if not db_code:
            raise NotFoundException("Verification code not found")

        # increment attempts and check validity inside repo/service
        db_code.increment_attempts()
        await self._session.commit()

        if not db_code.is_valid():
            return None

        db_code.mark_as_used()
        await self._session.commit()
        await self._session.refresh(db_code)
        return db_code

    async def get_latest_code(
        self, user_id: int, code_type: str
    ) -> Optional[VerificationCode]:
        return await verification_code_crud.get_latest(
            self._session, user_id, code_type
        )

    async def invalidate_user_codes(self, user_id: int, code_type: str) -> int:
        return await verification_code_crud.invalidate_user_codes(
            self._session, user_id, code_type
        )

    async def cleanup_expired_verification_codes(self) -> int:
        return await verification_code_crud.cleanup_expired(self._session)
