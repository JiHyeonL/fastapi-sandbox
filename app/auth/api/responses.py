from pydantic import BaseModel, Field

from app.users.api.responses import UserResponse


class RegisterResponse(BaseModel):
    access_token: str = Field(..., description="JWT 액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    expires_in: int = Field(..., description="토큰 만료 시간(초)")
    user: UserResponse = Field(..., description="생성된 사용자 정보")
