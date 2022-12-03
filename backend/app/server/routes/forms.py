"""FastAPI routes for forms."""

from fastapi import APIRouter, Depends, status

from server.config import settings
from server.util import jwt
from server.util.common import check_course_in_db

router = APIRouter()


@router.get(
    "/form/{course_name}/{sprint}",
    description="Get review forms info",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "form is returned successfully"}},
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_forms(course_name: str, sprint: int):
    """Get form"""
    check_course_in_db(course_name, [".sprints"])
    link = None
    if sprint > 0:
        coll = settings.database[course_name].sprints.find_one(
            {"sprint_number": sprint}
        )
        link = coll["forms_url"]
    return link
