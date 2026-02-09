import traceback

from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config.logger import logger
from app.shared.api.exceptions import APIException
from app.shared.api.responses import warn_response, APIResponseCode, error_response


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    logger.warning(
        f"API Exception: {exc.code.code} - {exc.code.description}",
        extra={
            "path": str(request.url.path),
            "method": request.method,
            "code": exc.code.code,
            "context": exc.context
        }
    )

    response = warn_response(exc.code)
    return JSONResponse(
        status_code=exc.status_code,
        content=response.dict()
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    code_mapping = {
        400: APIResponseCode.COMMON_INVALID_PARAM,
        401: APIResponseCode.AUTH_UNAUTHORIZED,
        403: APIResponseCode.AUTH_FORBIDDEN,
        404: APIResponseCode.USER_NOT_FOUND,
        500: APIResponseCode.COMMON_INTERNAL_ERROR,
    }

    response_code = code_mapping.get(exc.status_code, APIResponseCode.COMMON_INTERNAL_ERROR)

    logger.warning(
        f"HTTP Exception: {exc.status_code} - {exc.detail}",
        extra={
            "path": str(request.url.path),
            "method": request.method,
            "status_code": exc.status_code,
            "detail": exc.detail
        }
    )

    response = error_response(response_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning(
        f"Validation Error: {exc.errors()}",
        extra={
            "path": str(request.url.path),
            "method": request.method,
            "errors": exc.errors()
        }
    )

    response = warn_response(APIResponseCode.COMMON_INVALID_PARAM)
    return JSONResponse(
        status_code=400,
        content=response.model_dump()
    )


async def pydantic_validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    logger.warning(
        f"Pydantic Validation Error: {exc.errors()}",
        extra={
            "path": str(request.url.path),
            "method": request.method,
            "errors": exc.errors()
        }
    )

    response = warn_response(APIResponseCode.COMMON_JSON_INVALID)
    return JSONResponse(
        status_code=400,
        content=response.model_dump()
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(
        f"Database Error: {str(exc)}",
        extra={
            "path": str(request.url.path),
            "method": request.method,
            "error": str(exc)
        }
    )

    response = error_response(APIResponseCode.COMMON_DATABASE_ERROR)
    return JSONResponse(
        status_code=500,
        content=response.model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        f"Unexpected Error: {str(exc)}",
        extra={
            "path": str(request.url.path),
            "method": request.method,
            "error": str(exc),
            "traceback": traceback.format_exc()
        }
    )

    response = error_response(APIResponseCode.COMMON_INTERNAL_ERROR)
    return JSONResponse(
        status_code=500,
        content=response.dict()
    )
