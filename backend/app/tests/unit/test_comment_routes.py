"""Unit tests for the TA comment routes."""

from datetime import datetime

import pymongo
import pytest
from bson import ObjectId
from fastapi import HTTPException

from server.routes import comments
from tests.unit import mock_data


def test_add_comment(mocker):
    """Test successfully adding a comment to the database."""
    mock_insert_one = mocker.patch("pymongo.collection.Collection.insert_one")
    datetime_mock = mocker.patch("server.routes.comments.datetime")
    # Mock current datetime.
    datetime_mock.now.return_value = datetime.fromisoformat("2021-04-20T00:00:00")
    comments.add_comment("course_name", mock_data.COMMENT_REQUEST)
    mock_insert_one.assert_called_once_with(
        {
            "message": "test_message",
            "team": "test_team",
            "sprint_number": 1,
            "created_at": "2021-04-20T00:00:00",
            "last_modified_at": "2021-04-20T00:00:00",
        }
    )


def test_get_comments(mocker):
    """Test successfully getting all comments for a team from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find", return_value=[mock_data.COMMENT_JSON]
    )
    team_comments = comments.get_comments("course_name", 0, "team_name")
    mock_check_course_in_db.assert_called_once()
    mock_find.assert_called_once_with({"team": "team_name"})
    assert team_comments == [mock_data.COMMENT]


def test_get_sprint_comments(mocker):
    """Test successfully getting comments for a team for a sprint from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.SPRINT_DATES,
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find", return_value=[mock_data.COMMENT_JSON]
    )
    team_comments = comments.get_comments("course_name", 1, "team_name")
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once()
    mock_find.assert_called_once_with(
        {"$and": [{"sprint_number": 1}, {"team": "team_name"}]}
    )
    assert team_comments == [mock_data.COMMENT]


def test_get_comments_empty(mocker):
    """Test successful handling of an empty response if the team has no comments."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    mock_find = mocker.patch("pymongo.collection.Collection.find", return_value=[])
    team_comments = comments.get_comments("course_name", 0, "team_name")
    mock_check_course_in_db.assert_called_once()
    mock_find.assert_called_once_with({"team": "team_name"})
    assert not team_comments


def test_get_comments_invalid_sprint(mocker):
    """Test for 404 error being raised when a sprint that is not in the sprints collection is provided."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    mocker.patch("pymongo.collection.Collection.find_one", return_value=None)
    with pytest.raises(HTTPException) as exc_info:
        comments.get_comments("course_name", 2, "team_name")
    mock_check_course_in_db.assert_called_once()
    assert exc_info.value.status_code == 404


def test_get_comments_invalid_course(mocker):
    """Test for 404 error being raised when a course that does not have a corresponding comments subcollection is provided."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.comments.check_course_in_db", side_effect=HTTPException(404)
    )
    mocker.patch(
        "pymongo.collection.Collection.find", return_value=[mock_data.COMMENT_JSON]
    )
    with pytest.raises(HTTPException) as exc_info:
        comments.get_comments("bad_course", 1, "team_name")
    mock_check_course_in_db.assert_called_once()
    assert exc_info.value.status_code == 404


def test_edit_comment(mocker):
    """Test successfully editing a comment in the database."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")
    datetime_mock = mocker.patch("server.routes.comments.datetime")
    # Mock current datetime.
    datetime_mock.now.return_value = datetime.fromisoformat("2021-04-22T00:00:00")
    comments.edit_comment(
        "course_name", mock_data.COMMENT_ID, mock_data.UPDATE_COMMENT_JSON
    )
    mock_check_course_in_db.assert_called_once()
    mock_update_one.assert_called_once_with(
        {"_id": ObjectId(mock_data.COMMENT_ID)},
        {
            "$set": {
                "message": "test_message",
                "team": "test_team",
                "sprint_number": 1,
                "last_modified_at": "2021-04-22T00:00:00",
            }
        },
    )


