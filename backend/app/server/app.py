"""FastAPI app for the capstone dashboard backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from server.config import settings
from server.routes import (
    auth,
    comments,
    courses,
    dataexport,
    forms,
    github,
    minutes,
    students,
)
from server.util.github import get_access_token

app = FastAPI()
app.include_router(auth.router)
app.include_router(github.router)
app.include_router(students.router)
app.include_router(comments.router)
app.include_router(courses.router)
app.include_router(minutes.router)
app.include_router(dataexport.router)
app.include_router(forms.router)

origins = [
    "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def initialize_github_token():
    """Set the global GitHub token."""
    settings.github_token, settings.github_expiration = get_access_token()


@app.on_event("startup")
def startup_db_client():
    """Initialize the MongoDB client."""
    settings.mongodb_client = MongoClient(settings.MONGODB_ADDRESS)
    settings.database = settings.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
def shutdown_db_client():
    """Close the MongoDB client."""
    settings.mongodb_client.close()
