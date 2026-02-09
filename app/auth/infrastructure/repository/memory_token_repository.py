from datetime import datetime, timedelta
from typing import Set, Dict, Optional

from app.auth.core.interface.token_repository_port import TokenRepositoryPort
from app.config.logger import logger


class MemoryTokenRepository(TokenRepositoryPort):

    def __init__(self):
        self._blacklisted_tokens: Set[str] = set()
        self._refresh_tokens: Dict[int, tuple[str, datetime]] = {}
        logger.info("메모리 기반 토큰 저장소 초기화")

    async def blacklist_token(self, token: str, user_id: int = None, expires_at=None) -> bool:
        try:
            clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
            self._blacklisted_tokens.add(clean_token)

            logger.info(f"토큰 블랙리스트 추가 (메모리): {clean_token[:20]}...")
            return True

        except Exception as e:
            logger.error(f"토큰 블랙리스트 추가 실패 (메모리): {e}")
            return False

    async def is_blacklisted(self, token: str) -> bool:
        try:
            clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
            is_blacklisted = clean_token in self._blacklisted_tokens

            if is_blacklisted:
                logger.warning(f"블랙리스트된 토큰 접근 시도 (메모리): {clean_token[:20]}...")

            return is_blacklisted

        except Exception as e:
            logger.error(f"토큰 블랙리스트 확인 실패 (메모리): {e}")
            return False

    async def cleanup_expired_tokens(self) -> int:
        try:
            cleaned_count = len(self._blacklisted_tokens)
            self._blacklisted_tokens.clear()

            logger.info(f"메모리 토큰 저장소 정리 완료: {cleaned_count}개 토큰")
            return cleaned_count

        except Exception as e:
            logger.error(f"토큰 정리 실패 (메모리): {e}")
            return 0

    async def store_user_refresh_token(self, user_id: int, refresh_token: str, ttl_seconds: int = None) -> bool:
        try:
            expires_at = datetime.utcnow() + timedelta(
                seconds=ttl_seconds) if ttl_seconds else datetime.utcnow() + timedelta(days=7)
            self._refresh_tokens[user_id] = (refresh_token, expires_at)

            logger.info(f"Refresh Token 저장 (메모리): user_id={user_id}")
            return True

        except Exception as e:
            logger.error(f"Refresh Token 저장 실패 (메모리): {e}")
            return False

    async def get_user_refresh_token(self, user_id: int) -> Optional[str]:
        try:
            if user_id not in self._refresh_tokens:
                return None

            refresh_token, expires_at = self._refresh_tokens[user_id]

            if datetime.utcnow() > expires_at:
                del self._refresh_tokens[user_id]
                logger.info(f"만료된 Refresh Token 삭제 (메모리): user_id={user_id}")
                return None

            return refresh_token

        except Exception as e:
            logger.error(f"Refresh Token 조회 실패 (메모리): {e}")
            return None

    async def revoke_user_refresh_token(self, user_id: int) -> bool:
        try:
            if user_id in self._refresh_tokens:
                del self._refresh_tokens[user_id]
                logger.info(f"Refresh Token 삭제 (메모리): user_id={user_id}")
            return True

        except Exception as e:
            logger.error(f"Refresh Token 삭제 실패 (메모리): {e}")
            return False

    async def cleanup_expired_refresh_tokens(self) -> int:
        try:
            current_time = datetime.utcnow()
            expired_users = []

            for user_id, (token, expires_at) in self._refresh_tokens.items():
                if current_time > expires_at:
                    expired_users.append(user_id)

            for user_id in expired_users:
                del self._refresh_tokens[user_id]

            logger.info(f"만료된 Refresh Token 정리 (메모리): {len(expired_users)}개")
            return len(expired_users)

        except Exception as e:
            logger.error(f"Refresh Token 정리 실패 (메모리): {e}")
            return 0
