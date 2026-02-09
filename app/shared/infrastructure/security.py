import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

import jwt
from passlib.context import CryptContext

from app.config.logger import logger
from app.config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, JWT_SECRET_KEY, JWT_ALGORITHM, \
    JWT_EXPIRE_HOURS
from app.shared.api.exceptions import APIException
from app.shared.api.responses import APIResponseCode

# 비밀번호 해싱을 위한 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTManager:
    def __init__(self, token_repository=None):
        self.secret_key = _decode_secret_key(JWT_SECRET_KEY)
        self.algorithm = JWT_ALGORITHM
        self.expire_hours = JWT_EXPIRE_HOURS
        self.token_prefix = "Bearer "

        # 블랙리스트 토큰 저장소
        self.token_repository = token_repository

    def create_token(self, user_id: int, user_email: str, roles: List[str] = None) -> str:
        try:
            now = datetime.utcnow()
            expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

            payload = {
                "user_id": user_id,
                "user_email": user_email,
                "roles": roles or [],  # 역할 목록 추가
                "token_type": "access",
                "iat": now,
                "exp": expire,
                "iss": "fastapi-boilerplate"
            }

            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return f"{self.token_prefix}{token}"

        except Exception as e:
            logger.error(f"Access Token 생성 실패: {e}")
            raise APIException(APIResponseCode.AUTH_TOKEN_INVALID)

    def create_refresh_token(self, user_id: int, user_email: str, roles: List[str] = None) -> str:
        try:
            now = datetime.utcnow()
            expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

            payload = {
                "user_id": user_id,
                "user_email": user_email,
                "roles": roles or [],  # 역할 목록 추가
                "token_type": "refresh",
                "iat": now,
                "exp": expire,
                "iss": "fastapi-boilerplate"
            }

            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return f"{self.token_prefix}{token}"

        except Exception as e:
            logger.error(f"Refresh Token 생성 실패: {e}")
            raise APIException(APIResponseCode.AUTH_TOKEN_INVALID)

    def parse_token(self, token: str) -> str:
        if token and token.startswith(self.token_prefix):
            return token[len(self.token_prefix):]
        return token

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            pure_token = self.parse_token(token)

            payload = jwt.decode(
                pure_token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise APIException(APIResponseCode.AUTH_TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise APIException(APIResponseCode.AUTH_TOKEN_INVALID)
        except Exception:
            raise APIException(APIResponseCode.AUTH_TOKEN_INVALID)

    def get_user_id(self, token: str) -> int:
        payload = self.verify_token(token)
        return payload.get("user_id")

    def get_user_email(self, token: str) -> str:
        payload = self.verify_token(token)
        return payload.get("user_email")

    def get_user_roles(self, token: str) -> List[str]:
        payload = self.verify_token(token)
        return payload.get("roles", [])

    async def blacklist_token(self, token: str) -> bool:
        if self.token_repository:
            return await self.token_repository.blacklist_token(token)
        return True

    async def is_token_blacklisted(self, token: str) -> bool:
        if self.token_repository:
            return await self.token_repository.is_blacklisted(token)
        return False

    def verify_refresh_token(self, token: str) -> Dict[str, Any]:
        payload = self.verify_token(token)

        if payload.get("token_type") != "refresh":
            raise APIException(APIResponseCode.AUTH_TOKEN_INVALID)

        return payload

    async def auto_refresh_access_token(self, expired_token: str) -> Optional[str]:
        try:
            # 1. 만료된 토큰에서 user_id, roles 추출 (만료 검증 무시)
            payload = jwt.decode(
                self.parse_token(expired_token),
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": False}  # 만료 검증 무시
            )
            user_id = payload.get("user_id")
            user_email = payload.get("user_email")
            roles = payload.get("roles", [])

            if not user_id or not user_email:
                return None

            # 2. 저장된 Refresh Token 조회
            if not self.token_repository:
                return None

            refresh_token = await self.token_repository.get_user_refresh_token(user_id)
            if not refresh_token:
                return None

            # 3. Refresh Token 검증
            self.verify_refresh_token(refresh_token)

            # 4. 새 Access Token 생성 (roles 포함)
            new_access_token = self.create_token(user_id, user_email, roles)

            # todo: 나중에 set_access_token_cookie 호출해서 쿠키 저장해야 함.
            logger.info(f"자동 토큰 갱신 성공: user_id={user_id}")
            return new_access_token

        except Exception as e:
            logger.warning(f"자동 토큰 갱신 실패: {e}")
            return None


def _decode_secret_key(encoded_key: str) -> bytes:
    try:
        return base64.b64decode(encoded_key)
    except Exception as e:
        logger.error(f"JWT Secret Key 디코딩 실패: {e}")
        # Fallback: 문자열을 직접 바이트로 변환
        return encoded_key.encode('utf-8')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
