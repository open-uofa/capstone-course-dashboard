"""Unit tests for the course routes."""

import pymongo
import pytest
from fastapi import HTTPException
from pymongo.errors import OperationFailure

from server.routes import courses
from tests.unit import mock_data


def test_get_courses(mocker):
    """Test successfully getting all courses from the database."""
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find", return_value=[mock_data.COURSE_JSON]
    )
    course_list = courses.get_courses()
    mock_find.assert_called_once()
    assert course_list == [mock_data.COURSE]


def test_get_courses_empty(mocker):
    """Test a successful empty response when there are no courses in the database."""
    mock_find = mocker.patch("pymongo.collection.Collection.find", return_value=[])

    course_list = courses.get_courses()
    mock_find.assert_called_once()
    assert not course_list


def test_create_course(mocker):
    """Test successfully creating a new course."""
    mock_create_collection = mocker.patch("pymongo.database.Database.create_collection")
    mock_validate_course = mocker.patch(
        "pymongo.database.Database.validate_collection",
        side_effect=OperationFailure(""),
    )
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")

    courses.create_course(
        mock_data.COURSE,
        "user_email",
    )
    for coll in mock_data.CREATED_COLLS:
        mock_create_collection.assert_any_call("course_name" + coll)
    mock_validate_course.assert_called_once()
    assert mock_create_collection.call_count == len(mock_data.CREATED_COLLS)
    assert mock_update_one.call_count == 2


def test_get_courses_for_user(mocker):
    """Test successfully getting all courses for a user from the database."""
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one", return_value=mock_data.USER_JSON
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find", return_value=[mock_data.COURSE_JSON]
    )
    course_list = courses.get_courses_for_user("test_email")
    mock_find_one.assert_called_once_with({"email": "test_email"})
    mock_find.assert_called_once()
    assert course_list == [mock_data.COURSE]


def test_delete_course(mocker):
    """Test successfully deleting a single course from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_drop_collection = mocker.patch("pymongo.database.Database.drop_collection")
    mock_delete_one = mocker.patch("pymongo.collection.Collection.delete_one")
    mock_update_many = mocker.patch("pymongo.collection.Collection.update_many")

    courses.delete_course("test_course", "test_email")
    mock_check_course_in_db.assert_called_once_with("test_course", [".sprints"])
    mock_check_user_assigned.assert_called_once_with("test_email", "test_course")
    assert mock_drop_collection.call_count == len(mock_data.CREATED_COLLS)
    mock_delete_one.assert_called_once_with({"name": "test_course"})
    mock_update_many.assert_called_once_with(
        {"assigned_courses": "test_course"},
        {"$pull": {"assigned_courses": "test_course"}},
    )


def test_delete_course_invalid_course(mocker):
    """Test 404 error when deleting a course that does not exist."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.courses.check_course_in_db", side_effect=HTTPException(404)
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.delete_course("test_course")
    mock_check_course_in_db.assert_called_once_with("test_course", [".sprints"])
    assert exc_info.value.status_code == 404


