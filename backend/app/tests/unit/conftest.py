"""Fixtures for unit tests."""
import os
from distutils import dir_util

import pytest
from requests import Response

from server.config import settings
from tests.unit import mock_data


@pytest.fixture(scope="session", autouse=True)
def mock_settings():
    """Mock the global variables used throughout the program."""
    settings.MONGODB_ADDRESS = mock_data.DB_ADDRESS
    settings.DB_NAME = mock_data.DB_NAME
    settings.GITHUB_APP_ID = mock_data.GITHUB_APP_ID
    settings.GITHUB_PRIVATE_KEY_PATH = mock_data.GITHUB_PRIVATE_KEY_PATH
    settings.HTTP_TIMEOUT = mock_data.HTTP_TIMEOUT
    settings.API_SECRET_KEY = mock_data.API_SECRET_KEY
    settings.database = mock_data.DATABASE
    settings.github_token = mock_data.GITHUB_TOKEN
    settings.github_expiration = mock_data.GITHUB_EXPIRATION


@pytest.fixture()
def response_mock():
    """Mock request.Response to return a custom value."""

    def _response_mock(value, status_code=200, content=None):
        response = Response()
        response.json = lambda: value
        response.status_code = status_code
        if content is not None:
            # This is just for testing, so we want to set this value directly, even if it is protected.
            # pylint: disable=protected-access
            response._content = content
        return response

    return _response_mock


@pytest.fixture()
def datadir(tmp_path, request):
    """Fixture for loading test data."""
    filename = request.module.__file__
    print(filename)
    test_dir, _ = os.path.splitext(filename)
    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmp_path))
    return str(tmp_path)
