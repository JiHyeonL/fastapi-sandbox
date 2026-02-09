from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from app.users.core.domain.user_profile import UserProfile


@dataclass
class User:
    id: Optional[int] = None
    email: str = ""
    password_hash: str = ""
    name: Optional[str] = None
    is_active: bool = True
    roles: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    profile: Optional[UserProfile] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def update_name(self, new_name: str) -> None:
        self.name = new_name
        self.updated_at = datetime.now()

    def update_password(self, new_password_hash: str) -> None:
        self.password_hash = new_password_hash
        self.updated_at = datetime.now()

    def record_login(self) -> None:
        self.last_login = datetime.now()
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now()

    def add_role(self, role: str) -> None:
        if role not in self.roles:
            self.roles.append(role)
            self.updated_at = datetime.now()

    def remove_role(self, role: str) -> None:
        if role in self.roles:
            self.roles.remove(role)
            self.updated_at = datetime.now()

    def has_role(self, role: str) -> bool:
        return role in self.roles

    def has_any_role(self, roles: List[str]) -> bool:
        return any(role in self.roles for role in roles)

    @property
    def is_admin(self) -> bool:
        return "Admin" in self.roles

    def is_valid_for_login(self) -> bool:
        return self.is_active and bool(self.password_hash)

    def is_password_set(self) -> bool:
        return bool(self.password_hash)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}', is_active={self.is_active})>"
