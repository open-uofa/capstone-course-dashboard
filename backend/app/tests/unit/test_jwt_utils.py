"""Test helper functions for managing authorization."""
from datetime import timedelta

import jwt as pyjwt
import pytest
from fastapi import HTTPException

from server.util import jwt
from tests.unit import mock_data


def test_cast_to_number(mocker):
    """Test successful cast from an env var to a float."""
    mock_get = mocker.patch("os.environ.get", return_value=1)
    float_cast = jwt.cast_to_number("TEST_VAR")
    mock_get.assert_called_once_with("TEST_VAR")
    assert float_cast == 1.0


def test_cast_to_number_invalid(mocker):
    """Test unsuccessful cast from an env var to a float."""
    mock_get = mocker.patch("os.environ.get", return_value="invalid")
    float_cast = jwt.cast_to_number("TEST_VAR")
    mock_get.assert_called_once_with("TEST_VAR")
    assert float_cast is None


def test_cast_to_number_missing(mocker):
    """Test unsuccessful cast from a non-existent env var to a float."""
    mock_get = mocker.patch("os.environ.get", return_value=None)
    float_cast = jwt.cast_to_number("TEST_VAR")
    mock_get.assert_called_once_with("TEST_VAR")
    assert float_cast is None


def test_create_access_token():
    """Test successful creation of a JWT access token."""
    access_token = jwt.create_access_token(data={"sub": "test_email"})
    assert (
        pyjwt.decode(access_token, mock_data.API_SECRET_KEY, algorithms=["HS256"])[
            "sub"
        ]
        == "test_email"
    )


def test_create_access_token_no_api_key(mocker):
    """Test unsuccessful creation of a JWT access token due to missing API key."""
    mocker.patch("server.config.settings.API_SECRET_KEY", None)
    with pytest.raises(BaseException) as excinfo:
        jwt.create_access_token(data={"sub": "test_email"})
    assert excinfo.exconly() == "BaseException: Missing API_SECRET_KEY env var."


def test_create_token(mocker):
    """Test creating a token from an email."""
    mock_create_access_token = mocker.patch(
        "server.util.jwt.create_access_token", return_value="test_access_token"
    )
    access_token = jwt.create_token("test_email")
    mock_create_access_token.assert_called_once_with(
        data={"sub": "test_email"}, expires_delta=timedelta(minutes=15)
    )
    assert access_token == "test_access_token"


def test_valid_email_from_db(mocker):
    """Test successful validation of an email from the database."""
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one", return_value={"authorized": True}
    )
    valid_email = jwt.valid_email_from_db("test_email")
    mock_find_one.assert_called_once_with({"email": "test_email"})
    assert valid_email == "test_email"


def test_valid_email_from_db_not_authorized(mocker):
    """Test unsuccessful validation of an email from the database due to not being authorized."""
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one", return_value={"authorized": False}
    )
    with pytest.raises(HTTPException) as excinfo:
        jwt.valid_email_from_db("test_email")
    mock_find_one.assert_called_once_with({"email": "test_email"})
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"


def test_get_current_user_email(mocker):
    """Test successful retrieval of the current user's email."""
    mock_is_token_blacklisted = mocker.patch(
        "server.util.jwt.is_token_blacklisted", return_value=False
    )
    mock_decode_token = mocker.patch(
        "server.util.jwt.decode_token", return_value={"sub": "test_email"}
    )
    mock_valid_email_from_db = mocker.patch(
        "server.util.jwt.valid_email_from_db", return_value=True
    )

    current_user_email = jwt.get_current_user_email("test_access_token")
    mock_is_token_blacklisted.assert_called_once_with("test_access_token")
    mock_decode_token.assert_called_once_with("test_access_token")
    mock_valid_email_from_db.assert_called_once_with("test_email")
    assert current_user_email == "test_email"


def test_get_current_user_email_blacklisted(mocker):
    """Test unsuccessful retrieval of the current user's email due to the token being blacklisted."""
    mock_is_token_blacklisted = mocker.patch(
        "server.util.jwt.is_token_blacklisted", return_value=True
    )
    with pytest.raises(HTTPException) as excinfo:
        jwt.get_current_user_email("test_access_token")
    mock_is_token_blacklisted.assert_called_once_with("test_access_token")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"


