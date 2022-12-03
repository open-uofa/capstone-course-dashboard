"""Models related to meeting minutes."""

from pydantic import BaseModel, Field


class Minute(BaseModel):
    """Model for a meeting minute entry."""

    title: str = Field(example="September 4, 2021")
    body: str = Field(example="Agenda for today's meeting: ...")


class MinuteRequest(Minute):
    """Model for creating a meeting minute entry."""

    team: str = Field(example="team1")
    timestamp: str = Field(example="2021-09-04T12:00:00Z")
