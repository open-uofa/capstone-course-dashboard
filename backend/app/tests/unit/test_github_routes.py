"""Test API functions for interacting with GitHub."""
import pytest
from fastapi import HTTPException

from server.routes import github
from tests.unit import mock_data


def test_get_student_github_commits(mocker):
    """Test that the correct data is returned for a student's GitHub commits."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents",
        return_value=42,
    )
    student_commit = github.get_student_github_commits("test_course", 0, "test_student")
    mock_check_course_in_db.assert_called_once()
    mock_count_documents.assert_called_once()
    assert student_commit == mock_data.STUDENT_COMMIT


def test_get_student_sprint_github_commits(mocker):
    """Test that the correct data is returned for a student's GitHub commits for the specified sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.SPRINT_DATES,
    )
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents",
        return_value=42,
    )
    student_commit = github.get_student_github_commits("test_course", 1, "test_student")
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once()
    mock_count_documents.assert_called_once()
    assert student_commit == mock_data.STUDENT_COMMIT


def test_get_student_github_commits_invalid_sprint(mocker):
    """Test 404 error when trying to get a student's commits for a non-existent sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=None,
    )
    with pytest.raises(HTTPException) as exc_info:
        github.get_student_github_commits("test_course", 1, "test_student")
        mock_check_course_in_db.assert_called_once()
        mock_find_one.assert_called_once()
        assert exc_info.value.status_code == 404


def test_get_student_github_commits_invalid_course(mocker):
    """Test 404 error when trying to get a student's commits for a non-existent course."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.github.check_course_in_db",
        side_effect=HTTPException(404),
    )
    with pytest.raises(HTTPException) as exc_info:
        github.get_student_github_commits("test_course", 1, "test_student")
        mock_check_course_in_db.assert_called_once()
        assert exc_info.value.status_code == 404


def test_get_team_github_commits(mocker):
    """Test that the correct data is returned for a team's GitHub commits."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_distinct = mocker.patch(
        "pymongo.collection.Collection.distinct",
        return_value=["test_student"],
    )
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents",
        return_value=42,
    )
    mock_aggregate = mocker.patch(
        "pymongo.collection.Collection.aggregate",
        return_value=iter(mock_data.GITHUB_COMMITS),
    )
    team_commits = github.get_team_github_commits("test_course", "test_repo", 0)
    mock_check_course_in_db.assert_called_once()
    assert mock_distinct.call_count == 2
    mock_count_documents.assert_called_once()
    mock_aggregate.assert_called_once()
    assert team_commits == mock_data.TEAM_COMMITS


def test_get_team_sprint_github_commits(mocker):
    """Test that the correct data is returned for a team's GitHub commits for the specified sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.SPRINT_DATES,
    )
    mock_distinct = mocker.patch(
        "pymongo.collection.Collection.distinct",
        return_value=["test_student"],
    )
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents",
        return_value=42,
    )
    mock_aggregate = mocker.patch(
        "pymongo.collection.Collection.aggregate",
        return_value=iter(mock_data.GITHUB_COMMITS),
    )
    team_commits = github.get_team_github_commits("test_course", "test_repo", 1)
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once()
    assert mock_distinct.call_count == 2
    mock_count_documents.assert_called_once()
    mock_aggregate.assert_called_once()
    assert team_commits == mock_data.TEAM_COMMITS


def test_get_team_github_commits_empty(mocker):
    """Test that zero counts are returned when a team has no commits."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.SPRINT_DATES,
    )
    mock_distinct = mocker.patch(
        "pymongo.collection.Collection.distinct",
        return_value=["test_student"],
    )
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents", return_value=0
    )
    mock_aggregate = mocker.patch(
        "pymongo.collection.Collection.aggregate",
        return_value=iter([]),
    )
    team_commits = github.get_team_github_commits("test_course", "test_repo", 1)
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once()
    assert mock_distinct.call_count == 2
    mock_count_documents.assert_called_once()
    mock_aggregate.assert_called_once()
    assert team_commits == mock_data.TEAM_COMMITS_EMPTY


def test_get_team_github_commits_invalid_sprint(mocker):
    """Test 404 error when trying to get a team's commits for a non-existent sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_distinct = mocker.patch(
        "pymongo.collection.Collection.distinct",
        return_value=["test_student"],
    )
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=None,
    )
    with pytest.raises(HTTPException) as exc_info:
        github.get_team_github_commits("test_course", "test_repo", 1)
        mock_check_course_in_db.assert_called_once()
        mock_distinct.assert_called_once()
        mock_find_one.assert_called_once()
        assert exc_info.value.status_code == 404


