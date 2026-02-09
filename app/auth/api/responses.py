from pydantic import BaseModel, Field

from app.users.api.responses import UserResponse


class RegisterResponse(BaseModel):
    access_token: str = Field(..., description="JWT 액세스 토큰")
    user: UserResponse = Field(..., description="생성된 사용자 정보")
