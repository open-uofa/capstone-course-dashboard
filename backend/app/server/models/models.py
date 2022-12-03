"""Models for miscellaneous data."""
from typing import List, Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    email: str = Field(...)
    assigned_courses: List[str] = Field(...)
    authorized: Optional[bool] = False


class AuthRequest(BaseModel):
    token: str = Field(example="string")


class RefreshRequest(BaseModel):
    grant_type: str = Field(example="string")
    refresh_token: str = Field(example="string")
