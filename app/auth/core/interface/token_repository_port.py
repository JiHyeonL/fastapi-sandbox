from abc import ABC, abstractmethod
from typing import Optional


class TokenRepositoryPort(ABC):

    @abstractmethod
    async def blacklist_token(self, token: str, user_id: int = None, expires_at=None) -> bool:
        pass

    @abstractmethod
    async def is_blacklisted(self, token: str) -> bool:
        pass

    @abstractmethod
    async def cleanup_expired_tokens(self) -> int:
        pass

    @abstractmethod
    async def store_user_refresh_token(self, user_id: int, refresh_token: str, ttl_seconds: int = None) -> bool:
        pass

    @abstractmethod
    async def get_user_refresh_token(self, user_id: int) -> Optional[str]:
        pass

    @abstractmethod
    async def revoke_user_refresh_token(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def cleanup_expired_refresh_tokens(self) -> int:
        pass
