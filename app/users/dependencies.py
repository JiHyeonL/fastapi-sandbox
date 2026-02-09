from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import DB_TYPE
from app.shared.infrastructure.base import get_db
from app.users.core.application.user_service import UserService
from app.users.core.interface.user_repository_port import UserRepositoryPort
from app.users.infrastructure.repository.postgres_user_repository import PostgresUserRepository


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepositoryPort:
    db_type = DB_TYPE

    if db_type == "postgres":
        return PostgresUserRepository(db)
    raise ValueError(f"지원하지 않는 DB 타입: {db_type}")


def get_user_service(user_repository: UserRepositoryPort = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository)
