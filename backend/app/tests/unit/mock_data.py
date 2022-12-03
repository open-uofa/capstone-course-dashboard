"""File for storing (generally large) mock data for unit testing."""
import pymongo
from fastapi.encoders import jsonable_encoder

from server.models.comments import Comment, CommentResponse
from server.models.courses import Course, Sprint
from server.models.github import GithubRequest, StudentCommit, TeamCommit, TeamCommits
from server.models.minutes import Minute
from server.models.models import AuthRequest, RefreshRequest
from server.models.students import Student, StudentSprintData, StudentsResponse

GITHUB_UTILS_PATH = "server.util.github"

DB_ADDRESS = "mongodb://localhost:27017"
DB_NAME = "test_db"
GITHUB_APP_ID = "test_app_id"
GITHUB_PRIVATE_KEY_PATH = "private/key/path.pem"
HTTP_TIMEOUT = 60
DATABASE = pymongo.MongoClient().test_database
GITHUB_TOKEN = "test_github_token"
GITHUB_EXPIRATION = "1234567890"
GITHUB_INSTALLATION_ID = 123456
GOOGLE_CLIENT_ID = "test_google_client_id"
GOOGLE_CLIENT_SECRET = "test_google_client_secret"
API_SECRET_KEY = "test_api_secret_key"
SECRET_KEY = "test_secret_key"
METHOD = "POST"

GITHUB_COMMITS_JSON = [
    {
        "sha": "f7c3b0c",
        "author": {
            "login": "testuser",
        },
        "commit": {
            "author": {
                "date": "2020-01-01T00:00:00Z",
            },
            "message": "Test commit",
        },
    }
]

GITHUB_COMMITS = [
    {
        "sha": "f7c3b0c",
        "author": "testuser",
        "timestamp": "2020-01-01T00:00:00Z",
        "message": "Test commit",
        "repo_name": "test_repo",
        "fetched_at": "2020-01-01T00:00:00Z",
    }
]

GITHUB_TOKEN_JSON = {
    "token": GITHUB_TOKEN,
    "expires_at": GITHUB_EXPIRATION,
}

GITHUB_INSTALLATION_JSON = [{"id": GITHUB_INSTALLATION_ID}]

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCuZEXEdB6inRA7ZKirLv7GcZjhT/21qcr3Iou/cMU1AXRGe613
20AF4BmC2oEtC5ni3nQrQ/y49ooVBe1g61P7z2hKuHlchV7Y7K0+kD8DmjgcQOET
zvXghJhAA8IPR5q7c9Z4J3ipfegz3XMWZvq18hKb8DjgVnRvmZTaNMYi0wIDAQAB
AoGBAIzsDJDPAP6JC1fjZIVIaas0msTf3fZR6ejBKsqdt065CRv3z1q+esMEr7jV
F3OuH0F8X8Win/NbjoOkkYkzQV4yERoboaLcMT1l12jRSfowsPezRZ0wbrxbejFL
6Gv/+2t+ChDcnJl5PuIsYhtQF5q6Qp7ZWIEo6H88HOoZcxLpAkEA3MFG/oY7yVcI
S982SZLKWtxREXtDsgYwpn5O/GDvtsaTnvEbgy9SnBO6h3r+KNC/02wHpVw2+VtI
lIItxvqeFwJBAMo8B3qRiIeImP0+tT/+RbwxqgN5oTu+Roy9JA9j/EVySRxqghFM
izrA0TNqM3dvyw9L5O1mrW1QGpREhlrocqUCQEvqxAmADEt/fMDq8HZ43tJEdjS2
2V79tflr8qnkhEutGtNMQ5Pn0FcQidNRvto2f+Grgy2g+t7iP6Gi6y9EvN0CQHaN
uEinFiV181HKOBC6rADGEIeW/uj6A3uvyXroP1QqyidJXNRtTdV0gW8lm+QxehWO
hTaSkapaYip2/Vg/mi0CQAdaF6NgMw58Zi9oi0USqJLUcfEM1OVYtYjIK3lt2J44
tCRDGnnTb73o44K/g2D4ap0AbvKtPzG3/g1aiJH38xQ=
-----END RSA PRIVATE KEY-----"""

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCuZEXEdB6inRA7ZKirLv7GcZjh
T/21qcr3Iou/cMU1AXRGe61320AF4BmC2oEtC5ni3nQrQ/y49ooVBe1g61P7z2hK
uHlchV7Y7K0+kD8DmjgcQOETzvXghJhAA8IPR5q7c9Z4J3ipfegz3XMWZvq18hKb
8DjgVnRvmZTaNMYi0wIDAQAB
-----END PUBLIC KEY-----"""

