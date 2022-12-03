"""Fastapi routes for data export."""
import io

import pandas as pd
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from server.config import settings
from server.models.students import Student, StudentSprintData
from server.util import jwt
from server.util.common import check_course_in_db, get_sprint_list
from server.util.dataexport import roster_data_to_df, sprint_data_to_df

router = APIRouter()


@router.get(
    "/export/all/{course_name}",
    description="Export all data for a course. Response will be a multi-sheet excel file.",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    responses={
        200: {"description": "Data exported successfully"},
        404: {"description": "Course not found"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def export_all_data(course_name: str):
    """
    Export all data for a course.
    Response will be an xlsx where roster and each sprint are on separate sheets.
    """
    check_course_in_db(course_name, [".students", ".students.sprints"])
    # get data from db
    sprint_list = get_sprint_list(course_name)
    spr_coll = settings.database[course_name].students.sprints
    student_docs = list(settings.database[course_name].students.find())
    # create team map
    student_team_map = {}
    for student in student_docs:
        student_team_map[student["email"]] = student["project"]
    # create Student list
    students = []
    for student in student_docs:
        students.append(Student(**student))

    # create excel writer
    file_stream = io.BytesIO()
    writer = pd.ExcelWriter(file_stream)  # pylint: disable=abstract-class-instantiated

    # create roster sheet
    data_df = roster_data_to_df(students)
    data_df.to_excel(writer, sheet_name="Roster", index=False)

    # create a sheet for each sprint
    for sprint in sprint_list:
        # get all student sprint data for a given sprint into a list
        sprint_docs = spr_coll.find({"sprint": sprint})
        sprints = []
        for sprint_doc in sprint_docs:
            sprints.append(StudentSprintData(**sprint_doc))

        # convert to dataframe
        data_df = sprint_data_to_df(sprints, student_team_map)
        data_df.to_excel(writer, sheet_name=f"Sprint {sprint}", index=False)

    # save excel file
    writer.close()

    # build response
    response = StreamingResponse(
        io.BytesIO(file_stream.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename={course_name}_all.xlsx"
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"

    return response


@router.get(
    "/export/roster/{course_name}",
    description="Export roster data for a course.",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    responses={
        200: {"description": "Roster exported successfully"},
        404: {"description": "Course not found"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def export_roster_data(course_name: str):
    """Export roster data for a course."""
    check_course_in_db(course_name, [".students"])

    # get all student data into a list
    coll = settings.database[course_name].students
    students = []
    for student in coll.find():
        students.append(Student(**student))

    # convert to csv
    csv_df = roster_data_to_df(students)
    file_stream = io.StringIO()
    csv_df.to_csv(file_stream, index=False)

    # build response
    response = StreamingResponse(iter([file_stream.getvalue()]), media_type="text/csv")
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename={course_name}_roster.csv"
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"

    return response


@router.get(
    "/export/sprint/{course_name}/{sprint}",
    description="Export sprint data for a course. If sprint is a valid int but not an existing sprint, an empty csv will be returned.",
    status_code=status.HTTP_200_OK,
    response_class=StreamingResponse,
    responses={
        200: {"description": "Sprint exported successfully"},
        404: {"description": "Course not found"},
        422: {"description": "Likely bad sprint parameter"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def export_sprint_data(course_name: str, sprint: int):
    """
    Export sprint data for a course.
    This route does not support sprint=0 since exporting all sprints
    into a single file would be messy.
    """
    check_course_in_db(course_name, [".students", ".students.sprints"])

    # get all student sprint data for a given sprint into a list
    spr_coll = settings.database[course_name].students.sprints
    stu_coll = settings.database[course_name].students
    sprint_docs = spr_coll.find({"sprint": sprint})
    student_docs = stu_coll.find()
    sprints = []
    for sprint_doc in sprint_docs:
        sprints.append(StudentSprintData(**sprint_doc))
    student_team_map = {}
    for student in student_docs:
        student_team_map[student["email"]] = student["project"]

    # convert to csv
    csv_df = sprint_data_to_df(sprints, student_team_map)
    file_stream = io.StringIO()
    csv_df.to_csv(file_stream, index=False)

    # build response
    response = StreamingResponse(iter([file_stream.getvalue()]), media_type="text/csv")
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename={course_name}_sprint_{sprint}.csv"
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"

    return response
