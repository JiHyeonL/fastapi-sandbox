from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import DATABASE_URL
from app.core.timestamp import BaseTimeEntity

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncDBSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase, BaseTimeEntity):
    """
    모든 ORM 모델의 기본 클래스

    자동 제공 필드(BaseTimeEntity)
    - created_at: 생성 일시
    - updated_at: 수정 일시
    """

    pass


async def get_db():
    """
    데이터베이스 세션 주입용 함수
    """
    async with AsyncDBSession() as session:
        try:
            yield session
        finally:
            await session.close()
