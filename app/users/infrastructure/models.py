from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.infrastructure.base import Base


class UserDB(Base):
    __tablename__ = "tb_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False, comment="이메일")
    name: Mapped[str] = mapped_column(String(100), nullable=True, comment="이름")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True, comment="해싱된 비밀번호")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="활성 여부 (소프트 삭제용)")
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="마지막 로그인 시간")
    profile: Mapped["UserDBProfile"] = relationship(
        "UserDBProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="select"
    )

    def __repr__(self):
        return f"<UserDB(email='{self.email}', name='{self.name}')>"


class UserDBProfile(Base):
    __tablename__ = "tb_user_profiles"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tb_users.id", ondelete="CASCADE"),
        primary_key=True,
        comment="사용자 ID"
    )
    bio: Mapped[str] = mapped_column(Text, nullable=True, comment="자기소개")
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True, comment="아바타 URL")
    phone: Mapped[str] = mapped_column(String(20), nullable=True, comment="전화번호")
