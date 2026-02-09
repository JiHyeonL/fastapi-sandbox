from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.api.auth_api_mapper import AuthAPIMapper
from app.auth.api.requests import RegisterRequest
from app.auth.api.responses import RegisterResponse
from app.auth.core.application.auth_service import AuthService
from app.auth.dependencies import get_auth_service
from app.shared.api.cookie_manager import CookieManager
from app.shared.api.responses import APIResponse, success_response, APIResponseCode
from app.shared.infrastructure.transaction import get_transaction_db

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/register", response_model=APIResponse[RegisterResponse])
async def register(
        request: RegisterRequest,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service),
        db: AsyncSession = Depends(get_transaction_db)
):
    register_input = AuthAPIMapper.register_request_to_input(request)
    register_output = await auth_service.register(db=db, register_data=register_input)

    CookieManager.set_auth_cookies(
        response,
        register_output.access_token,
        register_output.refresh_token,
        "access_token",
        "refresh_token"
    )

    return success_response(
        APIResponseCode.CREATED,
        AuthAPIMapper.register_output_to_response(register_output)
    )