GITHUB_REQUEST = GithubRequest(
    owner="test_owner",
    repo="test_repo",
    course_name="test_course",
)

AUTH_REQUEST = AuthRequest(
    token="test_token",
)

REFRESH_REQUEST = RefreshRequest(
    grant_type="refresh_token", refresh_token="test_refresh_token"
)

ID_INFO_JSON = {
    "email": "test_email",
}

USER_JSON = {
    "authorized": True,
    "email": "test_email",
    "assigned_courses": ["course_name"],
}

SPRINT_DATES = {
    "start_date": "2020-01-01T00:00:00Z",
    "end_date": "2020-01-02T00:00:00Z",
}

STUDENT_COMMIT = StudentCommit(username="test_student", number_of_commits=42)

STUDENT_COMMIT_EMPTY = StudentCommit(username="test_student", number_of_commits=0)

TEAM_COMMITS = TeamCommits(
    student_commits=[STUDENT_COMMIT],
    last_fetched_at="2020-01-01T00:00:00Z",
)

TEAM_COMMITS_EMPTY = TeamCommits(
    student_commits=[STUDENT_COMMIT_EMPTY],
    last_fetched_at=None,
)

TEAM_COMMIT = TeamCommit(
    team_name="test_team",
    number_of_commits=42,
)

TEAM_COMMIT_EMPTY = TeamCommit(
    team_name="test_team",
    number_of_commits=0,
)

GOOGLE_USER_JSON = {"email": "test_email"}

STUDENT_UTILS_PATH = "server.util.students"

STUDENT_JSON = {
    "email": "test_email",
    "full_name": "test_name",
    "source_control_username": "test_username",
    "project": "test_project",
    "repo_name": "test_repo",
    "ta": "test_ta",
    "course_name": "test_course",
    "form_submitted": True,
    "experience_survey": {"experience": "I have a lot of experience"},
}

STUDENT_SPRINT_JSON = {
    "email": "test_email",
    "sprint": 1,
    "personal_peer_rev": {"workcompleted": "task A"},
    "received_peer_revs": {"monkey@ualberta.ca": {"rating": 3}},
    "avg_rating": 3.0,
    "stddev_rating": 1.5,
}

FORM = {
    "_id": {"$oid": "63470190fe34e89a25a8538a"},
    "sprint_number": 1,
    "start_date": "2022-09-05T19:05:45Z",
    "end_date": "2022-09-24T19:05:45Z",
    "sprint_file_name": "W2023_sprint1.csv",
    "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlD-M0-bVSzSYqis_epj_Uti7Mj8lDsqPygi9vmxLNhuIfBSHorqNlQ0jTLtbkZ8pK7ps7LhmwXcll/pubhtml?widget=true&amp;headers=false",
}

LINK = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlD-M0-bVSzSYqis_epj_Uti7Mj8lDsqPygi9vmxLNhuIfBSHorqNlQ0jTLtbkZ8pK7ps7LhmwXcll/pubhtml?widget=true&amp;headers=false"

STUDENTS_RESPONSE = StudentsResponse(
    students=[
        Student(
            email="test_email",
            full_name="test_name",
            source_control_username="test_username",
            project="test_project",
            repo_name="test_repo",
            ta="test_ta",
            course_name="test_course",
            form_submitted=True,
            experience_survey={"experience": "I have a lot of experience"},
        )
    ],
    sprint_data=[
        StudentSprintData(
            email="test_email",
            sprint=1,
            personal_peer_rev={"workcompleted": "task A"},
            received_peer_revs={"monkey@ualberta.ca": {"rating": 3}},
            avg_rating=3.0,
            stddev_rating=1.5,
        )
    ],
)


class MockFileWrapper:
    def __init__(self, filename, file):
        self.filename = filename
        self.file = file


