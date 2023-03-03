"""FastAPI routes for team meeting minutes."""

from typing import List

from bs4 import BeautifulSoup
from dateparser.date import DateDataParser
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from server.config import settings
from server.models.minutes import Minute, MinuteRequest
from server.util import jwt, requests
from server.util.common import check_course_in_db

router = APIRouter()


@router.get(
    "/minutes/{course}/{team}/{sprint}",
    description="Get a list of all meeting minutes for a team. Pass sprint = 0 to get minutes for all sprints.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Meeting minutes are returned successfully"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
    response_model=List[Minute],
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_meeting_minutes(course: str, team: str, sprint: int):
    """Get all meeting minutes for a team."""
    check_course_in_db(course, [".minutes"])

    if sprint == 0:
        # Get all meeting minutes for a team.
        minutes_cur = settings.database[course].minutes.find({"team": team})
    else:
        # First check if sprint exists.
        sprint_dates = settings.database[course].sprints.find_one(
            {"sprint_number": sprint}
        )
        if sprint_dates is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sprint {sprint} does not exist in course {course}",
            )

        minutes_cur = settings.database[course].minutes.find(
            {
                "$and": [
                    {"timestamp": {"$lt": sprint_dates["end_date"]}},
                    {"timestamp": {"$gt": sprint_dates["start_date"]}},
                    {"team": team},
                ]
            }
        )

    minutes = []
    for minute in minutes_cur:
        minutes.append(Minute(**minute))
    return minutes


# pylint: disable=too-many-locals
@router.post(
    "/minutes/{course}/{owner}/{team}",
    description="Fetch and store a team's meeting minutes from MKDocs",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            "description": "The meeting minutes were successfully fetched and stored"
        },
        400: {"description": "Error in parsing the meeting minutes"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def fetch_and_store_meeting_minutes(course: str, owner: str, team: str):
    """Fetch meeting minutes from the MKDocs page and store them into the database."""
    minutes_url = f"https://{owner}.github.io/{team}/meeting-minutes/"

    # Fetch the meeting minutes from the MKDocs page.
    minutes_page = requests.get(minutes_url)
    # Parsing is hardcoded for the current format of our MKDocs page.
    # This needs to be enforced for all teams for the meeting minutes to be fetched successfully.
    # URL format: https://{owner}.github.io/{team}/meeting_minutes/
    # update: 2023-03-03, meeting minutes link is now https://{owner}.github.io/{team}/meeting-minutes/
    # MKDocs format:
    # === "Title for tab, must be some sort of date"
    # Meeting minutes content (can be anything)
    tree = BeautifulSoup(minutes_page.text, "html.parser")
    # stripped_strings returns an iterator, so convert to list for convenience.
    try:
        dates = list(tree.find("div", class_="tabbed-labels").stripped_strings)

        entries = []
        content = tree.find("div", class_="tabbed-content")
        for entry in content.find_all("div", class_="tabbed-block"):
            # Collect the text content of the meeting minute entry.
            entries.append("".join(entry.strings).strip())
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error parsing meeting minutes from MKDocs page: {exc}",
        ) from exc

    # Should correspond one-to-one with dates.
    if len(dates) != len(entries):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The number of dates and entries do not match. Unable to process meeting minutes.",
        )

    check_course_in_db(course, [".minutes"])

    # Fuzzy parse the dates since they may not be in a standard format.
    ddp = DateDataParser(languages=["en"])
    batch_insert = []
    for i, date in enumerate(dates):
        date_data = ddp.get_date_data(date).date_obj
        if date_data is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to parse date {date}",
            )
        batch_insert.append(
            jsonable_encoder(
                MinuteRequest(
                    title=date,
                    body=entries[i],
                    team=team,
                    timestamp=date_data.isoformat(),
                )
            )
        )

    # Replace all information in case changes were made.
    settings.database[course].minutes.delete_many({"team": team})

    # Insert all at once.
    settings.database[course].minutes.insert_many(batch_insert)
