import datetime
from dataclasses import field
from typing import Optional, List

from pydantic import BaseModel


class UserCreateOutput(BaseModel):
    id: Optional[int] = None
    email: str = ""
    password_hash: str = ""
    name: Optional[str] = None
    is_active: bool = True
    roles: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
