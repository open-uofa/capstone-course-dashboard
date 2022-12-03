"""Backend authentication functions."""

import os
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from server.config import settings


def cast_to_number(var):
    """Helper to read numbers using var envs"""
    temp = os.environ.get(var)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None


# Configuration
API_ALGORITHM = os.environ.get("API_ALGORITHM") or "HS256"
API_ACCESS_TOKEN_EXPIRE_MINUTES = (
    cast_to_number("API_ACCESS_TOKEN_EXPIRE_MINUTES") or 15
)

# Token url (We should later create a token url that accepts just a user and a password to use it with Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/auth")

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Refresh Token
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """Create token internal function."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    if settings.API_SECRET_KEY is None:
        raise BaseException("Missing API_SECRET_KEY env var.")
    encoded_jwt = jwt.encode(
        to_encode, settings.API_SECRET_KEY, algorithm=API_ALGORITHM
    )
    return encoded_jwt


def create_token(email):
    """Create token for an email."""
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return access_token


def valid_email_from_db(email):
    """Check if email is authorized to use the API."""
    associated_user = settings.database["user"].find_one({"email": email})
    if not (associated_user and associated_user["authorized"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return email


def get_current_user_email(token: str = Depends(oauth2_scheme)):
    """Get current user email if it is valid and authorized."""
    if is_token_blacklisted(token):
        raise CREDENTIALS_EXCEPTION
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError as exc:
        raise CREDENTIALS_EXCEPTION from exc

    if valid_email_from_db(email):
        return email

    raise CREDENTIALS_EXCEPTION


def get_current_user_token(token: str = Depends(oauth2_scheme)):
    """Get current user token if the contained email is valid and authorized."""
    _ = get_current_user_email(token)
    return token


def add_blacklist_token(token):
    """Add a token to a blacklist, preventing users from reusing it."""
    settings.database["tokens"].insert_one({"token": token})
    return True


def is_token_blacklisted(token):
    """Check if a token is blacklisted."""
    content = settings.database["tokens"].find_one({"token": token})
    if content and content["token"] == token:
        return True
    return False


def create_refresh_token(email):
    """Create refresh token for an email, useful for when the active token expires."""
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": email}, expires_delta=expires)


def decode_token(token):
    """Decode a JWT token."""
    if settings.API_SECRET_KEY is None:
        raise BaseException("Missing API_SECRET_KEY env var.")
    return jwt.decode(token, settings.API_SECRET_KEY, algorithms=[API_ALGORITHM])