STUDENT_ROSTER_POST = [
    pymongo.UpdateOne(
        {"email": "aardvark@ualberta.ca"},
        {
            "$set": jsonable_encoder(
                Student(
                    email="aardvark@ualberta.ca",
                    full_name="Juan Carlos Rodriguez",
                    source_control_username="aardvark",
                    project="Paint Me A Picture",
                    repo_name="paint-me-a-picture",
                    ta="Luisa Rodriguez",
                    course_name="test_course",
                    form_submitted=False,
                    experience_survey={
                        "course_work": "291, 301",
                        "langs": "I have experience with many different programming languages and development tools. I am comfortable working in a variety of environments and am able to learn new languages and tools quickly.",
                        "hopes": "I hope to develop a strong foundation in the principles of software engineering and to gain practical experience in common software engineering tools and techniques.",
                        "diffs": "I expect CMPUT 401 to be more challenging than my prior courses.",
                        "experience": "I have been programming for 5 years. I am experienced in C++, Java, Python, and HTML/CSS. I have also done some web development with PHP and MySQL. I am always willing to learn new languages and technologies.",
                    },
                )
            )
        },
        upsert=True,
    )
]
STUDENT_ROSTER_RETURN = [
    Student(
        email="aardvark@ualberta.ca",
        full_name="Juan Carlos Rodriguez",
        source_control_username="aardvark",
        project="Paint Me A Picture",
        repo_name="paint-me-a-picture",
        ta="Luisa Rodriguez",
        course_name="course1",
        form_submitted=False,
        experience_survey={
            "course_work": "291, 301",
            "langs": "I have experience with many different programming languages and development tools. I am comfortable working in a variety of environments and am able to learn new languages and tools quickly.",
            "hopes": "I hope to develop a strong foundation in the principles of software engineering and to gain practical experience in common software engineering tools and techniques.",
            "diffs": "I expect CMPUT 401 to be more challenging than my prior courses.",
            "experience": "I have been programming for 5 years. I am experienced in C++, Java, Python, and HTML/CSS. I have also done some web development with PHP and MySQL. I am always willing to learn new languages and technologies.",
        },
    ),
]

STUDENT_ROSTER_EMPTY_FIELDS = Student(
    email="aardvark@ualberta.ca",
    full_name="Juan Carlos Rodriguez",
    source_control_username="aardvark",
    project="Paint Me A Picture",
    repo_name="paint-me-a-picture",
    ta="Luisa Rodriguez",
    course_name="course1",
    form_submitted=False,
    experience_survey={
        "course_work": "291, 301",
        "langs": "",
        "hopes": "",
        "diffs": "",
        "experience": "I have been programming for 5 years. I am experienced in C++, Java, Python, and HTML/CSS. I have also done some web development with PHP and MySQL. I am always willing to learn new languages and technologies.",
    },
)

ROSTER_DF_DICT = {
    "Email Address": ["aardvark@ualberta.ca"],
    "Full name (preferred)": ["Juan Carlos Rodriguez"],
    "Github Account": ["aardvark"],
    "Project": ["Paint Me A Picture"],
    "Github repo": ["paint-me-a-picture"],
    "TA": ["Luisa Rodriguez"],
    "Coursework": ["291, 301"],
    "Please describe your experience with other languages and development tools": [
        "I have experience with many different programming languages and development tools. I am comfortable working in a variety of environments and am able to learn new languages and tools quickly."
    ],
    "What do you hope to get out of your CMPUT 401 experience?": [
        "I hope to develop a strong foundation in the principles of software engineering and to gain practical experience in common software engineering tools and techniques."
    ],
    "Do you expect CMPUT 401 to be any different than your prior courses? If so, how?": [
        "I expect CMPUT 401 to be more challenging than my prior courses."
    ],
    "Experience": [
        "I have been programming for 5 years. I am experienced in C++, Java, Python, and HTML/CSS. I have also done some web development with PHP and MySQL. I am always willing to learn new languages and technologies."
    ],
}

STUDENT_SPRINT_POST = [
    pymongo.UpdateOne(
        {"email": "aardvark@ualberta.ca", "sprint": 1},
        {
            "$set": jsonable_encoder(
                StudentSprintData(
                    email="aardvark@ualberta.ca",
                    sprint=1,
                    personal_peer_rev={
                        "meeting_participation": 8.0,
                        "meeting_content": "What each members has/will complete, as well as the overall progress of the project",
                        "missed_meetings": "i believe just one (picking up the device from Jashwanth, only 3 people showed up for it)",
                        "project_appropriate": "Yes",
                        "confident_to_learn_sd": 5.0,
                        "capable_to_learn_sd": 6.0,
                        "able_to_achieve_learning_goals": 6.0,
                        "able_to_meet_sd_challenge": "4 - Somewhat true",
                        "students_care": 3.0,
                        "connected_with_others": 2.0,
                        "hard_to_get_help": 1.0,
                        "uneasy_exposing_gaps": 4.0,
                        "reluctant_to_speak_openly": 5.0,
                        "can_rely_on_others": 5.0,
                        "given_opportunities_to_learn": 5.0,
                        "confident_others_will_support_me": 4.0,
                    },
                    received_peer_revs={
                        "aardvark@ualberta.ca": {
                            "rating": 3.0,
                            "what_did_they_do": "recorded meetings, project backlog, high level architecture",
                        }
                    },
                    avg_rating=3,
                    stddev_rating=0,
                )
            )
        },
        upsert=True,
    )
]
STUDENT_SPRINT_RETURN = [
    StudentSprintData(
        email="aardvark@ualberta.ca",
        sprint=1,
        personal_peer_rev={
            "meeting_participation": 8.0,
            "meeting_content": "What each members has/will complete, as well as the overall progress of the project",
            "missed_meetings": "i believe just one (picking up the device from Jashwanth, only 3 people showed up for it)",
            "project_appropriate": "Yes",
            "confident_to_learn_sd": 5.0,
            "capable_to_learn_sd": 6.0,
            "able_to_achieve_learning_goals": 6.0,
            "able_to_meet_sd_challenge": "4 - Somewhat true",
            "students_care": 3.0,
            "connected_with_others": 2.0,
            "hard_to_get_help": 1.0,
            "uneasy_exposing_gaps": 4.0,
            "reluctant_to_speak_openly": 5.0,
            "can_rely_on_others": 5.0,
            "given_opportunities_to_learn": 5.0,
            "confident_others_will_support_me": 4.0,
        },
        received_peer_revs={
            "aardvark@ualberta.ca": {
                "rating": 3,
                "what_did_they_do": "recorded meetings, project backlog, high level architecture",
            }
        },
        avg_rating=3,
        stddev_rating=0,
    )
]

