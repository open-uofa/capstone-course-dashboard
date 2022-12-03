"""Test FastAPI endpoints for auth-related actions."""


from server.config import settings
from tests.unit import mock_data


def test_submit_auth(client, mocker, response_mock):
    """Test submitting a valid Google token and receiving a JWT access token."""
    # Need to mock the google call since there's no way to test it without providing sensitive user credentials.
    mocker.patch("requests.get", return_value=response_mock(mock_data.GOOGLE_USER_JSON))
    res = client.post("/auth", json={"token": "test_google_token"})
    assert res.status_code == 200
    assert res.json()["result"]


def test_submit_auth_invalid_token(client):
    """Test authorization with unauthorized Google token."""
    res = client.post("/auth", json={"token": "invalid_token"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Could not validate credentials"


def test_submit_auth_invalid_email(client, mocker, response_mock):
    """Test submitting a Google token with an email not in the database."""
    # Need to mock the google call since there's no way to test it without providing sensitive user credentials.
    mocker.patch("tests.unit.mock_data.GOOGLE_USER_JSON", {"email": "invalid_email"})
    mocker.patch("requests.get", return_value=response_mock(mock_data.GOOGLE_USER_JSON))
    res = client.post("/auth", json={"token": "test_google_token"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Could not validate credentials"


def test_check_auth(client, token):
    """Test checking if user is authorized."""
    res = client.get("/auth/check", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.text == '"Valid"'


def test_check_auth_blacklisted(client):
    """Test checking if user is blacklisted."""
    res = client.get(
        "/auth/check", headers={"Authorization": "Bearer blacklisted_token"}
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Could not validate credentials"


def test_check_auth_unauthorized(client):
    """Test checking if unauthorized user is authorized."""
    res = client.get("/auth/check", headers={"Authorization": "Bearer invalid_token"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Could not validate credentials"


def test_refresh(client, token):
    """Test refresh tokens"""
    res = client.post(
        "/refresh",
        json={"grant_type": "refresh_token", "refresh_token": token},
    )
    assert res.status_code == 200
    assert res.json()["result"]


def test_refresh_invalid_token(client):
    """Test refresh with invalid refresh token."""
    res = client.post(
        "/refresh",
        json={"grant_type": "refresh_token", "refresh_token": "invalid_token"},
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Could not validate credentials"


def test_refresh_invalid_email(client, bad_token):
    """Test refresh tokens"""
    res = client.post(
        "/refresh", json={"grant_type": "refresh_token", "refresh_token": bad_token}
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Could not validate credentials"


def test_logout(client, token):
    """Test logging out a user."""
    res = client.get("/logout", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["result"]
    # Check that token is blacklisted.
    assert settings.database["tokens"].find_one({"token": token}) is not None
    # Remove the token, just so it can be used in further tests.
    settings.database["tokens"].delete_one({"token": token})


def test_logout_unauthorized(client):
    """Test logging out a user that is not authorized."""
    res = client.get("/logout", headers={"Authorization": "Bearer invalid_token"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Could not validate credentials"
