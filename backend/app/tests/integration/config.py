"""Config settings for testing the app.

Can be loaded from a testing .env file or by default uses the values from the app's .env file."""
import os
import sys

from bson import ObjectId
from pydantic import BaseSettings


class TestSettings(BaseSettings):
    """Global variables for the app."""

    # Should remain constant.
    MONGODB_ADDRESS: str = None
    DB_NAME: str = "test_db"

    GITHUB_APP_ID: str = None
    GITHUB_PRIVATE_KEY_PATH: str = None
    GITHUB_OWNER: str = "Spazdaa"
    GITHUB_REPO: str = "capstone-dashboard-duplicate"

    class Config:
        """Load the .env file."""

        env_file = os.path.join(sys.path[0], "tests", "integration", ".env")


test_settings = TestSettings()


# Database contents for testing.

collections = {
    "course1.comments": [
        {
            "_id": ObjectId("5f9f1b9b9b9b9b9b9b9b9b9b"),
            "message": "Hello, my name is Inigo Montoya.",
            "team": "team1",
            "sprint_number": 2,
            "created_at": "2020-01-01T00:00:00Z",
            "last_modified_at": "2020-01-02T00:00:00Z",
        },
        {
            "_id": ObjectId("5f9f1b9b9b9b9b9b9b9b9b9c"),
            "message": "Stop saying that!",
            "team": "team1",
            "sprint_number": 1,
            "created_at": "2020-01-01T00:00:00Z",
            "last_modified_at": "2020-01-02T00:00:00Z",
        },
    ],
    "course1.github.commits": [
        {
            "sha": "88015676005906f9e514ebae3164b8c8256356e6",
            "author": "octocat",
            "message": "Initial commit",
            "repo_name": "cats-in-space",
            "timestamp": "2020-01-08T00:00:00Z",
            "fetched_at": "2020-01-09T00:00:00Z",
        }
    ],
    "course1.sprints": [
        {
            "sprint_number": 1,
            "start_date": "2020-01-01T00:00:00Z",
            "end_date": "2020-01-29T00:00:00Z",
            "sprint_file_name": "sprint1.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?output=csv",
        },
        {
            "sprint_number": 2,
            "start_date": "2020-02-01T00:00:00Z",
            "end_date": "2020-02-28T00:00:00Z",
            "sprint_file_name": "sprint2.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?output=csv",
        },
    ],
    "course1.students": [
        {
            "email": "octocat@github.ca",
            "full_name": "Octocat Cat",
            "source_control_username": "octocat",
            "project": "Cats in Space",
            "repo_name": "cats-in-space",
            "ta": "Octo Daddy",
            "course_name": "course1",
            "form_submitted": True,
            "experience_survey": {
                "course_work": "291, 301",
                "langs": "I have experience with many different programming languages and development tools. I am comfortable working in a variety of environments and am able to learn new languages and tools quickly.",
                "hopes": "I hope to develop a strong foundation in the principles of software engineering and to gain practical experience in common software engineering tools and techniques.",
                "diffs": "I expect CMPUT 401 to be more challenging than my prior courses.",
                "experience": "I have been programming for 5 years. I am experienced in C++, Java, Python, and HTML/CSS. I have also done some web development with PHP and MySQL. I am always willing to learn new languages and technologies.",
            },
        }
    ],
    "course1.students.sprints": [
        {
            "email": "octocat@github.ca",
            "sprint": 1,
            "received_peer_revs": {
                "octocat@github.ca": {
                    "rating": 3,
                    "what_did_they_do": "recorded meetings, project backlog, high level architecture",
                },
                "monkeyc@github.ca": {
                    "rating": 4,
                    "what_did_they_do": "spent a lot of time, like a lot of time, on high level architecture",
                },
                "monkeydu@github.ca": {
                    "rating": 5,
                    "what_did_they_do": "I didn't pay too much attention, but I think they worked on the project backlog",
                },
            },
            "avg_rating": 4.0,
            "stddev_rating": 1.0,
            "personal_peer_rev": {
                "meeting_participation": 8,
                "meeting_content": "What each members has/will complete, as well as the overall progress of the project",
                "missed_meetings": "i believe just one (picking up the device from Octo Daddy, only 3 people showed up for it)",
                "project_appropriate": "yes",
                "confident_to_learn_sd": "5",
                "capable_to_learn_sd": "6",
                "able_to_achieve_learning_goals": "6",
                "able_to_meet_sd_challenge": "4",
                "students_care": "3",
                "connected_with_others": "2",
                "hard_to_get_help": "1",
                "uneasy_exposing_gaps": "4",
                "reluctant_to_speak_openly": "5",
                "can_rely_on_others": "5",
                "given_opportunities_to_learn": "5",
                "confident_others_will_support_me": "4",
            },
        }
    ],
    "course1.minutes": [
        {
            "title": "January 8, 2020",
            "body": "Agenda for today's meeting: ...",
            "team": "team1",
            "timestamp": "2020-01-08T00:00:00Z",
        },
        {
            "title": "February 11, 2020",
            "body": "Agenda for today's meeting: ...",
            "team": "team1",
            "timestamp": "2020-02-11T00:00:00Z",
        },
    ],
    "courses": [
        {
            "name": "course1",
            "roster_file_name": "roster1.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        {
            "name": "course2",
            "roster_file_name": "roster2.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
    ],
    "user": [
        {
            "email": "admin@gmail.com",
            "assigned_courses": ["course1"],
            "authorized": True,
        },
        {
            "email": "test_email",
            "assigned_courses": ["course1"],
            "authorized": True,
        },
        {
            "email": "test_email2@gmail.com",
            "assigned_courses": [],
            "authorized": True,
        },
    ],
    "tokens": [{"token": "blacklisted_token"}],
}