def test_edit_comment_one_field(mocker):
    """Test successfully editing one field of a comment in the database."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    mock_update_one = mocker.patch("pymongo.collection.Collection.update_one")
    datetime_mock = mocker.patch("server.routes.comments.datetime")
    # Mock current datetime.
    datetime_mock.now.return_value = datetime.fromisoformat("2021-04-22T00:00:00")
    comments.edit_comment(
        "course_name", mock_data.COMMENT_ID, {"message": "test message"}
    )
    mock_check_course_in_db.assert_called_once()
    mock_update_one.assert_called_once_with(
        {"_id": ObjectId(mock_data.COMMENT_ID)},
        {
            "$set": {
                "message": "test message",
                "last_modified_at": "2021-04-22T00:00:00",
            }
        },
    )


def test_edit_comment_invalid_course(mocker):
    """Test for 404 error being raised when a course that does not have a corresponding comments subcollection is provided."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.comments.check_course_in_db", side_effect=HTTPException(404)
    )
    with pytest.raises(HTTPException) as exc_info:
        comments.edit_comment(
            "bad_course", mock_data.COMMENT_ID, mock_data.UPDATE_COMMENT_JSON
        )
    mock_check_course_in_db.assert_called_once()
    assert exc_info.value.status_code == 404


def test_edit_comment_invalid_id(mocker):
    """Test for 400 error being raised when an invalid format for the ID is provided."""
    with pytest.raises(HTTPException) as exc_info:
        comments.edit_comment("course_name", "bad_id", mock_data.UPDATE_COMMENT_JSON)
    assert exc_info.value.status_code == 400


def test_edit_comment_nonexistent_id(mocker):
    """Test for 404 error being raised when a comment that does not exist is provided."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    # Set the n value of the raw_result of the update_one call to 0 to simulate a nonexistent comment.
    mock_update_one = mocker.patch(
        "pymongo.collection.Collection.update_one",
        return_value=pymongo.results.UpdateResult({"n": 0}, 1),
    )
    datetime_mock = mocker.patch("server.routes.comments.datetime")
    # Mock current datetime.
    datetime_mock.now.return_value = datetime.fromisoformat("2021-04-22T00:00:00")
    with pytest.raises(HTTPException) as exc_info:
        comments.edit_comment(
            "course_name", mock_data.COMMENT_ID, mock_data.UPDATE_COMMENT_JSON
        )
    mock_check_course_in_db.assert_called_once()
    mock_update_one.assert_called_once_with(
        {"_id": ObjectId(mock_data.COMMENT_ID)},
        {
            "$set": {
                "message": "test_message",
                "team": "test_team",
                "sprint_number": 1,
                "last_modified_at": "2021-04-22T00:00:00",
            }
        },
    )
    assert exc_info.value.status_code == 404


def test_delete_comment(mocker):
    """Test successfully deleting a comment from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    # Set the n value of the raw_result of the delete_one call to 1 to simulate a successful deletion.
    mock_delete_one = mocker.patch(
        "pymongo.collection.Collection.delete_one",
        return_value=pymongo.results.DeleteResult({"n": 1}, 1),
    )
    comments.delete_comment("course_name", mock_data.COMMENT_ID)
    mock_check_course_in_db.assert_called_once()
    mock_delete_one.assert_called_once_with({"_id": ObjectId(mock_data.COMMENT_ID)})
    assert mock_delete_one.return_value.deleted_count == 1


def test_delete_comment_invalid_course(mocker):
    """Test for 404 error being raised when a course that does not have a corresponding comments subcollection is provided."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.comments.check_course_in_db", side_effect=HTTPException(404)
    )
    with pytest.raises(HTTPException) as exc_info:
        comments.delete_comment("bad_course", mock_data.COMMENT_ID)
    mock_check_course_in_db.assert_called_once()
    assert exc_info.value.status_code == 404


def test_delete_comment_invalid_id(mocker):
    """Test for 400 error being raised when an invalid format for the ID is provided."""
    with pytest.raises(HTTPException) as exc_info:
        comments.delete_comment("course_name", "bad_id")
    assert exc_info.value.status_code == 400


def test_delete_comment_nonexistent_id(mocker):
    """Test for 404 error being raised when a comment that does not exist is provided."""
    mock_check_course_in_db = mocker.patch("server.routes.comments.check_course_in_db")
    # Set the n value of the raw_result of the delete_one call to 0 to simulate a nonexistent comment.
    mock_delete_one = mocker.patch(
        "pymongo.collection.Collection.delete_one",
        return_value=pymongo.results.DeleteResult({"n": 0}, 1),
    )
    with pytest.raises(HTTPException) as exc_info:
        comments.delete_comment("course_name", mock_data.COMMENT_ID)
    mock_check_course_in_db.assert_called_once()
    mock_delete_one.assert_called_once_with({"_id": ObjectId(mock_data.COMMENT_ID)})
    assert exc_info.value.status_code == 404
    assert mock_delete_one.return_value.deleted_count == 0