def test_delete_course_user_unassigned(mocker):
    """Test 401 error when deleting a course that the user is not assigned to."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course",
        side_effect=HTTPException(401),
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.delete_course("test_course", "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "test_course")
    assert exc_info.value.status_code == 401


def test_get_sprints(mocker):
    """Test successfully getting all sprints for a course from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find", return_value=[mock_data.SPRINT_JSON]
    )
    sprints = courses.get_sprints("course_name", "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_find.assert_called_once()
    assert sprints == [mock_data.SPRINT]


def test_get_sprints_user_unassigned(mocker):
    """Test 401 error when getting sprints for a course the user is not assigned to."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course",
        side_effect=HTTPException(401),
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.get_sprints("course_name", "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    assert exc_info.value.status_code == 401


def test_get_sprints_empty(mocker):
    """Test a successful empty response when there are no sprints for the specified course in the database."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_find = mocker.patch("pymongo.collection.Collection.find", return_value=[])
    sprints = courses.get_sprints("course_name", "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_find.assert_called_once()
    assert not sprints


def test_get_sprints_invalid_course(mocker):
    """Test 404 error when getting sprints for a course that has no sprints."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.courses.check_course_in_db", side_effect=HTTPException(404)
    )
    mock_find = mocker.patch("pymongo.collection.Collection.find")

    with pytest.raises(HTTPException) as exc_info:
        courses.get_sprints("course_name")
    mock_check_course_in_db.assert_called_once()
    mock_find.assert_not_called()
    assert exc_info.value.status_code == 404


def test_create_sprint(mocker):
    """Test successfully creating a new sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_check_exists = mocker.patch(
        "pymongo.collection.Collection.count_documents", return_value=0
    )
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")

    courses.create_sprint("course_name", mock_data.SPRINT, "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_check_exists.assert_called_once()
    mock_update_one.assert_called_once()


def test_create_sprint_invalid_coursename(mocker):
    """Test 404 error when passing an invalid course name."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.courses.check_course_in_db", side_effect=HTTPException(404)
    )
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")

    with pytest.raises(HTTPException) as exc_info:
        courses.create_sprint("course_name", mock_data.SPRINT, "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_update_one.assert_not_called()
    assert exc_info.value.status_code == 404


def test_create_sprint_user_unassigned(mocker):
    """Test 401 error when user is not assigned to the course."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course",
        side_effect=HTTPException(401),
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.create_sprint("course_name", mock_data.SPRINT, "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")

    assert exc_info.value.status_code == 401


def test_delete_sprint(mocker):
    """Test successfully deleting a single sprint from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_delete_one = mocker.patch(
        "pymongo.collection.Collection.delete_one",
        return_value=pymongo.results.DeleteResult({"n": 1}, 1),
    )
    mock_delete_many = mocker.patch("pymongo.collection.Collection.delete_many")

    courses.delete_sprint("course_name", 1, "test_email")
    mock_check_course_in_db.assert_called_once_with("course_name", [".sprints"])
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_delete_one.assert_called_once_with({"sprint_number": 1})
    assert mock_delete_one.return_value.deleted_count == 1
    mock_delete_many.assert_called_once_with({"sprint": 1})


def test_delete_sprint_invalid_course(mocker):
    """Test 404 error when deleting a sprint from a course that does not exist."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.courses.check_course_in_db", side_effect=HTTPException(404)
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.delete_sprint("course_name", 1, "test_email")
    mock_check_course_in_db.assert_called_once_with("course_name", [".sprints"])
    assert exc_info.value.status_code == 404


def test_delete_sprint_invalid_sprint(mocker):
    """Test 404 error when deleting a sprint that does not exist."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_delete_one = mocker.patch(
        "pymongo.collection.Collection.delete_one",
        return_value=pymongo.results.DeleteResult({"n": 0}, 1),
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.delete_sprint("course_name", 1, "test_email")
    mock_check_course_in_db.assert_called_once_with("course_name", [".sprints"])
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_delete_one.assert_called_once_with({"sprint_number": 1})
    assert exc_info.value.status_code == 404
    assert mock_delete_one.return_value.deleted_count == 0


def test_delete_sprint_user_unassigned(mocker):
    """Test 401 error when deleting a sprint from a course the user is not assigned to."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course",
        side_effect=HTTPException(401),
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.delete_sprint("course_name", 1, "test_email")
    mock_check_course_in_db.assert_called_once_with("course_name", [".sprints"])
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    assert exc_info.value.status_code == 401


def test_update_course(mocker):
    """Test successfully updating a course."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")

    courses.update_course(mock_data.COURSE, "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_update_one.assert_called_once()


def test_update_course_invalid_course(mocker):
    """Test 404 error when updating a course that does not exist."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.courses.check_course_in_db", side_effect=HTTPException(404)
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.update_course(mock_data.COURSE, "test_email")
    mock_check_course_in_db.assert_called_once()
    assert exc_info.value.status_code == 404


def test_update_course_unassigned_user(mocker):
    """Test 401 error when user is not assigned to the course."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course",
        side_effect=HTTPException(401),
    )
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")

    with pytest.raises(HTTPException) as exc_info:
        courses.update_course(mock_data.COURSE, "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_update_one.assert_not_called()
    assert exc_info.value.status_code == 401


def test_update_sprint(mocker):
    """Test successfully updating a sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_count_documents = mocker.patch("pymongo.collection.Collection.count_documents")
    mock_update_one = mocker.patch(
        "pymongo.collection.Collection.update_one", return_value=1
    )

    courses.update_sprint(mock_data.SPRINT, "course_name", "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_count_documents.assert_called_once()
    mock_update_one.assert_called_once()


def test_update_sprint_invalid_course(mocker):
    """Test 404 error when updating a sprint from a course that does not exist."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.courses.check_course_in_db", side_effect=HTTPException(404)
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.update_sprint(mock_data.SPRINT, "course_name", "test_email")
    mock_check_course_in_db.assert_called_once()
    assert exc_info.value.status_code == 404


def test_update_sprint_invalid_sprint(mocker):
    """Test 404 error when updating a sprint that does not exist."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course"
    )
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents", return_value=0
    )

    with pytest.raises(HTTPException) as exc_info:
        courses.update_sprint(mock_data.SPRINT, "course_name", "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_count_documents.assert_called_once()
    assert exc_info.value.status_code == 404


def test_update_sprint_unassigned_user(mocker):
    """Test 401 error when user is not assigned to the course."""
    mock_check_course_in_db = mocker.patch("server.routes.courses.check_course_in_db")
    mock_check_user_assigned = mocker.patch(
        "server.routes.courses.check_user_assigned_to_course",
        side_effect=HTTPException(401),
    )
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")

    with pytest.raises(HTTPException) as exc_info:
        courses.update_sprint(mock_data.SPRINT, "course_name", "test_email")
    mock_check_course_in_db.assert_called_once()
    mock_check_user_assigned.assert_called_once_with("test_email", "course_name")
    mock_update_one.assert_not_called()
    assert exc_info.value.status_code == 401
