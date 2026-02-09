"""
FastAPI 애플리케이션 생명주기 관리 - 애플리케이션 시작/종료 시 동작 선언
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.database import (
    check_database_health,
    cleanup_database,
    init_database,
)
from app.config.logger import logger
from app.config.resource import cleanup_resources, init_resources


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션 시작 시:
    - 데이터베이스 초기화
    - 필요한 서비스 초기화


    애플리케이션 종료 시:
    - 리소스 정리
    - 연결 종료
    """
    logger.info("📦 FastAPI Sandbox 애플리케이션 시작")

    try:
        # 1. 데이터베이스 초기화
        await init_database()

        # 2. 데이터베이스 상태 확인
        db_healthy = await check_database_health()
        if not db_healthy:
            logger.warning(
                "⚠️ 데이터베이스 상태가 비정상이지만 애플리케이션을 실행합니다."
            )

        # 3. 기타 초기화 작업
        await init_resources()

        logger.info("✅ 데이터베이스 초기화 완료")

        # 애플리케이션 실행 상태 유지
        yield

    except Exception as e:
        logger.error(f"❌ 애플리케이션 초기화 실패: {e}")
        # 초기화 실패 시에도 애플리케이션이 실행되도록 함
        yield

    # 애플리케이션 종료 시 실행
    finally:
        logger.info("⛔ FastAPI Sandbox 애플리케이션 종료 프로세스 시작")

        try:
            # 1. 리소스 정리
            await cleanup_resources()

            # 2. 데이터베이스 정리
            await cleanup_database()

            logger.info("✅ 애플리케이션 종료 완료")

        except Exception as e:
            logger.error(f"❌ 애플리케이션 종료 중 오류 발생: {e}")
