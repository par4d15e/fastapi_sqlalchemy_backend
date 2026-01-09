from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

# 密码哈希算法
password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配

    :param plain_password: 明文密码（str）
    :param hashed_password: 存储的密码哈希值（str）
    :return: 匹配返回 True，否则返回 False

    注意：模块初始化时会调用 `pwdlib.PasswordHash.recommended()`，若未安装可选哈希器（argon2/bcrypt）可能会抛出 `pwdlib.exceptions.HasherNotAvailable`。
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希字符串

    :param password: 明文密码（str）
    :return: 密码哈希字符串（str）

    说明：该实现依赖 `pwdlib` 的可选哈希器，生产环境推荐安装 `pwdlib[argon2]` 或 `pwdlib[bcrypt]`。
    """
    return password_hash.hash(password)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """创建访问令牌（JWT）

    :param subject: 用户标识（通常为字符串，例如用户名或用户 id）；若需包含更多信息，可传入序列化字符串或在调用方扩展 payload。
    :param expires_delta: 过期时长（timedelta），默认使用 `settings.access_token_expire_minutes`。
    :return: 编码后的 JWT 字符串（使用 `settings.jwt_secret` 与 `settings.jwt_algorithm`）

    说明：
    - 使用 UTC 时区（timezone-aware）计算过期时间，并将 `exp` 存为整型秒级时间戳（Unix epoch）。
    - 解码/验证建议使用 `jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])` 并处理 `jwt.PyJWTError`。
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    # 使用 UTC 时间戳（秒）作为 exp，避免时区/序列化差异
    to_encode = {"exp": int(expire.timestamp()), "sub": subject}
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt
