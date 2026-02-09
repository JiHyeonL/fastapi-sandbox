from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일")
    password: str = Field(..., min_length=8, description="비밀번호 (최소 8자)")
    name: str | None = Field(None, max_length=100, description="사용자 이름")
