"""Wrapper for Python requests that allows us to raise errors automatically."""
import json

import requests
from fastapi import HTTPException

from server.config import settings


def make_request(method, *args, **kwargs):
    """Make a request with the given method."""
    func = getattr(requests, method)
    res = func(*args, **kwargs, timeout=settings.HTTP_TIMEOUT)
    try:
        # Raises an exception if the response is not 200.
        res.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        # Try to format the error message as JSON, otherwise just use the text.
        try:
            detail = json.loads(res.text)
        except json.decoder.JSONDecodeError:
            detail = res.text
        # Raise HTTPException so FastAPI displays the error message nicely.
        raise HTTPException(status_code=res.status_code, detail=detail) from exc
    return res


def get(*args, **kwargs):
    """Wrapped requests.get function."""
    return make_request("get", *args, **kwargs)


def post(*args, **kwargs):
    """Wrapped requests.post function."""
    return make_request("post", *args, **kwargs)


def put(*args, **kwargs):
    """Wrapped requests.put function."""
    return make_request("put", *args, **kwargs)


def delete(*args, **kwargs):
    """Wrapped requests.delete function."""
    return make_request("delete", *args, **kwargs)


def patch(*args, **kwargs):
    """Wrapped requests.patch function."""
    return make_request("patch", *args, **kwargs)
