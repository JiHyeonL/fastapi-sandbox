from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.auth.api.routers import auth_router
from app.config.database import check_database_health
from app.config.logger import setup_logger, logger
from app.config.settings import HOST, PORT, RELOAD, LOG_LEVEL
from app.shared.api.exception_handler import api_exception_handler, validation_exception_handler, \
    pydantic_validation_handler, sqlalchemy_exception_handler, general_exception_handler
from app.shared.api.exceptions import APIException
from app.shared.api.responses import success_response, APIResponseCode
from app.shared.core.lifespan import lifespan
from app.shared.core.middleware import setup_all_middleware

setup_logger()

app = FastAPI(
    title="FastAPI Sandbox",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

setup_all_middleware(app)

# 예외 핸들러 등록
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 라우터 등록
app.include_router(auth_router, prefix="/api/auth/v1")


@app.get("/")
async def root():
    return success_response(
        APIResponseCode.OK,
        {
            "message": "FastAPI Boilerplate API",
            "version": "1.0.0",
            "docs": "/docs",
            "status": "running"
        }
    )


@app.get("/health")
async def health_check():
    db_healthy = await check_database_health()

    return success_response(
        APIResponseCode.OK,
        {
            "status": "healthy" if db_healthy else "unhealthy",
            "database": "connected" if db_healthy else "disconnected",
            "timestamp": datetime.now()
        }
    )


if __name__ == "__main__":
    logger.info(f"FastAPI Sandbox 서버 시작: http://{HOST}:{PORT}")

    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level=LOG_LEVEL.lower()
    )
