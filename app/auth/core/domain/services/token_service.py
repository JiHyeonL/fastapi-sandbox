from app.auth.core.domain.token import Token
from app.auth.core.interface.token_repository_port import TokenRepositoryPort
from app.config.settings import REFRESH_TOKEN_EXPIRE_DAYS
from app.shared.infrastructure.security import JWTManager


class TokenService:

    def __init__(self, token_repository: TokenRepositoryPort):
        self.token_repository = token_repository
        self.jwt_manager = JWTManager(token_repository)

    async def create_token_set(self, user_id: int, user_email: str) -> Token:
        access_token = self.jwt_manager.create_token(
            user_id=user_id,
            user_email=user_email
        )
        refresh_token = self.jwt_manager.create_refresh_token(
            user_id=user_id,
            user_email=user_email
        )
        return Token(access_token, refresh_token)

    async def store_refresh_token(self, user_id: int, refresh_token: str):
        ttl_seconds = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        await self.token_repository.store_user_refresh_token(
            user_id=user_id,
            refresh_token=refresh_token,
            ttl_seconds=ttl_seconds
        )
