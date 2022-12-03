"""Fixtures for integration tests."""
import os
from distutils import dir_util

import pytest
from fastapi.testclient import TestClient

from server.app import app
from server.config import settings
from server.util.jwt import create_token
from tests.integration.config import collections, test_settings

# Import fixtures for use in integration tests.
# pylint: disable=unused-import
from tests.unit.conftest import mock_data, response_mock


@pytest.fixture(scope="session", autouse=True)
def set_test_db():
    """Set testing-specific config for the app."""
    for key in [
        "MONGODB_ADDRESS",
        "DB_NAME",
        "GITHUB_APP_ID",
        "GITHUB_PRIVATE_KEY_PATH",
    ]:
        # If the key is not set in the test config, use the values from the main config.
        value = getattr(test_settings, key, None)
        if value is not None:
            setattr(settings, key, value)


@pytest.fixture(scope="session", autouse=True)
def client(set_test_db):
    """A client we can use for testing calls to the API.

    Ensure this fixture runs after we set test-specific config values by passing set_test_db as a
    parameter.

    """
    # Using with allows the startup events to run.
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def clean_database(client):
    """Clean the database before each test session.

    This means dropping the database and creating a new one from scratch,
    following our testing template.

    Ensure this fixture runs after the client runs its startup events by passing client as a
    parameter.

    """
    settings.mongodb_client.drop_database(test_settings.DB_NAME)

    for key, val in collections.items():
        settings.database[key].insert_many(val)
        # The above line adds the _id field to the collection for some reason. Remove it.
        del val[0]["_id"]


@pytest.fixture()
def datadir(tmp_path, request):
    """Fixture for loading test data."""
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmp_path))
    return str(tmp_path)


@pytest.fixture()
def token():
    """Create JWT token used for testing API endpoints."""
    return create_token("admin@gmail.com")


@pytest.fixture()
def bad_token():
    """Create JWT token used for testing API endpoints."""
    return create_token("admin.com")


@pytest.fixture()
def token_no_courses():
    """
    Create JWT token used for testing API endpoints.
    This token represents a user with no assigned courses.
    """
    return create_token("test_email2@gmail.com")