STUDENT_SPRINT_RETURN_UNSUBMITTED = [
    STUDENT_SPRINT_RETURN[0],
    StudentSprintData(
        email="tiger@ualberta.ca",
        sprint=1,
        personal_peer_rev={
            "meeting_participation": "Peer review was not sumitted.",
            "meeting_content": "Peer review was not sumitted.",
            "missed_meetings": "Peer review was not sumitted.",
            "project_appropriate": "Peer review was not sumitted.",
            "confident_to_learn_sd": "Peer review was not sumitted.",
            "capable_to_learn_sd": "Peer review was not sumitted.",
            "able_to_achieve_learning_goals": "Peer review was not sumitted.",
            "able_to_meet_sd_challenge": "Peer review was not sumitted.",
            "students_care": "Peer review was not sumitted.",
            "connected_with_others": "Peer review was not sumitted.",
            "hard_to_get_help": "Peer review was not sumitted.",
            "uneasy_exposing_gaps": "Peer review was not sumitted.",
            "reluctant_to_speak_openly": "Peer review was not sumitted.",
            "can_rely_on_others": "Peer review was not sumitted.",
            "given_opportunities_to_learn": "Peer review was not sumitted.",
            "confident_others_will_support_me": "Peer review was not sumitted.",
        },
        received_peer_revs={
            "aardvark@ualberta.ca": {
                "rating": 3,
                "what_did_they_do": "recorded meetings, project backlog, high level architecture",
            }
        },
        avg_rating=3,
        stddev_rating=0,
    ),
]

SPRINT_DF_DICT = {
    "Count": [0],
    "Email Address": ["aardvark@ualberta.ca"],
    "Team": ["Paint Me A Picture"],
    "In how many meetings did you participate during this past sprint?": [8.0],
    "What was discussed/decided in these meetings?": [
        "What each members has/will complete, as well as the overall progress of the project"
    ],
    "Were there other team meetings that you missed?": [
        "i believe just one (picking up the device from Jashwanth, only 3 people showed up for it)"
    ],
    "Do you think that this project is appropriate (in complexity and scope) for the course?": [
        "Yes"
    ],
    "Please respond to each of the following items in terms of how true it is for you with respect to your learning software development through this sprint [I feel confident in my ability to learn software development]": [
        5.0
    ],
    "Please respond to each of the following items in terms of how true it is for you with respect to your learning software development through this sprint [I am capable of learning software development]": [
        6.0
    ],
    "Please respond to each of the following items in terms of how true it is for you with respect to your learning software development through this sprint [I am able to achieve my software development learning goals]": [
        6.0
    ],
    "Please respond to each of the following items in terms of how true it is for you with respect to your learning software development through this sprint [I feel able to meet the challenge of performing well when developing software.]": [
        "4 - Somewhat true"
    ],
    "I feel that students in this course care about each other": [3.0],
    "I feel connected to others in this course": [2.0],
    "I feel that it is hard to get help when I have a question": [1.0],
    "I feel uneasy exposing gaps in my understanding": [4.0],
    "I feel reluctant to speak openly": [5.0],
    "I feel that I can rely on others in this course": [5.0],
    "I feel that I am given ample opportunities to learn": [5.0],
    "I feel confident that others will support me": [4.0],
    "Choose a team member-1": ["aardvark@ualberta.ca"],
    "How would you rate their contribution?1": [3],
    "Please provide your reasons for this rating and share more details about their contribution.1": [
        "recorded meetings, project backlog, high level architecture"
    ],
    "Choose a team member-2": [""],
    "How would you rate their contribution?2": [""],
    "Please provide your reasons for this rating and share more details about their contribution.2": [
        ""
    ],
    "Choose a team member-3": [""],
    "How would you rate their contribution?3": [""],
    "Please provide your reasons for this rating and share more details about their contribution.3": [
        ""
    ],
    "Choose a team member-4": [""],
    "How would you rate their contribution?4": [""],
    "Please provide your reasons for this rating and share more details about their contribution.4": [
        ""
    ],
    "Choose a team member-5": [""],
    "How would you rate their contribution?5": [""],
    "Please provide your reasons for this rating and share more details about their contribution.5": [
        ""
    ],
    "Choose a team member-6": [""],
    "How would you rate their contribution?6": [""],
    "Please provide your reasons for this rating and share more details about their contribution.6": [
        ""
    ],
    "Choose a team member-7": [""],
    "How would you rate their contribution?7": [""],
    "Please provide your reasons for this rating and share more details about their contribution.7": [
        ""
    ],
    "Average peer review rating": [3],
    "Peer review rating standard deviation": [0.0],
}