def test_get_current_user_email_invalid_token(mocker):
    """Test unsuccessful retrieval of the current user's email due to no email being provided."""
    mock_is_token_blacklisted = mocker.patch(
        "server.util.jwt.is_token_blacklisted", return_value=False
    )
    mock_decode_token = mocker.patch("server.util.jwt.decode_token", return_value={})

    with pytest.raises(HTTPException) as excinfo:
        jwt.get_current_user_email("test_access_token")
    mock_is_token_blacklisted.assert_called_once_with("test_access_token")
    mock_decode_token.assert_called_once_with("test_access_token")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"


def test_get_current_user_email_invalid_email(mocker):
    """Test unsuccessful retrieval of the current user's email due to the email not being in the database."""
    mock_is_token_blacklisted = mocker.patch(
        "server.util.jwt.is_token_blacklisted", return_value=False
    )
    mock_decode_token = mocker.patch(
        "server.util.jwt.decode_token", return_value={"sub": "test_email"}
    )
    mock_valid_email_from_db = mocker.patch(
        "server.util.jwt.valid_email_from_db", return_value=False
    )

    with pytest.raises(HTTPException) as excinfo:
        jwt.get_current_user_email("test_access_token")
    mock_is_token_blacklisted.assert_called_once_with("test_access_token")
    mock_decode_token.assert_called_once_with("test_access_token")
    mock_valid_email_from_db.assert_called_once_with("test_email")
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Could not validate credentials"
    assert excinfo.value.headers["WWW-Authenticate"] == "Bearer"


def test_get_current_user_token(mocker):
    """Test successful retrieval of the current user's token."""
    mock_get_current_user_email = mocker.patch("server.util.jwt.get_current_user_email")
    token = jwt.get_current_user_token("test_access_token")
    mock_get_current_user_email.assert_called_once_with("test_access_token")
    assert token == "test_access_token"


def test_add_blacklist_token(mocker):
    """Test successful addition of a token to the blacklist."""
    mock_insert_one = mocker.patch("pymongo.collection.Collection.insert_one")
    add_token = jwt.add_blacklist_token("test_access_token")
    mock_insert_one.assert_called_once_with({"token": "test_access_token"})
    assert add_token


def test_is_token_blacklisted(mocker):
    """Test successful check if a token is blacklisted."""
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value={"token": "test_access_token"},
    )
    is_blacklisted = jwt.is_token_blacklisted("test_access_token")
    mock_find_one.assert_called_once_with({"token": "test_access_token"})
    assert is_blacklisted


def test_is_token_blacklisted_not_blacklisted(mocker):
    """Test unsuccessful check if a token is blacklisted."""
    mock_find_one = mocker.patch(
        "pymongo.collection.Collection.find_one", return_value=None
    )
    is_blacklisted = jwt.is_token_blacklisted("test_access_token")
    mock_find_one.assert_called_once_with({"token": "test_access_token"})
    assert not is_blacklisted


def test_create_refresh_token(mocker):
    """Test successful creation of a refresh token."""
    mock_create_access_token = mocker.patch(
        "server.util.jwt.create_access_token", return_value="test_refresh_token"
    )
    refresh_token = jwt.create_refresh_token("test_email")
    mock_create_access_token.assert_called_once_with(
        data={"sub": "test_email"}, expires_delta=timedelta(days=30)
    )
    assert refresh_token == "test_refresh_token"


def test_decode_token():
    """Test successful decoding of a JWT token."""
    decoded_token = jwt.decode_token(
        pyjwt.encode({"sub": "test_email"}, mock_data.API_SECRET_KEY, algorithm="HS256")
    )
    assert decoded_token == {"sub": "test_email"}


def test_decode_token_no_api_key(mocker):
    """Test unsuccessful decoding of a JWT token due to no API key being provided."""
    mocker.patch("server.config.settings.API_SECRET_KEY", None)
    with pytest.raises(BaseException) as excinfo:
        jwt.decode_token(
            pyjwt.encode(
                {"sub": "test_email"}, mock_data.API_SECRET_KEY, algorithm="HS256"
            )
        )
    assert excinfo.exconly() == "BaseException: Missing API_SECRET_KEY env var."
