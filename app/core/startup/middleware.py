"""
Middleware Setup - FastAPI 미들웨어
(API 요청-응답 주기동안 실행되는 공통 로직 처리)
"""

import time
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.core.logger import logger


def setup_all_middleware(app: FastAPI):
    logger.info("-----미들웨어 설정 시작-----")

    # 미들웨어는 역순으로 실행되므로 순서 주의
    setup_logging_middleware(app)
    setup_compression_middleware(app)
    setup_security_middleware(app)
    setup_cors_middleware(app)

    logger.info("모든 미들웨어 설정 완료")


def setup_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://mydomain.com",
        ],
        allow_credentials=True,  # 쿠키 허용
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    logger.info("CORS 미들웨어 설정 완료")


def setup_security_middleware(app: FastAPI):
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "localhost",
            "127.0.0.1",
            "mydomain.com",
            "*.mydomain.com",
            "testserver",  # 테스트용 Mock Server (TestClient)
        ],
    )
    logger.info("보안 미들웨어 설정 완료")


def setup_compression_middleware(app: FastAPI):
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,  # 1KB 이상부터 압축
    )
    logger.info("압축 미들웨어 설정 완료")


def setup_logging_middleware(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        # 요청 ID 생성
        request_id = str(uuid.uuid4())

        # 요청 시작 시간
        start_time = time.time()

        # 요청 정보 로깅
        client_ip = request.client.host if request.client else "unknown"
        logger.info(f"요청 시작: {request.method} {request.url} from {client_ip}")

        # 요청 처리
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(
                f"요청 완료: {request.method} {request.url} -> {response.status_code} ({process_time:.3f}s)"
            )
            # 응답 헤더에 요청 ID 추가
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            # 오류 발생 시 로깅
            process_time = time.time() - start_time
            logger.error(
                f"요청 실패: {request.method} {request.url} -> ERROR: {str(e)} ({process_time:.3f}s)"
            )

            raise

    logger.info("로깅 미들웨어 설정 완료")
