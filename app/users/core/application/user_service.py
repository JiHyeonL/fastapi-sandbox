from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logger import logger
from app.shared.api.exceptions import APIException
from app.shared.api.responses import APIResponseCode
from app.shared.infrastructure.security import hash_password
from app.users.core.application.inputs import UserCreateInput
from app.users.core.application.outputs import UserCreateOutput
from app.users.core.application.user_output_mapper import UserOutputMapper
from app.users.core.domain.user import User
from app.users.core.interface.user_repository_port import UserRepositoryPort


class UserService:

    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repository = user_repository

    async def create(self, db: AsyncSession, user_data: UserCreateInput) -> UserCreateOutput:
        same_user = await self.user_repository.find_by_email(user_data.email)
        if same_user:
            logger.warning(f"이미 존재하는 이메일로 회원가입 시도: {user_data.email}")
            raise APIException(APIResponseCode.USER_EMAIL_ALREADY_EXISTS)

        password_hash = hash_password(user_data.password)
        user_payload = {
            "email": user_data.email,
            "password_hash": password_hash,
            "name": user_data.name or user_data.email.split("@")[0]
        }

        saved_user = await self.user_repository.create(db, User(**user_payload))
        return UserOutputMapper.domain_to_create_output(saved_user)
