"""Models for storing GitHub data."""
from typing import List, Optional

from pydantic import BaseModel, Field


class GithubRequest(BaseModel):
    """Model for a GitHub request."""

    owner: str = Field(example="illinois-cs241")
    repo: str = Field(example="coursebook")
    course_name: str = Field(example="CS241-w22")


class Commit(BaseModel):
    """Model for storing GitHub commit data."""

    sha: str = Field(description="Commit SHA.", example="a1b2c3d4e5f6g7h8i9j0")
    author: str = Field(
        description="GitHub username of the commit author", example="cs241-bot"
    )
    timestamp: str = Field(
        description="Date of the commit.", example="2021-09-01T00:00:00Z"
    )
    message: str = Field(description="Commit message.", example="Update README.md")
    repo_name: str = Field(
        description="Name of the repository the commit was made in.",
        example="coursebook",
    )
    fetched_at: str = Field(
        description="Date the commit was fetched from GitHub.",
        example="2021-09-01T00:00:00Z",
    )


class StudentCommit(BaseModel):
    username: str = Field()
    number_of_commits: int = Field()


class TeamCommit(BaseModel):
    team_name: str = Field()
    number_of_commits: int = Field()


class TeamCommits(BaseModel):
    student_commits: List[StudentCommit] = Field(description="List of student commits.")
    last_fetched_at: Optional[str] = Field(
        description="Date the data was last fetched from GitHub.",
        example="2021-09-01T00:00:00Z",
    )
