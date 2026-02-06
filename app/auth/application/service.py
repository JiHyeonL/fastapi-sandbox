from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:

    def __init__(self, token_repository: TokenRepository, user_port: UserService):
        self.token_repository = token_repository
        self.user_port = user_port  # User 도메인과의 통신은 Port를 통해
        self.jwt_manager = JWTManager(token_repository)

    async def register(self, db: AsyncSession, email: str, password: str, name: str = None) -> Tuple[str, str, "User"]:
        """
        사용자 회원가입 및 자동 로그인 (Access + Refresh Token 쌍 발급)

        Args:
            db: 데이터베이스 세션
            email: 사용자 이메일
            password: 비밀번호
            name: 사용자 이름

        Returns:
            Tuple[str, str, User]: (Access Token, Refresh Token, 사용자 객체)
        """
        # 사용자 생성 (Port를 통해 User 도메인 호출)
        user = await self.user_port.create_user(
            db=db,
            email=email,
            password=password,
            name=name,
        )

        # Access + Refresh Token 쌍 생성
        access_token = self.jwt_manager.create_token(
            user_id=user.id,
            user_email=user.email
        )

        refresh_token = self.jwt_manager.create_refresh_token(
            user_id=user.id,
            user_email=user.email
        )

        # Refresh Token 저장
        ttl_seconds = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        await self.token_repository.store_user_refresh_token(
            user_id=user.id,
            refresh_token=refresh_token,
            ttl_seconds=ttl_seconds
        )

        logger.info(f"회원가입 및 자동 로그인 성공: {email}")
        return access_token, refresh_token, user
