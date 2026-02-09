from pydantic import BaseModel, Field

from app.users.core.application.outputs import UserCreateOutput


class RegisterOutput(BaseModel):
    access_token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh Token")
    user_create_output: UserCreateOutput = Field(..., description="회원가입 한 유저 정보")
