"""
응답으로 전송할 코드와 응답 모델
"""

from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponseCode(Enum):
    # SUCCESS
    SUCCESS = ("SUCCESS", 200, "요청이 성공적으로 처리되었습니다")

    # AUTH 도메인
    AUTH_UNAUTHORIZED = ("AUTH-01", 401, "인증이 필요합니다")
    AUTH_FORBIDDEN = ("AUTH-02", 403, "접근 권한이 없습니다")
    AUTH_TOKEN_INVALID = ("AUTH-03", 401, "유효하지 않은 토큰입니다")
    AUTH_TOKEN_EXPIRED = ("AUTH-04", 401, "토큰이 만료되었습니다")
    AUTH_USER_NOT_FOUND = ("AUTH-05", 404, "사용자를 찾을 수 없습니다")
    AUTH_LOGIN_FAILED = ("AUTH-06", 401, "로그인에 실패했습니다")
    AUTH_LOGOUT_FAILED = ("AUTH-07", 500, "로그아웃 처리 중 오류가 발생했습니다")

    # USER 도메인
    USER_NOT_FOUND = ("USER-01", 404, "사용자를 찾을 수 없습니다")
    USER_EMAIL_ALREADY_EXISTS = ("USER-02", 409, "이미 존재하는 이메일입니다")
    USER_CREATION_FAILED = ("USER-03", 500, "사용자 생성에 실패했습니다")
    USER_UPDATE_FAILED = ("USER-04", 500, "사용자 정보 수정에 실패했습니다")
    USER_INVALID_PASSWORD = ("USER-05", 400, "잘못된 비밀번호입니다")

    # TRANSACTION 도메인
    TRANSACTION_ERROR = ("TRANSACTION-01", 500, "트랜잭션 처리 중 오류가 발생했습니다")
    TRANSACTION_ROLLBACK = ("TRANSACTION-02", 500, "트랜잭션이 롤백되었습니다")
    TRANSACTION_TIMEOUT = ("TRANSACTION-03", 504, "트랜잭션 처리 시간이 초과되었습니다")

    # COMMON 도메인
    COMMON_INVALID_PARAM = ("COMMON-01", 400, "요청 파라미터가 유효하지 않습니다")
    COMMON_INTERNAL_ERROR = ("COMMON-02", 500, "서버 내부 오류가 발생했습니다")
    COMMON_DATABASE_ERROR = ("COMMON-03", 500, "데이터베이스 오류가 발생했습니다")
    COMMON_JSON_INVALID = ("COMMON-04", 400, "JSON 형식이 올바르지 않습니다")

    def __init__(self, code: str, status: int, description: str):
        self.code = code
        self.status = status
        self.description = description

    @property
    def value(self) -> str:
        return self.code


class APIResponse(BaseModel, Generic[T]):
    code: str
    data: Optional[T] = None

    model_config = {
        "json_schema_extra": {
            "properties": {"code": {"order": 1}, "data": {"order": 2}}
        }
    }


def success_response(data: Optional[T] = None) -> APIResponse[T]:
    return APIResponse(code=APIResponseCode.SUCCESS.code, data=data)


def error_response(code: APIResponseCode) -> APIResponse[None]:
    return APIResponse(code=code.code, data=None)


def warn_response(code: APIResponseCode) -> APIResponse[None]:
    return APIResponse(code=code.code, data=None)
