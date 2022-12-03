"""Test FastAPI endpoints for GitHub-related data."""
from tests.integration.config import test_settings


def test_get_student_commits(client, token):
    """Test getting the number of commits for a student."""
    res = client.get(
        "/student/course1/1/octocat/commits",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json() == {"number_of_commits": 1, "username": "octocat"}


def test_get_student_sprint_commits(client, token):
    """Test getting the number of commits for a student in a single sprint."""
    res = client.get(
        "/student/course1/0/octocat/commits",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json() == {"number_of_commits": 1, "username": "octocat"}


def test_get_student_commits_invalid_course(client, token):
    """Test getting the number of commits for a student in a non-existent course."""
    res = client.get(
        "/student/course42/1/octocat/commits",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course42 does not exist"}


def test_get_student_commits_invalid_sprint(client, token):
    """Test getting the number of commits for a student in a non-existent sprint."""
    res = client.get(
        "/student/course1/42/octocat/commits",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Sprint 42 does not exist"}


def test_get_student_commits_unauthorized(client):
    """Test getting the number of commits for a student without authorization."""
    res = client.get(
        "/student/course1/1/octocat/commits",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_get_team_commits(client, token):
    """Test getting the number of commits for all team members."""
    res = client.get(
        "/team/course1/1/commits/cats-in-space",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json() == {
        "student_commits": [{"username": "octocat", "number_of_commits": 1}],
        "last_fetched_at": "2020-01-09T00:00:00Z",
    }


def test_get_team_sprint_commits(client, token):
    """Test getting the number of commits for all team members in a single sprint."""
    res = client.get(
        "/team/course1/0/commits/cats-in-space",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json() == {
        "student_commits": [{"username": "octocat", "number_of_commits": 1}],
        "last_fetched_at": "2020-01-09T00:00:00Z",
    }


def test_get_team_commits_empty(client, token):
    """Test getting the number of commits for a non-existent team."""
    res = client.get(
        "/team/course1/1/commits/empty-team",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json() == {"student_commits": [], "last_fetched_at": None}


def test_get_team_commits_invalid_course(client, token):
    """Test getting the number of commits for a team in a non-existent course."""
    res = client.get(
        "/team/course42/1/commits/cats-in-space",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course42 does not exist"}


def test_get_team_commits_invalid_sprint(client, token):
    """Test getting the number of commits for a team for a non-existent sprint."""
    res = client.get(
        "/team/course1/42/commits/cats-in-space",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Sprint 42 does not exist"}


def test_get_team_commits_unauthorized(client):
    """Test getting the number of commits for a team without authorization."""
    res = client.get(
        "/team/course1/1/commits/cats-in-space",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_get_teams_commits(client, token):
    """Test getting the number of commits for all teams."""
    res = client.get(
        "/class/course1/1/commits", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == [{"team_name": "cats-in-space", "number_of_commits": 1}]


def test_get_teams_sprint_commits(client, token):
    """Test getting the number of commits for all teams in a single sprint."""
    res = client.get(
        "/class/course1/0/commits", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == [{"team_name": "cats-in-space", "number_of_commits": 1}]


def test_get_teams_commits_invalid_course(client, token):
    """Test getting the number of commits for all teams in a non-existent course."""
    res = client.get(
        "/class/course42/1/commits", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course42 does not exist"}


def test_get_teams_commits_invalid_sprint(client, token):
    """Test getting the number of commits for all teams in a non-existent sprint."""
    res = client.get(
        "/class/course1/42/commits", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Sprint 42 does not exist"}


def test_get_teams_commits_unauthorized(client):
    """Test getting the number of commits for all teams without authorization."""
    res = client.get(
        "/class/course1/1/commits", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_store_commits(client, token):
    """Test fetching commits from GitHub and storing them in the database for a course."""
    res = client.post(
        "/github",
        json={
            "owner": test_settings.GITHUB_OWNER,
            "repo": test_settings.GITHUB_REPO,
            "course_name": "course1",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204


def test_store_commits_invalid_course(client, token):
    """Test fetching commits from GitHub and storing them in the database for a non-existent course."""
    res = client.post(
        "/github",
        json={
            "owner": test_settings.GITHUB_OWNER,
            "repo": test_settings.GITHUB_REPO,
            "course_name": "course42",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course42 does not exist"}


def test_store_commits_invalid_repo(client, token):
    """Test fetching commits from GitHub for a non-existent repository."""
    res = client.post(
        "/github",
        json={
            "owner": test_settings.GITHUB_OWNER,
            "repo": "invalid-repo",
            "course_name": "course1",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404


def test_store_commits_invalid_owner(client, token):
    """Test fetching commits from GitHub for a non-existent repository owner."""
    res = client.post(
        "/github",
        json={
            "owner": "invalid-owner",
            "repo": test_settings.GITHUB_REPO,
            "course_name": "course1",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404


def test_store_commits_unauthorized(client):
    """Test fetching commits from GitHub without authorization."""
    res = client.post(
        "/github",
        json={
            "owner": test_settings.GITHUB_OWNER,
            "repo": test_settings.GITHUB_REPO,
            "course_name": "course1",
        },
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}
