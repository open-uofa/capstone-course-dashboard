"""Test common utilities."""

import pytest
from fastapi import HTTPException

from server.util import common


def test_check_course_in_db(mocker):
    """Test successfully checking if a course has the specified subcollection."""
    validate_collection_mock = mocker.patch(
        "pymongo.database.Database.validate_collection"
    )
    common.check_course_in_db("test", [".test"])
    validate_collection_mock.assert_called_once()


def test_check_course_in_db_not_found(mocker):
    """Test failing to find a course in the database."""
    mocker.patch(
        "pymongo.database.Database.validate_collection", side_effect=Exception()
    )
    with pytest.raises(HTTPException) as exc:
        common.check_course_in_db("test", [".test"])
        assert exc.status_code == 404
        assert exc.detail == "Course test does not exist"


def test_get_sprint_list(mocker):
    """Test getting a list of sprints for a course."""
    mocker.patch("pymongo.database.Database.validate_collection")
    find_mock = mocker.patch(
        "pymongo.collection.Collection.find",
        return_value=[{"sprint_number": 1}, {"sprint_number": 2}],
    )
    sprints = common.get_sprint_list("test")
    assert sprints == [1, 2]
    find_mock.assert_called_once()


def test_check_user_assigned_to_course(mocker):
    """Test successfully checking if a user is assigned to a course."""
    find_mock = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value={"assigned_courses": ["test"]},
    )
    common.check_user_assigned_to_course("admin@gmail.com", "test")
    find_mock.assert_called_once()


def test_check_user_assigned_to_course_not_assigned(mocker):
    """Test failing to find a user assigned to a course."""
    find_mock = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value={"assigned_courses": ["test"]},
    )
    with pytest.raises(HTTPException) as exc:
        common.check_user_assigned_to_course("admin@gmail.com", "course_name")
        assert exc.status_code == 401
        assert (
            exc.detail == "User admin@gmail.com is not authorized to access course_name"
        )
    find_mock.assert_called_once()
