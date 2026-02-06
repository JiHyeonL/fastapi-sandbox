"""
데이터베이스 초기화 및 마이그레이션
"""

import asyncio

import alembic.runtime.migration
import alembic.util.exc
from alembic import command
from alembic.config import Config
from sqlalchemy import text

from app.config.config import DATABASE_URL
from app.core.database import Base, engine
from common.logger import logger


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

        # 2. Alembic 마이그레이션 실행
        await run_migrations()
        logger.info("데이터베이스 초기화 완료")

    except Exception as e:
        logger.error(f"데이터베이스 초기화 실패: {e}")
        raise


async def run_migrations():
    try:
        logger.info("-----데이터베이스 마이그레이션 시작-----")

        alembic_config = Config("alembic.ini")
        alembic_config.set_main_option("sqlalchemy.url", DATABASE_URL)

        def check_current_revision(connection):
            context = alembic.runtime.migration.MigrationContext.configure(connection)
            return context.get_current_revision()

        def upgrade_to_head(connection):
            alembic_config.attributes["connection"] = connection
            command.upgrade(alembic_config, "head")

        async with engine.begin() as conn:
            current_rev = await conn.run_sync(check_current_revision)
            logger.info(f"현재 데이터베이스 리비전: {current_rev}")

            # 마이그레이션 실행
            await conn.run_sync(upgrade_to_head)

        logger.info("데이터베이스 마이그레이션 완료")

    except alembic.util.exc.CommandError as e:
        if "Can't locate revision identified by" in str(e):
            logger.warning(
                "마이그레이션 히스토리가 없습니다. 테이블을 새로 생성합니다."
            )
            await create_tables()
        else:
            logger.error(f"Alembic 마이그레이션 실패: {e}")
            raise
    except Exception as e:
        logger.error(f"마이그레이션 실행 실패: {e}")

        # 마이그레이션 실패 시 테이블 직접 생성 시도
        await create_tables()


async def create_tables():
    """
    SQLAlchemy를 사용한 테이블 직접 생성 (Alembic 없이)
    """
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
