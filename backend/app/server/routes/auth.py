"""API routes for handling Google Authentication."""
from datetime import datetime

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from server.models import models
from server.util import jwt, requests

router = APIRouter()


@router.post(
    "/auth",
    description="verify auth token and user authorization",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "User is authorized"},
        401: {"description": "User is not authorized"},
    },
)
def submit_auth(authreq: models.AuthRequest = Body(...)):
    """Checking User authentication"""
    authreq = jsonable_encoder(authreq)
    try:
        user = requests.get(
            f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={authreq["token"]}'
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    # query db for matching user and check authorization
    user_data = user.json()
    if jwt.valid_email_from_db(user_data["email"]):
        access_token = jwt.create_token(user_data["email"])
        content = JSONResponse(
            {
                "result": True,
                "access_token": access_token,
                "refresh_token": jwt.create_refresh_token(user_data["email"]),
                "email": user_data["email"],
            }
        )
        return content
    raise jwt.CREDENTIALS_EXCEPTION


@router.post("/refresh")
def refresh(refreq: models.RefreshRequest):
    """Check the refresh token for creating new JWT token."""
    try:
        if refreq.grant_type == "refresh_token":
            token = refreq.refresh_token
            payload = jwt.decode_token(token)
            # Check if token is not expired
            if datetime.utcfromtimestamp(payload.get("exp")) > datetime.utcnow():
                email = payload.get("sub")
                # Validate email
                if jwt.valid_email_from_db(email):
                    # Create and return token
                    return JSONResponse(
                        {"result": True, "access_token": jwt.create_token(email)}
                    )

    except Exception as exc:
        raise jwt.CREDENTIALS_EXCEPTION from exc
    raise jwt.CREDENTIALS_EXCEPTION


@router.get("/auth/check", dependencies=[Depends(jwt.get_current_user_email)])
def check_auth():
    """Check if the provided email is authorized."""
    return "Valid"


@router.get("/logout")
def logout(token: str = Depends(jwt.get_current_user_token)):
    """finishing user session"""
    if jwt.add_blacklist_token(token):
        return JSONResponse({"result": True})
    raise jwt.CREDENTIALS_EXCEPTION
