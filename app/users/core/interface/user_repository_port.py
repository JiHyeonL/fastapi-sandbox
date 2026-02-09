from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.core.domain.user import User


class UserRepositoryPort(ABC):

    @abstractmethod
    async def create(self, transaction_session: AsyncSession, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass
