from fastapi import Response

from app.config.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


class CookieManager:
    ACCESS_TOKEN_KEY = "access_token"
    REFRESH_TOKEN_KEY = "refresh_token"

    @staticmethod
    def set_auth_cookies(
            response: Response,
            access_token: str,
            refresh_token: str,
            access_token_key: str = None,
            refresh_token_key: str = None
    ) -> None:
        response.set_cookie(
            key=access_token_key,
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

        response.set_cookie(
            key=refresh_token_key,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
        )

    @staticmethod
    def set_access_token_cookie(
            response: Response,
            access_token: str
    ):
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 15분
        )

    @staticmethod
    def clear_auth_cookies(
            response: Response,
            access_token_key: str = None,
            refresh_token_key: str = None
    ) -> None:
        response.delete_cookie(
            key=access_token_key,
            httponly=True,
            secure=True,
            samesite="lax"
        )

        response.delete_cookie(
            key=refresh_token_key,
            httponly=True,
            secure=True,
            samesite="lax"
        )
