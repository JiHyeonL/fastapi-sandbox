"""
Redis Token Repository Adapter - Redis 기반 토큰 저장소
"""
import json
from datetime import datetime
from typing import Optional

import redis.asyncio as redis

from app.auth.core.ports.token_repository_port import TokenRepositoryPort
from app.config.logger import logger
from app.config.settings import REDIS_URL, JWT_EXPIRE_HOURS


class RedisTokenRepository(TokenRepositoryPort):

    def __init__(self, redis_url: str = REDIS_URL):
        self.redis_url = redis_url
        self._redis_client: Optional[redis.Redis] = None
        self.blacklist_key_prefix = "blacklist:token:"
        self.refresh_key_prefix = "refresh_user:"  # Refresh Token 전용 프리픽스
        logger.info(f"Redis 토큰 저장소 초기화: {redis_url}")

    async def _get_redis_client(self) -> redis.Redis:
        if self._redis_client is None:
            self._redis_client = redis.from_url(
                self.redis_url,
                decode_responses=True,
                retry_on_timeout=True
            )
        return self._redis_client

    async def blacklist_token(self, token: str, user_id: int = None, expires_at=None) -> bool:
        try:
            redis_client = await self._get_redis_client()

            clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token

            redis_key = f"{self.blacklist_key_prefix}{clean_token}"

            token_info = {
                "user_id": user_id,
                "blacklisted_at": datetime.utcnow().isoformat(),
                "expires_at": expires_at.isoformat() if expires_at else None
            }

            if expires_at:
                ttl = int((expires_at - datetime.utcnow()).total_seconds())
            else:
                ttl = JWT_EXPIRE_HOURS * 3600  # 기본 만료시간

            await redis_client.setex(
                redis_key,
                ttl,
                json.dumps(token_info)
            )

            logger.info(f"토큰 블랙리스트 추가 (Redis): {clean_token[:20]}..., TTL: {ttl}s")
            return True

        except Exception as e:
            logger.error(f"토큰 블랙리스트 추가 실패 (Redis): {e}")
            return False

    async def is_blacklisted(self, token: str) -> bool:
        try:
            redis_client = await self._get_redis_client()

            # Bearer 프리픽스 제거
            clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token

            # Redis 키 확인
            redis_key = f"{self.blacklist_key_prefix}{clean_token}"
            token_info = await redis_client.get(redis_key)

            is_blacklisted = token_info is not None

            if is_blacklisted:
                logger.warning(f"블랙리스트된 토큰 접근 시도 (Redis): {clean_token[:20]}...")

            return is_blacklisted

        except Exception as e:
            logger.error(f"토큰 블랙리스트 확인 실패 (Redis): {e}")
            return False

    async def cleanup_expired_tokens(self) -> int:
        try:
            redis_client = await self._get_redis_client()

            pattern = f"{self.blacklist_key_prefix}*"
            keys = await redis_client.keys(pattern)

            if not keys:
                return 0

            # 만료된 키들 확인 및 정리
            cleaned_count = 0
            for key in keys:
                ttl = await redis_client.ttl(key)
                # TTL이 0보다 작으면 이미 만료되었거나 TTL이 설정되지 않음
                if ttl < 0:
                    await redis_client.delete(key)
                    cleaned_count += 1

            if cleaned_count > 0:
                logger.info(f"Redis 토큰 정리 완료: {cleaned_count}개 토큰")

            return cleaned_count

        except Exception as e:
            logger.error(f"토큰 정리 실패 (Redis): {e}")
            return 0

    async def store_user_refresh_token(self, user_id: int, refresh_token: str, ttl_seconds: int = None) -> bool:
        try:
            redis_client = await self._get_redis_client()

            redis_key = f"{self.refresh_key_prefix}{user_id}"
            ttl = ttl_seconds if ttl_seconds else 7 * 24 * 3600  # 기본 7일

            await redis_client.setex(redis_key, ttl, refresh_token)

            logger.info(f"Refresh Token 저장 (Redis): user_id={user_id}, TTL={ttl}s")
            return True

        except Exception as e:
            logger.error(f"Refresh Token 저장 실패 (Redis): {e}")
            return False

    async def get_user_refresh_token(self, user_id: int) -> Optional[str]:
        try:
            redis_client = await self._get_redis_client()

            redis_key = f"{self.refresh_key_prefix}{user_id}"
            refresh_token = await redis_client.get(redis_key)

            return refresh_token

        except Exception as e:
            logger.error(f"Refresh Token 조회 실패 (Redis): {e}")
            return None

    async def revoke_user_refresh_token(self, user_id: int) -> bool:
        try:
            redis_client = await self._get_redis_client()

            redis_key = f"{self.refresh_key_prefix}{user_id}"
            result = await redis_client.delete(redis_key)

            logger.info(f"Refresh Token 삭제 (Redis): user_id={user_id}, deleted={result}")
            return True

        except Exception as e:
            logger.error(f"Refresh Token 삭제 실패 (Redis): {e}")
            return False

    async def cleanup_expired_refresh_tokens(self) -> int:
        try:
            redis_client = await self._get_redis_client()

            pattern = f"{self.refresh_key_prefix}*"
            keys = await redis_client.keys(pattern)

            # TTL이 만료된 키들 정리
            cleaned_count = 0
            for key in keys:
                ttl = await redis_client.ttl(key)
                if ttl < 0:  # 만료되었지만 아직 삭제되지 않은 키
                    await redis_client.delete(key)
                    cleaned_count += 1

            if cleaned_count > 0:
                logger.info(f"Redis Refresh Token 정리 완료: {cleaned_count}개")

            return cleaned_count

        except Exception as e:
            logger.error(f"Refresh Token 정리 실패 (Redis): {e}")
            return 0

    async def close(self):
        if self._redis_client:
            await self._redis_client.close()
            logger.info("Redis 연결 종료")
