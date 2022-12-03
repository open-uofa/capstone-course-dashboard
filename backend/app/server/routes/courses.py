"""FastAPI routes for courses."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo.errors import OperationFailure

from server.config import settings
from server.models.courses import Course, Sprint
from server.util import jwt
from server.util.common import check_course_in_db, check_user_assigned_to_course

router = APIRouter()


@router.get(
    "/courses",
    description="Get a list of all courses.",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Courses are returned successfully"}},
    response_model=List[Course],
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_courses():
    """Get all courses."""
    courses = []
    for course in settings.database.courses.find():
        courses.append(Course(**course))
    return courses


@router.get(
    "/courses/{user_email}",
    description="Get a list of all courses authorized to a given user.",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Courses are returned successfully"}},
    response_model=List[Course],
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_courses_for_user(user_email: str):
    """Get all courses for a given user."""
    user_courses = settings.database.user.find_one({"email": user_email})
    courses = []
    for course in settings.database.courses.find():
        if course["name"] in user_courses["assigned_courses"]:
            courses.append(Course(**course))
    return courses


@router.post(
    "/courses",
    description="Create a new course and add the created course to assigned courses for the owner.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Course is created successfully"},
        400: {"description": "Course already exists"},
        422: {"description": "Invalid course data"},
    },
)
def create_course(
    course: Course, user_email: str = Depends(jwt.get_current_user_email)
):
    """Create a new course and add the created course to assigned courses for the owner."""
    # Check if course already exists
    col_exist_res = True
    try:
        settings.database.validate_collection(f"{course.name}.sprints")
    except OperationFailure:
        col_exist_res = False
    if col_exist_res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course {course.name} already exists",
        )

    # list of collections needed for a course
    collections_to_be_created = [
        ".sprints",
        ".comments",
        ".students",
        ".students.sprints",
        ".github.commits",
        ".minutes",
    ]
    for coll in collections_to_be_created:  # create all needed collections
        settings.database.create_collection(course.name + coll)
    # insert course into courses collection
    settings.database.courses.update_one(
        {"name": course.name}, {"$set": jsonable_encoder(course)}, upsert=True
    )
    # add course to user's assigned courses
    settings.database.user.update_one(
        {"email": user_email},
        {"$addToSet": {"assigned_courses": course.name}},
        upsert=True,
    )


@router.put(
    "/courses",
    description="Update a course.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Course updated successfully"},
        401: {
            "description": "User is not authorized or does not have permission to access the specified course"
        },
        404: {"description": "Course does not exist"},
        422: {"description": "Invalid course data"},
    },
)
def update_course(
    course: Course, user_email: str = Depends(jwt.get_current_user_email)
):
    """Update a course."""
    # Check if course exists
    check_course_in_db(course.name, [".sprints"])

    # Check if user has access to the course
    check_user_assigned_to_course(user_email, course.name)

    # Update course
    settings.database.courses.update_one(
        {"name": course.name}, {"$set": jsonable_encoder(course)}, upsert=True
    )


@router.delete(
    "/courses/{course_name}",
    description="Delete a course.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Course is deleted successfully"},
        401: {
            "description": "User is not authorized or does not have permission to access the specified course"
        },
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)
def delete_course(
    course_name: str, user_email: str = Depends(jwt.get_current_user_email)
):
    """Delete a course. Keep an eye on this to ensure all loose ends are tied up."""
    # Check if course exists.
    check_course_in_db(course_name, [".sprints"])

    # Check if user has access to the course
    check_user_assigned_to_course(user_email, course_name)

    # Drop all collections related to the course.
    collections_to_be_deleted = [
        ".sprints",
        ".comments",
        ".students",
        ".students.sprints",
        ".github.commits",
        ".minutes",
    ]
    for coll in collections_to_be_deleted:
        settings.database.drop_collection(course_name + coll)
    # Now remove course from courses collection.
    settings.database.courses.delete_one({"name": course_name})
    # Remove course from all users who have it under their assigned courses.
    settings.database.user.update_many(
        {"assigned_courses": course_name}, {"$pull": {"assigned_courses": course_name}}
    )


@router.get(
    "/courses/{course_name}/sprints",
    description="Get a list of all sprints for a course.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Sprints are returned successfully"},
        401: {
            "description": "User is not authorized or does not have permission to access the specified course"
        },
        404: {"description": "Course not found"},
    },
    response_model=List[Sprint],
)
def get_sprints(
    course_name: str, user_email: str = Depends(jwt.get_current_user_email)
):
    """Get all sprints for a course."""
    check_course_in_db(course_name, [".sprints"])

    # Check if user has access to the course
    check_user_assigned_to_course(user_email, course_name)

    coll = settings.database[course_name].sprints
    sprints = []
    for sprint in coll.find():
        sprints.append(Sprint(**sprint))

    return sprints


@router.post(
    "/courses/{course_name}/sprints",
    description="Create a new sprint.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Sprint created successfully"},
        400: {"description": "Sprint already exists"},
        401: {
            "description": "User is not authorized or does not have permission to access the specified course"
        },
        404: {"description": "Course not found"},
        422: {"description": "Invalid sprint data"},
    },
)
def create_sprint(
    course_name: str,
    sprint: Sprint,
    user_email: str = Depends(jwt.get_current_user_email),
):
    """Create a new sprint."""
    # check if course exists
    check_course_in_db(course_name, [".sprints"])

    # Check if user has access to the course
    check_user_assigned_to_course(user_email, course_name)

    # check if sprint already exists
    if (
        settings.database[course_name].sprints.count_documents(
            {"sprint_number": sprint.sprint_number}
        )
        != 0
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sprint {sprint.sprint_number} already exists",
        )
    # update or insert (upsert) sprint info
    settings.database[course_name].sprints.update_one(
        {"sprint_number": sprint.sprint_number},
        {"$set": jsonable_encoder(sprint)},
        upsert=True,
    )


@router.put(
    "/courses/{course_name}/sprints",
    description="Update a sprint.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Sprint updated successfully"},
        401: {
            "description": "User is not authorized or does not have permission to access the specified course"
        },
        404: {"description": "Course or sprint does not exist"},
        422: {"description": "Invalid sprint data"},
    },
)
def update_sprint(
    sprint: Sprint,
    course_name: str,
    user_email: str = Depends(jwt.get_current_user_email),
):
    """Update a course."""
    # Check if course exists
    check_course_in_db(course_name, [".sprints"])

    # Check if user has access to the course
    check_user_assigned_to_course(user_email, course_name)

    # Check if sprint exists
    if (
        settings.database[course_name].sprints.count_documents(
            {"sprint_number": sprint.sprint_number}
        )
        == 0
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sprint {sprint.sprint_number} does not exist",
        )

    # Update course
    settings.database[course_name].sprints.update_one(
        {"sprint_number": sprint.sprint_number},
        {"$set": jsonable_encoder(sprint)},
        upsert=True,
    )


@router.delete(
    "/courses/{course_name}/sprints/{sprint_number}",
    description="Delete a sprint and corresponding student data.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Sprint is deleted successfully"},
        401: {
            "description": "User is not authorized or does not have permission to access the specified course"
        },
        404: {"description": "Course not found"},
        500: {"description": "Internal server error"},
    },
)
def delete_sprint(
    course_name: str,
    sprint_number: int,
    user_email: str = Depends(jwt.get_current_user_email),
):
    """Delete a sprint and corresponding student data. Keep an eye on this to ensure all loose ends are tied up."""
    # Check if course exists.
    check_course_in_db(course_name, [".sprints"])

    # Check if user has access to the course
    check_user_assigned_to_course(user_email, course_name)

    # Now remove sprint from sprints collection.
    res = settings.database[course_name].sprints.delete_one(
        {"sprint_number": sprint_number}
    )
    if res.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sprint not found",
        )
    # Remove student data for the deleted sprint.
    settings.database[course_name].students.sprints.delete_many(
        {"sprint": sprint_number}
    )
