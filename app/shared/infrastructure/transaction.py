"""
트랜잭션 관리 유틸리티
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.api.exceptions import APIException
from app.shared.api.responses import APIResponseCode
from app.shared.infrastructure.base import AsyncDBSession

logger = logging.getLogger(__name__)


async def get_transaction_db() -> AsyncGenerator[AsyncSession, None]:
    """
    트랜잭션 DB 세션 의존성 주입 함수

    트랜잭션 적용 범위:
    - get_transaction_db()를 호출한 곳

    사용법:
    ```python
    @router.post("/example")
    async def create_example(
        db: AsyncSession = Depends(get_transaction_db)
    ):
        # db에 의존성을 주입한 순간 트랜잭션이 시작
        # Repository CUD 메소드에 db 파라미터로 전달
    ```
    """
    async with transaction_context() as db:
        yield db


@asynccontextmanager
async def transaction_context() -> AsyncGenerator[AsyncSession, None]:
    """
    트랜잭션 컨텍스트 매니저

    자동으로 트랜잭션을 시작하고, 성공시 커밋, 실패시 롤백 처리
    의존성 주입 방법을 사용하지 못할 때 활용한다.

    사용 예시:
    ```python
    async with transaction_context() as db:
        users = User(name="test")
        db.add(users)
        await db.flush()  # 중간 검증 가능

        project = Project(user_id=users.id)
        db.add(project)
        # 에러 발생시 user와 project 모두 롤백
    ```
    """
    async with AsyncDBSession() as session:
        try:
            logger.debug("트랜잭션 시작 (AsyncSession 자동 트랜잭션)")

            yield session

            await session.commit()
            logger.debug("트랜잭션 커밋 완료")

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"DB 에러로 인한 롤백: {str(e)}")
            raise APIException(
                APIResponseCode.TRANSACTION_ERROR,
                {"original_error": str(e), "error_type": "database_error"},
            )
        except Exception as e:
            await session.rollback()
            logger.error(f"예외 발생으로 인한 롤백: {str(e)}")
            raise
