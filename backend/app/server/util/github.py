"""Helper functions for interacting with the GitHub API."""
import time
from datetime import datetime, timezone
from typing import List

import jwt
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from fastapi.encoders import jsonable_encoder
from pymongo import UpdateOne
from requests.auth import AuthBase

from server.config import settings
from server.models.github import Commit
from server.util import requests
from server.util.common import check_course_in_db


class GitHubTokenAuth(AuthBase):
    """Request authentication mechanism for GitHub token authentication."""

    def __call__(self, request):
        """Attach the GitHub token to the header or regenerate if expired."""
        if datetime.now().isoformat() > settings.github_expiration:
            settings.github_token, settings.github_expiration = get_access_token()
        request.headers["Authorization"] = f"Bearer {settings.github_token}"
        request.headers["Accept"] = "application/vnd.github+json"
        return request


# Adapted from https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps#authenticating-as-a-github-app
def create_jwt():
    """Create a JSON Web Token for authenticating with the GitHub API."""
    # Private key contents.
    with open(settings.GITHUB_PRIVATE_KEY_PATH, "r", encoding="utf-8") as file:
        private_pem = file.read()
    private_key = load_pem_private_key(private_pem.encode(), password=None)

    # Generate the JWT.
    payload = {
        # Issued at time, 60 seconds in the past to allow for clock drift.
        "iat": int(time.time()) - 60,
        # JWT expiration time (10 minute maximum).
        "exp": int(time.time()) + (10 * 60),
        # GitHub App's identifier.
        "iss": settings.GITHUB_APP_ID,
    }
    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation(github_jwt: str):
    """Get the installation ID for the GitHub App."""
    headers = {
        "Authorization": f"Bearer {github_jwt}",
        "Accept": "application/vnd.github+json",
    }
    url = "https://api.github.com/app/installations"
    res = requests.get(url, headers=headers)
    # Currently we only handle one installation due to private GitHub Apps.
    return res.json()[0]["id"]


def get_access_token():
    """Get an access token for the GitHub App."""
    github_jwt = create_jwt()
    installation_id = get_installation(github_jwt)
    headers = {
        "Authorization": f"Bearer {github_jwt}",
        "Accept": "application/vnd.github+json",
    }
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    res = requests.post(url, headers=headers)
    return res.json()["token"], res.json()["expires_at"]


def get_new_commits(owner: str, repo: str, course_name: str):
    """Get all commits for a repository that are newer than what we have in our database."""
    coll = settings.database[course_name].github.commits

    # We only fetch commits that are newer than what we currently have in our database.
    # This makes the assumption that commits on the main branch of the repository
    # will not be modified.
    most_recent_commit = coll.find_one({"repo_name": repo},sort=[("timestamp", -1)])

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"per_page": 100}
    if most_recent_commit:
        params["since"] = most_recent_commit["timestamp"]
    commits = []

    while True:
        # Get the max amount of commits per page (100) to save on quota.
        res = requests.get(url, params=params, auth=GitHubTokenAuth())
        commits.extend(res.json())
        # Keep fetching the next page of commits until there are no more.
        if "next" not in res.links:
            break
        url = res.links["next"]["url"]

    return commits


def store_commits(commits: List[any], repo: str, course_name: str):
    """Store commits in the database."""
    check_course_in_db(course_name, [".github.commits"])

    # Use upsert to insert a new commit,
    # or simply update the information if already present (sha will be a unique identifier).
    batch_update = [
        (
            UpdateOne(
                {
                    "sha": commit["sha"],
                },
                {
                    "$set": jsonable_encoder(
                        Commit(
                            sha=commit["sha"],
                            author=commit["author"]["login"],
                            timestamp=commit["commit"]["author"]["date"],
                            message=commit["commit"]["message"],
                            repo_name=repo,
                            fetched_at=datetime.now(timezone.utc).isoformat(),
                        )
                    )
                },
                upsert=True,
            )
        )
        for commit in commits
    ]

    # Write all at once.
    settings.database[course_name].github.commits.bulk_write(batch_update)
