"""FastAPI routes for the capstone dashboard backend."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from server.config import settings
from server.models.github import GithubRequest, StudentCommit, TeamCommit, TeamCommits
from server.util import github, jwt
from server.util.common import check_course_in_db

router = APIRouter()


@router.get(
    "/student/{course_name}/{sprint}/{username}/commits",
    description="Get the number of commits a student has made in a sprint. Pass sprint as 0 to get the total number of commits.",
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Course not found"}},
    response_model=StudentCommit,
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_student_github_commits(course_name: str, sprint: int, username: str):
    """Get the commits for a specific repository."""
    check_course_in_db(course_name, [".sprints", ".github.commits"])

    students_data = settings.database[course_name].github.commits
    if sprint == 0:
        # Get all commits for a student.
        student_commits = students_data.count_documents({"author": username})
    else:
        # Get commits for a student for a specific sprint.
        sprint_dates = settings.database[course_name].sprints.find_one(
            {"sprint_number": sprint}
        )
        if sprint_dates is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sprint {sprint} does not exist",
            )
        student_commits = students_data.count_documents(
            {
                "$and": [
                    {"timestamp": {"$lt": sprint_dates["end_date"]}},
                    {"timestamp": {"$gt": sprint_dates["start_date"]}},
                    {"author": username},
                ]
            }
        )

    return StudentCommit(username=username, number_of_commits=student_commits)


@router.get(
    "/team/{course_name}/{sprint}/commits/{repo}",
    description="Get the number of commits each member of a team has made in a sprint. Pass sprint as 0 to get the total number of commits.",
    response_model=TeamCommits,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Course not found"},
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_team_github_commits(course_name: str, repo: str, sprint: int):
    """Get the commits for a specific repository."""
    check_course_in_db(course_name, [".sprints", ".github.commits", ".students"])

    team_data = settings.database[course_name].github.commits
    authors = set()
    authors.update(
        settings.database[course_name].students.distinct(
            "source_control_username", {"repo_name": repo}
        )
    )
    # We don't technically need to add the authors from the github.commits collection,
    # but since we don't have real importable user data associated with GitHub commits, we'll
    # just add them here to make sure we get all the authors.
    authors.update(
        settings.database[course_name].github.commits.distinct(
            "author", {"repo_name": repo}
        )
    )
    student_commits = []

    if sprint == 0:
        # Get all commits for a team.
        for author in authors:
            count = team_data.count_documents(
                {"$and": [{"author": author}, {"repo_name": repo}]}
            )
            student_commits.append(
                StudentCommit(username=author, number_of_commits=count)
            )
    else:
        # Get commits for a team for a specific sprint.
        sprint_dates = settings.database[course_name].sprints.find_one(
            {"sprint_number": sprint}
        )
        if sprint_dates is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sprint {sprint} does not exist",
            )
        for author in authors:
            count = team_data.count_documents(
                {
                    "$and": [
                        {"timestamp": {"$lt": sprint_dates["end_date"]}},
                        {"timestamp": {"$gt": sprint_dates["start_date"]}},
                        {"author": author},
                        {"repo_name": repo},
                    ]
                }
            )
            student_commits.append(
                StudentCommit(username=author, number_of_commits=count)
            )

    # Return the date that the team's commits were last updated. (Sprint is irrelevant here)
    # Note: aggregate returns a cursor.
    last_fetched_at_cur = settings.database[course_name].github.commits.aggregate(
        [
            {"$match": {"repo_name": repo}},
            {"$sort": {"fetched_at": -1}},
            {"$limit": 1},
        ]
    )
    # We are guaranteed to only have one item due to limit being 1.
    try:
        last_fetched_at = next(last_fetched_at_cur)["fetched_at"]
    except StopIteration:
        last_fetched_at = None
    return TeamCommits(student_commits=student_commits, last_fetched_at=last_fetched_at)


@router.get(
    "/class/{course_name}/{sprint}/commits",
    description="Get the number of commits each team has made in a sprint. Pass sprint as 0 to get the total number of commits.",
    response_model=List[TeamCommit],
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Course not found"},
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_teams_github_commits(course_name: str, sprint: int):
    """Get each team's number of commits."""
    check_course_in_db(course_name, [".sprints", ".github.commits", ".students"])

    repos = set()
    repos.update(settings.database[course_name].students.distinct("repo_name"))
    # We don't technically need to add the teams from the github.commits collection,
    # but since we don't have real importable team data associated with GitHub commits, we'll
    # just add them here to make sure we get all the teams.
    repos.update(settings.database[course_name].github.commits.distinct("repo_name"))
    team_commits = []

    if sprint == 0:
        # Get all commits for a team.
        for repo in repos:
            count = settings.database[course_name].github.commits.count_documents(
                {"$and": [{"repo_name": repo}]}
            )
            team_commits.append(TeamCommit(team_name=repo, number_of_commits=count))
    else:
        # Get commits for a team for a specific sprint.
        sprint_dates = settings.database[course_name].sprints.find_one(
            {"sprint_number": sprint}
        )
        if sprint_dates is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sprint {sprint} does not exist",
            )

        for repo in repos:
            count = settings.database[course_name].github.commits.count_documents(
                {
                    "$and": [
                        {"timestamp": {"$lt": sprint_dates["end_date"]}},
                        {"timestamp": {"$gt": sprint_dates["start_date"]}},
                        {"repo_name": repo},
                    ]
                }
            )
            team_commits.append(TeamCommit(team_name=repo, number_of_commits=count))

    return team_commits


@router.post(
    "/github",
    description="Fetch and store GitHub commits",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "The data was fetched and stored successfully"},
        400: {"description": "The request was invalid"},
        401: {"description": "User is not authorized"},
        404: {"description": "Not found"},
        409: {"description": "Conflict error"},
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def fetch_and_store_github_commits(request: GithubRequest):
    """Fetch and store the GitHub commits."""
    new_commits = github.get_new_commits(
        request.owner, request.repo, request.course_name
    )
    github.store_commits(new_commits, request.repo, request.course_name)
