"""Unit tests for the team meeting minutes."""

import pytest
from fastapi import HTTPException

from server.routes import minutes
from tests.unit import mock_data


def test_get_meeting_minutes(mocker):
    """Test successfully getting all meeting minutes for a team from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.minutes.check_course_in_db")
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find",
        return_value=[mock_data.MEETING_MINUTES_JSON],
    )
    meeting_minutes = minutes.get_meeting_minutes("course_name", "team_name", 0)
    mock_check_course_in_db.assert_called_once()
    mock_find.assert_called_once_with({"team": "team_name"})
    assert meeting_minutes == [mock_data.MEETING_MINUTES]


def test_get_meeting_minutes_sprint(mocker):
    """Test successfully getting meeting minutes for a team for a sprint from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.minutes.check_course_in_db")
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find",
        return_value=[mock_data.MEETING_MINUTES_JSON],
    )
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.SPRINT_DATES,
    )
    meeting_minutes = minutes.get_meeting_minutes("course_name", "team_name", 1)
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once_with({"sprint_number": 1})
    mock_find.assert_called_once_with(
        {
            "$and": [
                {"timestamp": {"$lt": "2020-01-02T00:00:00Z"}},
                {"timestamp": {"$gt": "2020-01-01T00:00:00Z"}},
                {"team": "team_name"},
            ]
        }
    )
    assert meeting_minutes == [mock_data.MEETING_MINUTES]


def test_get_meeting_minutes_no_meeting_minutes(mocker):
    """Test getting meeting minutes for a team from the database when there are none."""
    mock_check_course_in_db = mocker.patch("server.routes.minutes.check_course_in_db")
    mock_find = mocker.patch("pymongo.collection.Collection.find", return_value=[])
    meeting_minutes = minutes.get_meeting_minutes("course_name", "team_name", 0)
    mock_check_course_in_db.assert_called_once()
    mock_find.assert_called_once_with({"team": "team_name"})
    assert not meeting_minutes


def test_get_meeting_minutes_course_not_found(mocker):
    """Test getting meeting minutes for a team from the database when the course is not found."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.minutes.check_course_in_db", side_effect=HTTPException(404)
    )
    with pytest.raises(HTTPException) as exc:
        minutes.get_meeting_minutes("course_name", "team_name", 0)
    mock_check_course_in_db.assert_called_once()
    assert exc.value.status_code == 404


def test_get_meeting_minutes_invalid_sprint(mocker):
    """Test getting meeting minutes for a team from the database when the sprint is invalid."""
    mock_check_course_in_db = mocker.patch("server.routes.minutes.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one", return_value=None
    )
    with pytest.raises(HTTPException) as exc:
        minutes.get_meeting_minutes("course_name", "team_name", 562)
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once_with({"sprint_number": 562})
    assert exc.value.status_code == 404


def test_fetch_and_store_meeting_minutes(mocker, response_mock):
    """Test successfully fetching and storing meeting minutes for a team."""
    mock_get = mocker.patch(
        "requests.get",
        return_value=response_mock({}, content=mock_data.MEETING_MINUTES_TEXT),
    )
    mock_check_course_in_db = mocker.patch("server.routes.minutes.check_course_in_db")
    mock_delete_many = mocker.patch("pymongo.collection.Collection.delete_many")
    mock_insert_many = mocker.patch("pymongo.collection.Collection.insert_many")

    minutes.fetch_and_store_meeting_minutes("course_name", "owner_name", "team_name")
    mock_get.assert_called_once_with(
        "https://owner_name.github.io/team_name/meeting-minutes/", timeout=60
    )
    mock_check_course_in_db.assert_called_once()
    mock_delete_many.assert_called_once_with({"team": "team_name"})
    mock_insert_many.assert_called_once_with(
        [
            {
                "title": "October 24, 1988",
                "body": "Meeting minutes text 1",
                "team": "team_name",
                "timestamp": "1988-10-24T00:00:00",
            },
            {
                "title": "October 25, 1988",
                "body": "Meeting minutes text 2",
                "team": "team_name",
                "timestamp": "1988-10-25T00:00:00",
            },
        ]
    )


def test_fetch_and_store_meeting_minutes_invalid_course(mocker, response_mock):
    """Test fetching and storing meeting minutes for a team when the course is invalid."""
    mock_get = mocker.patch(
        "requests.get",
        return_value=response_mock({}, content=mock_data.MEETING_MINUTES_TEXT),
    )
    mock_check_course_in_db = mocker.patch(
        "server.routes.minutes.check_course_in_db", side_effect=HTTPException(404)
    )

    with pytest.raises(HTTPException) as exc:
        minutes.fetch_and_store_meeting_minutes(
            "course_name", "owner_name", "team_name"
        )
    mock_get.assert_called_once_with(
        "https://owner_name.github.io/team_name/meeting-minutes/", timeout=60
    )
    mock_check_course_in_db.assert_called_once()
    assert exc.value.status_code == 404


def test_fetch_and_store_meeting_minutes_invalid_url(mocker, response_mock):
    """Test fetching and storing meeting minutes for a team when the team or owner is invalid."""
    mock_get = mocker.patch(
        "requests.get", return_value=response_mock({}, status_code=404)
    )

    with pytest.raises(HTTPException) as exc:
        minutes.fetch_and_store_meeting_minutes(
            "course_name", "owner_name", "team_name"
        )
    mock_get.assert_called_once_with(
        "https://owner_name.github.io/team_name/meeting-minutes/", timeout=60
    )
    assert exc.value.status_code == 404


def test_fetch_and_store_meeting_minutes_parsing_error(mocker, response_mock):
    """Test fetching and storing meeting minutes for a team when there is a parsing error."""
    mock_get = mocker.patch(
        "requests.get",
        return_value=response_mock({}, content=b"<html />"),
    )

    with pytest.raises(HTTPException) as exc:
        minutes.fetch_and_store_meeting_minutes(
            "course_name", "owner_name", "team_name"
        )
    mock_get.assert_called_once_with(
        "https://owner_name.github.io/team_name/meeting-minutes/", timeout=60
    )
    assert exc.value.status_code == 400
    assert exc.value.detail.startswith(
        "Error parsing meeting minutes from MKDocs page:"
    )


def test_fetch_and_store_meeting_minutes_date_format_error(mocker, response_mock):
    """Test fetching and storing meeting minutes for a team when the expected date cannot be parsed."""
    mock_get = mocker.patch(
        "requests.get",
        return_value=response_mock(
            {}, content=mock_data.MEETING_MINUTES_INVALID_DATE_TEXT
        ),
    )
    mock_check_course_in_db = mocker.patch("server.routes.minutes.check_course_in_db")

    with pytest.raises(HTTPException) as exc:
        minutes.fetch_and_store_meeting_minutes(
            "course_name", "owner_name", "team_name"
        )
    mock_get.assert_called_once_with(
        "https://owner_name.github.io/team_name/meeting-minutes/", timeout=60
    )
    mock_check_course_in_db.assert_called_once()
    assert exc.value.status_code == 400
    assert exc.value.detail == "Unable to parse date October 24th/25th, 1988, 2pm/11am"
