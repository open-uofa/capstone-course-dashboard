"""Test FastAPI endpoints for student-related data."""
import os

from tests.integration.config import collections


def test_get_students(client, token):
    """Test getting details for all students."""
    res = client.get(
        "/students/course1/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json() == {
        "students": collections["course1.students"],
        "sprint_data": collections["course1.students.sprints"],
    }


def test_get_students_unauthorized(client):
    """Test getting details for all students without authorization."""
    res = client.get(
        "/students/course1/1",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_get_student(client, token):
    """Test getting details for a single student."""
    res = client.get(
        "/students/course1/1/octocat@github.ca",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json() == {
        "students": collections["course1.students"],
        "sprint_data": collections["course1.students.sprints"],
    }


def test_get_student_unauthorized(client):
    """Test getting details for a single student without authorization."""
    res = client.get(
        "/students/course1/1/octocat@github.ca",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_post_roster(client, datadir, token):
    """Test uploading roster data from a CSV file."""
    with open(os.path.join(datadir, "test_roster.csv"), "r", encoding="utf-8") as file:
        res = client.post(
            "/students/course1/0",
            files={"file": ("test_roster.csv", file, "application/vnd.ms-excel")},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert res.status_code == 204


def test_post_roster_invalid_sprint(client, token):
    """Test uploading roster data for a non-existent sprint."""
    res = client.post(
        "/students/course1/-1",
        files={"file": "test"},
        headers={
            "Content-Type": "multipart/form-data",
            "Authorization": f"Bearer {token}",
        },
    )
    assert res.status_code == 400


def test_post_sprint(client, datadir, token):
    """Test uploading sprint data from a CSV file."""
    with open(os.path.join(datadir, "test_sprint1.csv"), "r", encoding="utf-8") as file:
        res = client.post(
            "/students/course1/1",
            files={"file": ("test_sprint1.csv", file, "application/vnd.ms-excel")},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert res.status_code == 204


def test_post_roster_unauthorized(client, datadir):
    """Test uploading roster/sprint data without authorization."""
    with open(os.path.join(datadir, "test_roster.csv"), "r", encoding="utf-8") as file:
        res = client.post(
            "/students/course1/0",
            files={"file": ("test_roster.csv", file, "application/vnd.ms-excel")},
            headers={"Authorization": "Bearer invalid_token"},
        )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}
