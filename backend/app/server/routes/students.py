"""Fastapi routes for students"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from pymongo import UpdateOne

from server.config import settings
from server.models.students import Student, StudentSprintData, StudentsResponse
from server.util import jwt
from server.util.common import check_course_in_db
from server.util.students import parse_roster_data, parse_sprint_data

router = APIRouter()


@router.get(
    "/students/{course_name}/{sprint}",
    description="Get all students in a course for a given sprint. Specify sprint 0 for all sprints",
    responses={
        200: {
            "description": "Sprint data and Students with sprint data are returned for a course and sprint if any"
        },
        404: {"description": "Course not found"},
    },
    response_model=StudentsResponse,
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_students_in_course_sprint(course_name: str, sprint: int):
    """get students from a given course and sprint

    course_name and sprint are url parameters

    """

    check_course_in_db(course_name, [".students.sprints", ".students"])

    # query collections
    students_data = settings.database[course_name].students.find({})
    if sprint == 0:
        students_sprint_data = settings.database[course_name].students.sprints.find({})
    else:
        students_sprint_data = settings.database[course_name].students.sprints.find(
            {"sprint": sprint}
        )
    # create response from doc data
    student_list = []
    student_email_collection = set()
    sprint_data_list = []
    for sprint_data in students_sprint_data:
        sprint_data_list.append(StudentSprintData(**sprint_data))
        student_email_collection.add(sprint_data["email"])
    for student in students_data:
        # prevent students with no sprint data from being added to the list when sprint is specified
        if sprint != 0 and student["email"] in student_email_collection:
            student_list.append(Student(**student))
        elif sprint == 0:
            student_list.append(Student(**student))
    return StudentsResponse(students=student_list, sprint_data=sprint_data_list)


@router.get(
    "/students/{course_name}/{sprint}/{student_email}",
    description="Get a single student in a course for a given sprint by email. Specify sprint 0 to get all sprints",
    responses={
        200: {
            "description": "Sprint data and Student are returned for a course and sprint"
        },
        404: {"description": "Course, sprint, or student not found"},
    },
    response_model=StudentsResponse,
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_student_in_course_sprint(course_name: str, sprint: int, student_email: str):
    """get a student from a given course and sprint and email

    course_name, sprint, student_email are url parameters

    """

    check_course_in_db(course_name, [".students.sprints", ".students"])

    # query collections
    student_data = settings.database[course_name].students.find_one(
        {"email": student_email}
    )
    if student_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    if sprint == 0:
        student_sprints_data = settings.database[course_name].students.sprints.find(
            {"email": student_email}
        )
    else:
        student_sprints_data = settings.database[course_name].students.sprints.find(
            {"sprint": sprint, "email": student_email}
        )
    # create response from doc data
    student_data = Student(**student_data)
    sprint_data_list = []
    for sprint_data in student_sprints_data:
        sprint_data_list.append(StudentSprintData(**sprint_data))
    return StudentsResponse(students=[student_data], sprint_data=sprint_data_list)


@router.post(
    "/students/{course_name}/{sprint}",
    description="Post student data to a course, roster data must be sent with sprint 0 whereas sprint data must be sent with a sprint number greater than 0",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Student roster data is posted to course"},
        400: {"description": "Invalid sprint number"},
        404: {"description": "Course not found"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def post_student_data(course_name: str, sprint: int, file: UploadFile):
    """post student data to a course or sprint

    course_name and sprint is url parameter

    """
    if sprint < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Sprint must be >= 0"
        )

    if sprint == 0:  # if sprint is 0, parse roster data
        check_course_in_db(course_name, [".students"])

        # parse file
        student_list = parse_roster_data(file.file, course_name)

        # post to database
        coll = settings.database[course_name].students
        # coll = settings.database.temptest.students  # for testing
        batch_req = [
            UpdateOne(
                {"email": student.email},
                {"$set": jsonable_encoder(student)},
                upsert=True,
            )
            for student in student_list
        ]
        # update course metadata
        settings.database.courses.update_one(
            {"name": course_name}, {"$set": {"roster_file_name": file.filename}}
        )
    else:  # if sprint is > 0, parse sprint data
        check_course_in_db(course_name, [".students.sprints"])

        # parse file
        sprint_data_list = parse_sprint_data(file.file, sprint)

        # post to database
        coll = settings.database[course_name].students.sprints
        # coll = settings.database.temptest.students.sprints  # for testing
        batch_req = [
            UpdateOne(
                {"email": sprint_data.email, "sprint": sprint_data.sprint},
                {"$set": jsonable_encoder(sprint_data)},
                upsert=True,
            )
            for sprint_data in sprint_data_list
        ]
        # update course sprint metadata
        settings.database[course_name].sprints.update_one(
            {"sprint": sprint}, {"$set": {"sprint_file_name": file.filename}}
        )

    coll.bulk_write(batch_req)
