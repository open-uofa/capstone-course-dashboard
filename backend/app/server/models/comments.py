"""Models related to TA comments."""

from typing import Optional

from pydantic import BaseModel, Field


class Comment(BaseModel):
    """Model for a comment."""

    message: str = Field(example="We had a good meeting today.")
    team: str = Field(example="Team 1")
    sprint_number: int = Field(example=1)


class UpdateComment(BaseModel):
    """Model for updating a comment.

    Can provide one or more fields.

    """

    message: Optional[str] = Field(example="We had a good meeting today.")
    team: Optional[str] = Field(example="Team 1")
    sprint_number: Optional[int] = Field(example=1)


class CommentResponse(Comment):
    """Model for a comment including the assigned ID."""

    id: str = Field(example="6351d670cc2cae4d305f2b97")
    created_at: str = Field(example="2021-03-25T12:00:00Z")
    last_modified_at: str = Field(example="2021-03-25T12:00:00Z")
