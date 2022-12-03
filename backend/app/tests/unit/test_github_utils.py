"""Test helper functions for interacting with the GitHub API."""
from datetime import datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException
from pymongo import UpdateOne
from requests import Request

from server.config import settings
from server.util import github
from tests.unit import mock_data


class TestGitHubTokenAuth:
    def test__call__(self):
        """Test that the GitHubTokenAuth class returns a request with the correct headers."""
        # Use datetime in the future to test a valid token.
        settings.github_expiration = (datetime.now() + timedelta(days=1)).isoformat()
        request = Request()
        request = github.GitHubTokenAuth()(request)
        assert request.headers["Authorization"] == f"Bearer {mock_data.GITHUB_TOKEN}"
        assert request.headers["Accept"] == "application/vnd.github+json"
        # Reset expiration back to original mock value.
        settings.github_expiration = mock_data.GITHUB_EXPIRATION

    def test__call__expired(self, mocker):
        """Test that the GitHubTokenAuth class generates a new token if the token is expired."""
        mocker.patch(
            f"{mock_data.GITHUB_UTILS_PATH}.get_access_token",
            return_value=(mock_data.GITHUB_TOKEN, mock_data.GITHUB_EXPIRATION),
        )
        request = Request()
        request = github.GitHubTokenAuth()(request)
        assert request.headers["Authorization"] == f"Bearer {mock_data.GITHUB_TOKEN}"
        assert request.headers["Accept"] == "application/vnd.github+json"


def test_create_jwt(mocker):
    """Test that a valid JWT is successfully created from a private key."""
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_data.PRIVATE_KEY))
    github_jwt = github.create_jwt()
    # Check that the JWT contains the expected GitHub app ID.
    assert (
        jwt.decode(github_jwt, mock_data.PUBLIC_KEY, algorithms=["RS256"])["iss"]
        == "test_app_id"
    )


def test_get_installation(mocker, response_mock):
    """Test that the correct GitHub App installation ID is returned."""
    mocker.patch(
        "requests.get", return_value=response_mock(mock_data.GITHUB_INSTALLATION_JSON)
    )
    installation = github.get_installation("jwt")
    assert installation == mock_data.GITHUB_INSTALLATION_ID


def test_get_access_token(mocker, response_mock):
    """Test that a valid GitHub access token is returned."""
    mocker.patch(f"{mock_data.GITHUB_UTILS_PATH}.create_jwt")
    mocker.patch(f"{mock_data.GITHUB_UTILS_PATH}.get_installation")
    mocker.patch(
        "requests.post", return_value=response_mock(mock_data.GITHUB_TOKEN_JSON)
    )
    token, expiry = github.get_access_token()
    assert token == mock_data.GITHUB_TOKEN
    assert expiry == mock_data.GITHUB_EXPIRATION


def test_get_new_commits(mocker, response_mock):
    """Test that new GitHub commits are successfully returned."""
    mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.GITHUB_COMMITS[0],
    )
    mocker.patch(
        f"{mock_data.GITHUB_UTILS_PATH}.GitHubTokenAuth.__call__",
        return_value=Request(),
    )
    mocker.patch(
        "requests.get", return_value=response_mock(mock_data.GITHUB_COMMITS_JSON)
    )
    commits = github.get_new_commits("owner", "repo", "semester")
    assert commits == mock_data.GITHUB_COMMITS_JSON


def test_get_new_commits_no_last_commit(mocker, response_mock):
    """Test that new GitHub commits are successfully returned even when there is no previous commit
    to indicate the most recent date of a commit in the database."""
    mocker.patch("pymongo.collection.Collection.find_one", return_value=None)
    mocker.patch(
        f"{mock_data.GITHUB_UTILS_PATH}.GitHubTokenAuth.__call__",
        return_value=Request(),
    )
    mocker.patch(
        "requests.get", return_value=response_mock(mock_data.GITHUB_COMMITS_JSON)
    )
    commits = github.get_new_commits("owner", "repo", "semester")
    assert commits == mock_data.GITHUB_COMMITS_JSON


def test_get_new_commits_no_new_commits(mocker, response_mock):
    """Test that no GitHub commits are returned when there are no new commits."""
    mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.GITHUB_COMMITS[0],
    )
    mocker.patch(
        f"{mock_data.GITHUB_UTILS_PATH}.GitHubTokenAuth.__call__",
        return_value=Request(),
    )
    mocker.patch("requests.get", return_value=response_mock([]))
    commits = github.get_new_commits("owner", "repo", "semester")
    assert not commits


def test_store_commits(mocker):
    """Test that GitHub commits are successfully stored in the database."""
    mock_check_course_in_db = mocker.patch(
        f"{mock_data.GITHUB_UTILS_PATH}.check_course_in_db"
    )
    mock_bulk_write = mocker.patch("pymongo.collection.Collection.bulk_write")
    datetime_mock = mocker.patch(f"{mock_data.GITHUB_UTILS_PATH}.datetime")
    # Mock current datetime.
    datetime_mock.now.return_value = datetime.fromisoformat("2021-04-20T00:00:00")
    github.store_commits(mock_data.GITHUB_COMMITS_JSON, "repo", "semester")
    mock_check_course_in_db.assert_called_once_with("semester", [".github.commits"])
    mock_bulk_write.assert_called_once_with(
        [
            UpdateOne(
                {"sha": "f7c3b0c"},
                {
                    "$set": {
                        "sha": "f7c3b0c",
                        "author": "testuser",
                        "timestamp": "2020-01-01T00:00:00Z",
                        "message": "Test commit",
                        "repo_name": "repo",
                        "fetched_at": "2021-04-20T00:00:00",
                    },
                },
                upsert=True,
            )
        ]
    )


def test_store_commits_no_commits(mocker):
    """Test that no GitHub commits are stored in the database when an empty list is passed."""
    mock_check_course_in_db = mocker.patch(
        f"{mock_data.GITHUB_UTILS_PATH}.check_course_in_db"
    )
    mock_bulk_write = mocker.patch("pymongo.collection.Collection.bulk_write")
    github.store_commits([], "repo", "semester")
    mock_check_course_in_db.assert_called_once()
    mock_bulk_write.assert_called_once_with([])


def test_store_commits_invalid_course(mocker):
    """Test that an error is raised when a non-existent course is passed."""
    mock_check_course_in_db = mocker.patch(
        f"{mock_data.GITHUB_UTILS_PATH}.check_course_in_db",
        side_effect=HTTPException(404),
    )
    with pytest.raises(HTTPException):
        github.store_commits(mock_data.GITHUB_COMMITS_JSON, "repo", "semester")
    mock_check_course_in_db.assert_called_once()
