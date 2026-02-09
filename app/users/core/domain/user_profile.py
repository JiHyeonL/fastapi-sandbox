from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UserProfile:
    user_id: int = 0
    bio: Optional[str] = None
    phone: Optional[str] = None
    additional_info: dict = field(default_factory=dict)
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def update_info(self, **new_info) -> None:
        self.additional_info.update(new_info)
        self.updated_at = datetime.now()

    def update_bio(self, bio: str) -> None:
        self.bio = bio
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        return f"<UserProfile(user_id={self.user_id}, bio={self.bio[:20] if self.bio else None}...)>"
