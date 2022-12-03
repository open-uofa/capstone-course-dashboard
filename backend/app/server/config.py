"""Global config settings for the app using Pydantic Settings."""
import os
import sys

from pydantic import BaseSettings
from pymongo import MongoClient
from pymongo.database import Database


class Settings(BaseSettings):
    """Global variables for the app."""

    # Should remain constant.
    MONGODB_ADDRESS: str = None
    DB_NAME: str = None

    GITHUB_APP_ID: str = None
    GITHUB_PRIVATE_KEY_PATH: str = None

    API_SECRET_KEY: str = None

    HTTP_TIMEOUT: int = 60

    # Variable.
    database: Database = None
    mongodb_client: MongoClient = None

    github_token: str = None
    github_expiration: str = None

    class Config:
        """Load the .env file."""

        env_file = os.path.join(sys.path[0], "server", ".env")


settings = Settings()
