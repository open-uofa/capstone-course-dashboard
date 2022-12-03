"""Test API functions for handling Google OAuth."""
import json
import time

import pytest
from fastapi import HTTPException

from server.routes import auth
from tests.unit import mock_data


def test_submit_auth(mocker, response_mock):
    """Test successfully authorizing a user."""
    mock_get = mocker.patch(
        "requests.get", return_value=response_mock(mock_data.GOOGLE_USER_JSON)
    )
    mock_valid_email_from_db = mocker.patch(
        "server.util.jwt.valid_email_from_db", return_value=True
    )
    mock_create_token = mocker.patch(
        "server.util.jwt.create_token", return_value="test_access_token"
    )
    mock_create_refresh_token = mocker.patch(
        "server.util.jwt.create_refresh_token", return_value="test_refresh_token"
    )

    authentication = auth.submit_auth(mock_data.AUTH_REQUEST)
    mock_get.assert_called_once()
    mock_valid_email_from_db.assert_called_once_with("test_email")
    mock_create_token.assert_called_once_with("test_email")
    mock_create_refresh_token.assert_called_once_with("test_email")
    assert json.loads(authentication.body.decode()) == {
        "result": True,
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "email": "test_email",
    }


def test_submit_auth_invalid_token(mocker, response_mock):
    """Test that submit_auth handles invalid token."""
    mock_get = mocker.patch(
        "requests.get", return_value=response_mock({}, status_code=401)
    )

    with pytest.raises(HTTPException) as excinfo:
        auth.submit_auth(mock_data.AUTH_REQUEST)
    mock_get.assert_called_once()
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"


def test_submit_auth_invalid_email(mocker, response_mock):
    """Test that submit_auth handles invalid email."""
    mock_get = mocker.patch(
        "requests.get", return_value=response_mock(mock_data.GOOGLE_USER_JSON)
    )
    mock_valid_email_from_db = mocker.patch(
        "server.util.jwt.valid_email_from_db", return_value=False
    )

    with pytest.raises(HTTPException) as excinfo:
        auth.submit_auth(mock_data.AUTH_REQUEST)
    mock_get.assert_called_once()
    mock_valid_email_from_db.assert_called_once_with("test_email")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"


def test_refresh(mocker, response_mock):
    """Test successfully generates a new auth token using refresh token"""
    mock_valid_email_from_db = mocker.patch(
        "server.util.jwt.valid_email_from_db", return_value=True
    )
    mock_create_token = mocker.patch(
        "server.util.jwt.create_token", return_value="test_refresh_token"
    )
    mock_decode_token = mocker.patch(
        "server.util.jwt.decode_token",
        return_value={"exp": time.time() + 60, "sub": "test_email"},
    )
    authentication = auth.refresh(mock_data.REFRESH_REQUEST)
    mock_valid_email_from_db.assert_called_once_with("test_email")
    mock_decode_token.assert_called_once_with("test_refresh_token")
    mock_create_token.assert_called_once_with("test_email")
    assert json.loads(authentication.body.decode()) == {
        "result": True,
        "access_token": "test_refresh_token",
    }


def test_refresh_invalid_token(mocker, response_mock):
    """Test that refresh handles invalid token"""
    mock_decode_token = mocker.patch(
        "server.util.jwt.decode_token",
        return_value={"exp": time.time() - 60, "sub": "test_email"},
    )

    with pytest.raises(HTTPException) as excinfo:
        auth.refresh(mock_data.REFRESH_REQUEST)
    mock_decode_token.assert_called_once()
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"


def test_refresh_invalid_email(mocker, response_mock):
    """Test that refresh handles invalid email."""
    mock_decode_token = mocker.patch(
        "server.util.jwt.decode_token",
        return_value={"exp": time.time() + 60, "sub": "test_email"},
    )
    mock_valid_email_from_db = mocker.patch(
        "server.util.jwt.valid_email_from_db", return_value=False
    )

    with pytest.raises(HTTPException) as excinfo:
        auth.refresh(mock_data.REFRESH_REQUEST)
    mock_decode_token.assert_called_once()
    mock_valid_email_from_db.assert_called_once_with("test_email")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"


def test_check_auth():
    """Test that check_auth returns as expected."""
    response = auth.check_auth()
    assert response == "Valid"


def test_logout(mocker):
    """Test that logout blacklists the token."""
    mock_add_blacklist_token = mocker.patch(
        "server.util.jwt.add_blacklist_token", return_value=True
    )
    response = auth.logout("test_access_token")
    mock_add_blacklist_token.assert_called_once_with("test_access_token")
    assert json.loads(response.body.decode()) == {"result": True}


def test_logout_invalid_token(mocker):
    """Test that logout handles invalid token."""
    mock_add_blacklist_token = mocker.patch(
        "server.util.jwt.add_blacklist_token", return_value=False
    )
    with pytest.raises(HTTPException) as excinfo:
        auth.logout("test_access_token")
    mock_add_blacklist_token.assert_called_once_with("test_access_token")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"
