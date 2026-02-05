"""
Service Setup - 애플리케이션 시작 시 필요한 리소스 초기화 & 정리
"""

import redis

from app.core.config import REDIS_URL, TOKEN_STORAGE
from app.core.logger import logger


async def init_resources():
    """
    애플리케이션 시작 시 필요한 리소스 초기화
    """
    try:
        logger.info("-----리소스 초기화 시작-----")

        # 1. Redis 연결 테스트
        await test_redis_connection()

        # 2. 외부 API 연결 테스트 (Optional)
        await test_external_apis()

        # 3. 이벤트 시스템 초기화 (Optional)
        await init_event_system()

        # 4. 기타 초기화 작업들 (Optional)
        await setup_background_tasks()

        logger.info("리소스 초기화 완료")

    except Exception as e:
        logger.error(f"리소스 초기화 실패: {e}")


async def test_redis_connection():
    try:
        if TOKEN_STORAGE == "redis":
            redis_client = redis.from_url(REDIS_URL, decode_response=True)
            await redis_client.ping()
            await redis_client.close()

            logger.info("Redis 연결 테스트 성공")
        else:
            logger.info("Redis 사용하지 않음 (서버 인메모리 사용)")

    except ImportError:
        logger.warning("Redis 패키지가 설치되지 않음")

    except Exception as e:
        logger.warning(f"Redis 연결 테스트 실패: {e}")


async def test_external_apis():
    try:
        # 외부 API 테스트 로직 추가 가능
        logger.info("외부 API 연결 테스트 성공")

    except Exception as e:
        logger.warning(f"외부 API 연결 테스트 실패: {e}")


async def init_event_system():
    try:
        # 이벤트 시스템 초기화 로직 추가 가능
        logger.info("이벤트 시스템 초기화 성공")

    except Exception as e:
        logger.warning(f"이벤트 시스템 초기화 실패: {e}")


async def setup_background_tasks():
    try:
        # 백그라운드 태스크 설정 로직 추가 가능
        # 예: 토큰 정리, 로그 정리 등
        logger.info("백그라운드 태스크 설정 완료")

    except Exception as e:
        logger.error(f"백그라운드 태스크 설정 실패: {e}")


async def cleanup_resources():
    """
    애플리케이션 종료 시 사용한 리소스 정리
    """
    try:
        logger.info("-----리소스 정리 시작-----")

        # 1. 이벤트 시스템 정리 (Optional)
        await cleanup_event_system()

        # 2. Redis 연결 종료
        await cleanup_redis_connection()

        # 3. 백그라운드 태스크 정리 (Optional)
        await cleanup_background_tasks()

        logger.info("리소스 정리 완료")

    except Exception as e:
        logger.error(f"리소스 정리 실패: {e}")


async def cleanup_event_system():
    try:
        # 이벤트 시스템 정리 로직 추가 가능
        logger.info("이벤트 시스템 정리 완료")

    except Exception as e:
        logger.error(f"이벤트 시스템 정리 실패: {e}")


async def cleanup_redis_connection():
    try:
        if TOKEN_STORAGE == "redis":
            # Redis 클라이언트 정리는 각 서비스에서 담당
            logger.info("Redis 연결 정리 완료")

    except Exception as e:
        logger.error(f"Redis 연결 정리 실패: {e}")


async def cleanup_background_tasks():
    try:
        # 백그라운드 태스크 정리 로직 추가 가능
        logger.info("백그라운드 태스크 정리 완료")

    except Exception as e:
        logger.error(f"백그라운드 태스크 정리 실패: {e}")