def test_get_team_github_commits_invalid_course(mocker):
    """Test 404 error when trying to get a team's commits for a non-existent course."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.github.check_course_in_db",
        side_effect=HTTPException(404),
    )
    with pytest.raises(HTTPException) as exc_info:
        github.get_team_github_commits("test_course", "test_repo", 1)
        mock_check_course_in_db.assert_called_once()
        assert exc_info.value.status_code == 404


def test_get_teams_github_commits(mocker):
    """Test that the correct data is returned for all teams' GitHub commits."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_distinct = mocker.patch(
        "pymongo.collection.Collection.distinct",
        return_value=["test_team"],
    )
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents",
        return_value=42,
    )
    team_commits = github.get_teams_github_commits("test_course", 0)
    mock_check_course_in_db.assert_called_once()
    assert mock_distinct.call_count == 2
    mock_count_documents.assert_called_once()
    assert team_commits == [mock_data.TEAM_COMMIT]


def test_get_teams_sprint_github_commits(mocker):
    """Test that the correct data is returned for all teams' GitHub commits for the specified sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.SPRINT_DATES,
    )
    mock_distinct = mocker.patch(
        "pymongo.collection.Collection.distinct",
        return_value=["test_team"],
    )
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents",
        return_value=42,
    )
    team_commits = github.get_teams_github_commits("test_course", 1)
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once()
    assert mock_distinct.call_count == 2
    mock_count_documents.assert_called_once()
    assert team_commits == [mock_data.TEAM_COMMIT]


def test_get_teams_github_commits_empty(mocker):
    """Test that zero counts are returned when no teams have commits."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.SPRINT_DATES,
    )
    mock_distinct = mocker.patch(
        "pymongo.collection.Collection.distinct",
        return_value=["test_team"],
    )
    mock_count_documents = mocker.patch(
        "pymongo.collection.Collection.count_documents",
        return_value=0,
    )
    team_commits = github.get_teams_github_commits("test_course", 1)
    mock_check_course_in_db.assert_called_once()
    mock_find_one.assert_called_once()
    assert mock_distinct.call_count == 2
    mock_count_documents.assert_called_once()
    assert team_commits == [mock_data.TEAM_COMMIT_EMPTY]


def test_get_teams_github_commits_invalid_sprint(mocker):
    """Test 404 error when trying to get all teams' commits for a non-existent sprint."""
    mock_check_course_in_db = mocker.patch("server.routes.github.check_course_in_db")
    mock_distinct = mocker.patch(
        "pymongo.collection.Collection.distinct",
        return_value=["test_student"],
    )
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=None,
    )
    with pytest.raises(HTTPException) as exc_info:
        github.get_teams_github_commits("test_course", 1)
        mock_check_course_in_db.assert_called_once()
        mock_distinct.assert_called_once()
        mock_find_one.assert_called_once()
        assert exc_info.value.status_code == 404


def test_get_teams_github_commits_invalid_course(mocker):
    """Test 404 error when trying to get all teams' commits for a non-existent course."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.github.check_course_in_db",
        side_effect=HTTPException(404),
    )
    with pytest.raises(HTTPException) as exc_info:
        github.get_teams_github_commits("test_course", 1)
        mock_check_course_in_db.assert_called_once()
        assert exc_info.value.status_code == 404


def test_fetch_and_store_github_commits(mocker):
    """Test that GitHub commits can be fetched from GitHub and stored in the database successfully."""
    mock_get_new_commits = mocker.patch(
        f"{mock_data.GITHUB_UTILS_PATH}.get_new_commits",
        return_value=mock_data.GITHUB_COMMITS,
    )
    mock_store_commits = mocker.patch(f"{mock_data.GITHUB_UTILS_PATH}.store_commits")
    github.fetch_and_store_github_commits(mock_data.GITHUB_REQUEST)
    mock_get_new_commits.assert_called_once_with(
        "test_owner", "test_repo", "test_course"
    )
    mock_store_commits.assert_called_once_with(
        mock_data.GITHUB_COMMITS, "test_repo", "test_course"
    )