TEAM_MAP = {
    "aardvark@ualberta.ca": "Paint Me A Picture",
}

SPRINT_DF_DICT_NO_TEAM = SPRINT_DF_DICT.copy()
SPRINT_DF_DICT_NO_TEAM["Team"] = ["This student does not appear in the roster."]


COMMENT_ID = "5f9f1b9b9b9b9b9b9b9b9b9b"

COMMENT_REQUEST = Comment(message="test_message", team="test_team", sprint_number=1)


COMMENT = CommentResponse(
    message="test_message",
    team="test_team",
    sprint_number=1,
    created_at="2020-10-29T20:00:00.000Z",
    last_modified_at="2020-10-29T20:00:00.000Z",
    id=COMMENT_ID,
)

COMMENT_JSON = {
    "_id": COMMENT_ID,
    "message": "test_message",
    "team": "test_team",
    "sprint_number": 1,
    "created_at": "2020-10-29T20:00:00.000Z",
    "last_modified_at": "2020-10-29T20:00:00.000Z",
}

UPDATE_COMMENT_JSON = {
    "message": "test_message",
    "team": "test_team",
    "sprint_number": 1,
}

COURSE = Course(
    name="course_name",
    roster_file_name="roster.csv",
    use_github=True,
    use_team_structure=True,
    use_student_experience_form=True,
)

COURSE_JSON = {
    "name": "course_name",
    "roster_file_name": "roster.csv",
    "use_github": True,
    "use_team_structure": True,
    "use_student_experience_form": True,
}

SPRINT = Sprint(
    sprint_number=1,
    start_date="2020-01-01T00:00:00Z",
    end_date="2020-01-02T00:00:00Z",
    sprint_file_name="sprint1.csv",
    forms_url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?output=csv",
)

SPRINT_JSON = {
    "sprint_number": 1,
    "start_date": "2020-01-01T00:00:00Z",
    "end_date": "2020-01-02T00:00:00Z",
    "sprint_file_name": "sprint1.csv",
    "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?output=csv",
}

CREATED_COLLS = [
    ".sprints",
    ".comments",
    ".students",
    ".students.sprints",
    ".github.commits",
    ".minutes",
]

MEETING_MINUTES = Minute(
    title="October 24, 1988",
    body="Today we spent time doing nothing. It was a lot of fun and we will do the same tomorrow.",
)

MEETING_MINUTES_JSON = {
    "title": "October 24, 1988",
    "body": "Today we spent time doing nothing. It was a lot of fun and we will do the same tomorrow.",
}

MEETING_MINUTES_TEXT = b"""
    <html>
        <div>
            <div class="tabbed-labels">
                <label>October 24, 1988</label>
                <label>October 25, 1988</label>
            </div>
            <div class="tabbed-content">
                <div class="tabbed-block">
                    <p>Meeting minutes text 1</p>
                </div>
                <div class="tabbed-block">
                    <p>Meeting minutes text 2</p>
                </div>
            </div>
        </div>
    </html>
"""

MEETING_MINUTES_INVALID_DATE_TEXT = b"""
    <html>
        <div>
            <div class="tabbed-labels">
                <label>October 24th/25th, 1988, 2pm/11am</label>
            </div>
            <div class="tabbed-content">
                <div class="tabbed-block">
                    <p>Meeting minutes text 1</p>
                </div>
            </div>
        </div>
    </html>
"""
