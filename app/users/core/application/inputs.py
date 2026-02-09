from pydantic import BaseModel, Field, EmailStr


class UserCreateInput(BaseModel):
    email: EmailStr = Field(..., description="사용자 이메일")
    password: str = Field(..., description="비밀번호")
    name: str | None = Field(None, description="사용자 이름")
