"""Unit tests for student util functions"""
import os

from server.util import students
from tests.unit import mock_data


def test_parse_roster_data(mocker, datadir):
    """Test successfully parsing student roster data from a CSV file."""
    with open(os.path.join(datadir, "test_roster.csv"), "r", encoding="utf-8") as file:
        return_val = students.parse_roster_data(file, "course1")
    assert return_val[0].dict() == mock_data.STUDENT_ROSTER_RETURN[0].dict()


def test_parse_roster_data_empty_fields(mocker, datadir):
    """Test parsing student roster data from a CSV file with empty survey fields."""
    with open(
        os.path.join(datadir, "test_roster_empty_survey.csv"), "r", encoding="utf-8"
    ) as file:
        return_val = students.parse_roster_data(file, "course1")
    assert return_val[0].dict() == mock_data.STUDENT_ROSTER_EMPTY_FIELDS.dict()


def test_parse_sprint_data(mocker, datadir):
    """Test successfully parsing student sprint data from a CSV file."""
    with open(os.path.join(datadir, "test_sprint1.csv"), "r", encoding="utf-8") as file:
        return_val = students.parse_sprint_data(file, 1)
    assert return_val[0].dict() == mock_data.STUDENT_SPRINT_RETURN[0].dict()


def test_parse_sprint_data_reversed_names(mocker, datadir):
    """
    Test successfully parsing student sprint data from a CSV file with
    team members formatted as 'name - email'.
    """
    with open(
        os.path.join(datadir, "test_sprint1_reversed_names.csv"), "r", encoding="utf-8"
    ) as file:
        return_val = students.parse_sprint_data(file, 1)
    assert return_val[0].dict() == mock_data.STUDENT_SPRINT_RETURN[0].dict()


def test_parse_sprint_data_unsubmitted_peer_review(mocker, datadir):
    """
    Test successfully parsing student sprint data from a CSV file where a student
    did not submit a peer review, but their team members did.
    """
    with open(
        os.path.join(datadir, "test_sprint1_unsubmitted_peer_review.csv"),
        "r",
        encoding="utf-8",
    ) as file:
        return_val = students.parse_sprint_data(file, 1)
    assert return_val[1].dict() == mock_data.STUDENT_SPRINT_RETURN_UNSUBMITTED[1].dict()
