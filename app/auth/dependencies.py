from fastapi import Depends

from app.auth.core.application.auth_service import AuthService
from app.auth.core.domain.services.token_service import TokenService
from app.auth.core.interface.token_repository_port import TokenRepositoryPort
from app.auth.infrastructure.repository.memory_token_repository import MemoryTokenRepository
from app.auth.infrastructure.repository.redis_token_repository import RedisTokenRepository
from app.config.settings import TOKEN_STORAGE
from app.shared.infrastructure.transaction import logger
from app.users.core.application.user_service import UserService
from app.users.dependencies import get_user_service


def get_token_repository() -> TokenRepositoryPort:
    storage_type = TOKEN_STORAGE
    if storage_type == "memory":
        return MemoryTokenRepository()
    if storage_type == "redis":
        return RedisTokenRepository()
    logger.warning(f"지원하지 않는 토큰 저장소 타입")
    return MemoryTokenRepository()


def get_token_service(
        token_repository: TokenRepositoryPort = Depends(get_token_repository),
) -> TokenService:
    return TokenService(token_repository)


def get_auth_service(
        token_service: TokenService = Depends(get_token_service),
        user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(token_service, user_service)
