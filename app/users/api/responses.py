from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
