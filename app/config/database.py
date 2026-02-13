"""
데이터베이스 초기화 및 마이그레이션
"""

import asyncio

from sqlalchemy import text

from app.config.logger import logger
from app.shared.infrastructure.base import Base, engine


async def init_database():
    """
    1. 데이터베이스 연결 확인
    2. Alembic을 사용한 자동 마이그레이션 실행
    3. 필요시 초기 데이터 설정
    """
    try:
        logger.info("-----데이터베이스 초기화 시작-----")

        # 1. 데이터베이스 연결 확인
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute(text("SELECT 1")))
            logger.info("데이터베이스 연결 확인 완료")

        # 2. 데이터베이스 초기화
        await initialize_db()
        logger.info("데이터베이스 초기화 완료")

    except Exception as e:
        logger.error(f"데이터베이스 초기화 실패: {e}")
        raise


async def initialize_db():
    try:
        logger.info("-----SQLAlchemy를 통한 테이블 생성 시작-----")

        async with engine.begin() as conn:
            # 모든 테이블 생성
            await conn.run_sync(Base.metadata.create_all)

        logger.info("테이블 생성 완료")

    except Exception as e:
        logger.error(f"테이블 생성 실패: {e}")
        raise


async def check_database_health():
    try:
        async with engine.begin() as conn:
            # 간단한 쿼리로 연결 확인
            result = await conn.execute(text("SELECT 1 as health_check"))
            health_result = result.scalar()

            if health_result == 1:
                logger.info("데이터베이스 상태: 정상")
                return True
            else:
                logger.warning("데이터베이스 상태: 비정상")
                return False

    except Exception as e:
        logger.error(f"데이터베이스 상태 확인 실패: {e}")
        return False


async def cleanup_database():
    try:
        logger.info("-----데이터베이스 연결 정리 중-----")
        await engine.dispose()
        logger.info("데이터베이스 연결 정리 완료")

    except Exception as e:
        logger.error(f"데이터베이스 정리 실패: {e}")


# 비동기 헬퍼 함수들
def run_async_migration():
    """
    동기 컨텍스트에서 비동기 마이그레이션 실행
    """
    asyncio.run(init_database())
