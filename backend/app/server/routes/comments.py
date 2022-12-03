"""FastAPI routes for comments."""

from datetime import datetime, timezone
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from server.config import settings
from server.models.comments import Comment, CommentResponse, UpdateComment
from server.util import jwt
from server.util.common import check_course_in_db

router = APIRouter()


@router.post(
    "/teams/{course_name}/comments",
    description="Add a comment to a team.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "The comment was added successfully"},
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def add_comment(course_name: str, comment: Comment):
    """Add a TA comment for a team into the database."""
    coll = settings.database[course_name].comments
    comment_json = jsonable_encoder(comment)
    # Timestamp the comment.
    comment_json["created_at"] = comment_json["last_modified_at"] = datetime.now(
        timezone.utc
    ).isoformat()
    coll.insert_one(comment_json)


@router.get(
    "/teams/{course_name}/{sprint}/{team}/comments",
    description="Get comments for a team for a specific sprint. Specify sprint 0 to get all sprints",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Comments are returned successfully"},
        404: {"description": "Course, sprint, or team not found"},
    },
    response_model=List[CommentResponse],
    dependencies=[Depends(jwt.get_current_user_email)],
)
def get_comments(course_name: str, sprint: int, team: str):
    """Get all comments for a team for a specific sprint."""
    check_course_in_db(course_name, [".comments", ".sprints"])

    if sprint == 0:
        # Get all comments for a team.
        comments_cur = settings.database[course_name].comments.find({"team": team})
    else:
        # First check if sprint exists.
        verify_sprint = settings.database[course_name].sprints.find_one(
            {"sprint_number": sprint}
        )
        if verify_sprint is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sprint {sprint} does not exist",
            )

        comments_cur = settings.database[course_name].comments.find(
            {"$and": [{"sprint_number": sprint}, {"team": team}]}
        )

    comments = []
    for comment in comments_cur:
        comment_detail = CommentResponse(
            id=str(comment["_id"]),
            message=comment["message"],
            team=comment["team"],
            sprint_number=comment["sprint_number"],
            created_at=comment["created_at"],
            last_modified_at=comment["last_modified_at"],
        )
        comments.append(comment_detail)

    return comments


@router.patch(
    "/teams/{course_name}/comments/{comment_id}",
    description="Edit a comment for a team.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "The comment was edited successfully"},
        400: {"description": "The ID was invalid"},
        404: {"description": "The course or comment was not found"},
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def edit_comment(course_name: str, comment_id: str, comment: UpdateComment):
    """Edit a TA comment for a team in the database."""
    if not ObjectId.is_valid(comment_id):
        raise HTTPException(status_code=400, detail="Invalid comment ID")
    check_course_in_db(course_name, [".comments"])

    comment_json = jsonable_encoder(comment, exclude_none=True)
    # Timestamp the comment update.
    comment_json["last_modified_at"] = datetime.now(timezone.utc).isoformat()

    coll = settings.database[course_name].comments
    res = coll.update_one({"_id": ObjectId(comment_id)}, {"$set": comment_json})
    if res.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )


@router.delete(
    "/teams/{course_name}/comments/{comment_id}",
    description="Delete a comment for a team.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "The comment was deleted successfully"},
        400: {"description": "The ID was invalid"},
        404: {"description": "The course or comment was not found"},
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(jwt.get_current_user_email)],
)
def delete_comment(course_name: str, comment_id: str):
    """Delete a TA comment for a team in the database."""
    if not ObjectId.is_valid(comment_id):
        raise HTTPException(status_code=400, detail="Invalid comment ID")
    check_course_in_db(course_name, [".comments"])

    coll = settings.database[course_name].comments
    res = coll.delete_one({"_id": ObjectId(comment_id)})
    if res.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
