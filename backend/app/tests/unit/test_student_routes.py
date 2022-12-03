"""Test API functions for handling students."""
import os

from server.routes import students
from tests.unit import mock_data


def test_get_students_in_course_sprint(mocker):
    """Test successfully getting all students' details for a specified sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.students.check_course_in_db")
    mock_find = mocker.patch("pymongo.collection.Collection.find")
    mock_find.side_effect = [[mock_data.STUDENT_JSON], [mock_data.STUDENT_SPRINT_JSON]]
    students_response = students.get_students_in_course_sprint("test_course", 1)
    mock_check_course_in_db.assert_called_once()
    assert mock_find.call_count == 2
    assert students_response == mock_data.STUDENTS_RESPONSE


def test_get_student_in_course_sprint(mocker):
    """Test successfully getting a student's details for a specified sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.students.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one", return_value=mock_data.STUDENT_JSON
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find",
        return_value=[mock_data.STUDENT_SPRINT_JSON],
    )
    students_response = students.get_student_in_course_sprint(
        "test_course", 1, "test_email"
    )
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once()
    mock_find.assert_called_once()
    assert students_response == mock_data.STUDENTS_RESPONSE


def test_post_student_data_roster(mocker, datadir):
    """Test successfully uploading student course data to the database."""
    mock_check_course_in_db = mocker.patch("server.routes.students.check_course_in_db")
    mock_bulk_write = mocker.patch("pymongo.collection.Collection.bulk_write")
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")
    # mock_parse_roster_data = mocker.patch(
    #     f"{mock_data.STUDENT_UTILS_PATH}.parse_roster_data"
    # )
    with open(os.path.join(datadir, "test_roster.csv"), "r", encoding="utf-8") as file:
        roster_data = mock_data.MockFileWrapper(
            os.path.join(datadir, "test_roster.csv"), file
        )
        students.post_student_data("test_course", 0, roster_data)
    mock_check_course_in_db.assert_called_once()
    # mock_parse_roster_data.assert_called_once_with(roster_data.file, "test_course")
    mock_bulk_write.assert_called_once_with(mock_data.STUDENT_ROSTER_POST)
    mock_update_one.assert_called_once()


def test_post_student_data_sprint(mocker, datadir):
    """Test successfully uploading student sprint data to the database."""
    mock_check_course_in_db = mocker.patch("server.routes.students.check_course_in_db")
    mock_bulk_write = mocker.patch("pymongo.collection.Collection.bulk_write")
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")
    # mock_parse_sprint_data = mocker.patch(
    #     f"{mock_data.STUDENT_UTILS_PATH}.parse_sprint_data"
    # )
    with open(os.path.join(datadir, "test_sprint1.csv"), "r", encoding="utf-8") as file:
        sprint_data = mock_data.MockFileWrapper(
            os.path.join(datadir, "test_sprint1.csv"), file
        )
        students.post_student_data("test_course", 1, sprint_data)
    mock_check_course_in_db.assert_called_once()
    # assert mock_parse_sprint_data.call_count == 1
    mock_bulk_write.assert_called_once_with(mock_data.STUDENT_SPRINT_POST)
    mock_update_one.assert_called_once()
