"""Common utilities for the backend app."""

from typing import List

from fastapi import HTTPException, status

from server.config import settings


def check_course_in_db(course_name: str, colls: List[str]):
    """Check if a course is in the database.

    Where colls is a list of subcollection names listed under a course.
    Ex. course_name = "cmput401w22", colls = [".students", ".students.sprints"]

    Raises HTTPException if course is not in the database.

    """
    try:
        for coll in colls:
            settings.database.validate_collection(course_name + coll)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course {course_name} does not exist",
        ) from exc


def get_sprint_list(course_name: str):
    """Get a list of sprints for a course."""
    check_course_in_db(course_name, [".sprints"])
    coll = settings.database[course_name].sprints
    sprints = []
    for sprint in coll.find():
        sprints.append(sprint["sprint_number"])
    return sorted(list(sprints))


def check_user_assigned_to_course(user_email: str, course_name: str):
    """Check if a user is assigned to a course.

    Raises HTTPException if user is not assigned to the course.

    """
    user_courses = settings.database.user.find_one({"email": user_email})
    if user_courses is not None:
        if course_name not in user_courses["assigned_courses"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"User {user_email} is not authorized to access {course_name}",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {user_email} does not exist",
        )
