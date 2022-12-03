"""Test FastAPI endpoints for meeting-minutes-related data."""
from tests.integration.config import test_settings


def test_get_meeting_minutes(client, token):
    """Test getting all meeting minutes."""
    res = client.get(
        "/minutes/course1/team1/0", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == [
        {
            "title": "January 8, 2020",
            "body": "Agenda for today's meeting: ...",
        },
        {
            "title": "February 11, 2020",
            "body": "Agenda for today's meeting: ...",
        },
    ]


def test_get_meeting_minutes_sprint(client, token):
    """Test getting meeting minutes for a sprint."""
    res = client.get(
        "/minutes/course1/team1/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == [
        {"title": "January 8, 2020", "body": "Agenda for today's meeting: ..."}
    ]


def test_get_meeting_minutes_empty(client, token):
    """Test getting meeting minutes for a team with no meeting minutes."""
    res = client.get(
        "/minutes/course1/team2/0", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == []


def test_get_meeting_minutes_invalid_course(client, token):
    """Test getting meeting minutes for a non-existent course"""
    res = client.get(
        "/minutes/course2/team1/0", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course2 does not exist"}


def test_get_meeting_minutes_invalid_sprint(client, token):
    """Test getting meeting minutes for a non-existent sprint."""
    res = client.get(
        "/minutes/course1/team1/562", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Sprint 562 does not exist in course course1"}


def test_get_meeting_minutes_unauthorized(client):
    """Test getting meeting minutes without authorization."""
    res = client.get(
        "/minutes/course1/team1/0", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_fetch_and_store_meeting_minutes(client, token):
    """Test fetching and storing meeting minutes."""
    res = client.post(
        f"/minutes/course1/{test_settings.GITHUB_OWNER}/{test_settings.GITHUB_REPO}",
        json={
            "title": "September 18, 2021",
            "body": "Agenda for today's meeting: ...",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204


def test_fetch_and_store_meeting_minutes_invalid_course(client, token):
    """Test fetching and storing meeting minutes for a non-existent course."""
    res = client.post(
        f"/minutes/course2/{test_settings.GITHUB_OWNER}/{test_settings.GITHUB_REPO}",
        json={
            "title": "September 18, 2021",
            "body": "Agenda for today's meeting: ...",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course2 does not exist"}


def test_fetch_and_store_meeting_minutes_invalid_owner(client, token):
    """Test fetching and storing meeting minutes for a non-existent team."""
    res = client.post(
        f"/minutes/course1/owner2/{test_settings.GITHUB_REPO}",
        json={
            "title": "September 18, 2021",
            "body": "Agenda for today's meeting: ...",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404


def test_fetch_and_store_meeting_minutes_invalid_team(client, token):
    """Test fetching and storing meeting minutes for a non-existent team."""
    res = client.post(
        f"/minutes/course1/{test_settings.GITHUB_OWNER}/team2",
        json={
            "title": "September 18, 2021",
            "body": "Agenda for today's meeting: ...",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404


def test_fetch_and_store_meeting_minutes_unauthorized(client):
    """Test fetching and storing meeting minutes without authorization."""
    res = client.post(
        f"/minutes/course1/{test_settings.GITHUB_OWNER}/{test_settings.GITHUB_REPO}",
        json={
            "title": "September 18, 2021",
            "body": "Agenda for today's meeting: ...",
        },
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}
