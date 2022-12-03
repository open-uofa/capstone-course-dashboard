"""
Models for storing student data.
The models here can have fields added or removed as needed
for different courses. The changes should apply to all endpoints dealing
with these models automatically. Note that existing database
entries and data import/export functions will need to be
manually updated.
"""
from typing import List

from pydantic import BaseModel, Field


class Student(BaseModel):
    # email is treated as the primary key, avoid changing
    email: str = Field(example="cat@ualberta.ca")
    full_name: str = Field(example="Cat Caterson")
    source_control_username: str = Field(example="codecat")
    project: str = Field(example="super cool project")
    repo_name: str = Field(example="super-cool-project")
    ta: str = Field(example="Bobert")
    # grade: int = Field(example=10)
    course_name: str = Field(example="CMPUT 401")
    form_submitted: bool = Field(example=False)
    experience_survey: dict = Field(
        example={"experience": "I have a lot of experience"}
    )

    class Config:
        allow_population_by_field_name = True


class StudentSprintData(BaseModel):
    # identifying information
    # email is treated as the primary key, avoid changing
    email: str = Field(example="cat@ualberta.ca")
    sprint: int = Field(example=1)

    # sprint data
    personal_peer_rev: dict = Field(example={"workcompleted": "task A"})
    received_peer_revs: dict = Field(example={"monkey@ualberta.ca": {"rating": 3}})
    avg_rating: float = Field(example=3.0)
    stddev_rating: float = Field(example=1.5)


class StudentsResponse(BaseModel):
    # course level student information will be stored in its own collection
    students: List[Student] = Field(...)
    # sprint level student information will be stored in a separate collection
    sprint_data: List[StudentSprintData] = Field(...)
