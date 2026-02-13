from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logger import logger
from app.shared.api.exceptions import APIException
from app.shared.api.responses import APIResponseCode
from app.users.core.domain.user import User
from app.users.core.interface.user_repository_port import UserRepositoryPort
from app.users.infrastructure.models import UserDB
from app.users.infrastructure.user_db_mapper import UserDBMapper


class PostgresUserRepository(UserRepositoryPort):

    def __init__(self, session: AsyncSession):
        self._read_session = session

    async def create(self, transaction_session: AsyncSession, user: User) -> User:
        try:
            user_db = UserDBMapper.domain_to_db(user)
            transaction_session.add(user_db)
            await transaction_session.commit()
            await transaction_session.refresh(user_db)

            return UserDBMapper.db_to_domain(user_db)

        except Exception as e:
            logger.error(f"사용자 생성 실패: {e}")
            raise APIException(APIResponseCode.USER_CREATION_FAILED)

    async def find_by_email(self, email: str) -> Optional[User]:
        try:
            result = await self._read_session.execute(
                select(UserDB)
                .where(UserDB.email == email)
            )
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return UserDBMapper.db_to_domain(user)

        except SQLAlchemyError as e:
            logger.error(f"사용자 이메일 조회 실패: {e}")
            raise
