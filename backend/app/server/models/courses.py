"""Models related to courses."""

from pydantic import BaseModel, Field


class Course(BaseModel):
    """Model for a course."""

    name: str = Field(example="CMPUT 401 W22")
    roster_file_name: str = Field(example="roster.csv")
    use_github: bool = Field(example=True)
    use_team_structure: bool = Field(example=True)
    use_student_experience_form: bool = Field(example=True)


class Sprint(BaseModel):
    """Model for a course sprint."""

    sprint_number: int = Field(example=1)
    start_date: str = Field(example="2020-01-01T00:00:00Z")
    end_date: str = Field(example="2020-01-29T00:00:00Z")
    sprint_file_name: str = Field(example="sprint1.csv")
    forms_url: str = Field(
        example="https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?output=csv"
    )
