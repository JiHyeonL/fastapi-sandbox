from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.core.application.auth_output_mapper import AuthOutputMapper
from app.auth.core.application.inputs import RegisterInput
from app.auth.core.application.outputs import RegisterOutput
from app.auth.core.domain.services.token_service import TokenService
from app.users.core.application.inputs import UserCreateInput
from app.users.core.application.user_service import UserService


class AuthService:

    def __init__(self, token_service: TokenService, user_service: UserService):
        self.token_service = token_service
        self.user_service = user_service

    async def register(self, db: AsyncSession, register_data: RegisterInput) -> RegisterOutput:
        user_create_data = UserCreateInput(
            email=register_data.email,
            password=register_data.password,
            name=register_data.name
        )
        created_user = await self.user_service.create(db, user_create_data)
        token_set = await self.token_service.create_token_set(created_user.id, created_user.email)
        await self.token_service.store_refresh_token(created_user.id, token_set.refresh_token)

        return AuthOutputMapper.domain_to_register_output(token_set, created_user)
