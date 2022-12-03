"""Test FastAPI endpoints for comments-related data."""


def test_get_comments(client, token):
    """Test getting all comments."""
    res = client.get(
        "/teams/course1/0/team1/comments", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == [
        {
            "id": "5f9f1b9b9b9b9b9b9b9b9b9b",
            "message": "Hello, my name is Inigo Montoya.",
            "team": "team1",
            "sprint_number": 2,
            "created_at": "2020-01-01T00:00:00Z",
            "last_modified_at": "2020-01-02T00:00:00Z",
        },
        {
            "id": "5f9f1b9b9b9b9b9b9b9b9b9c",
            "message": "Stop saying that!",
            "team": "team1",
            "sprint_number": 1,
            "created_at": "2020-01-01T00:00:00Z",
            "last_modified_at": "2020-01-02T00:00:00Z",
        },
    ]


def test_get_sprint_comments(client, token):
    """Test getting comments for a specific sprint."""
    res = client.get(
        "/teams/course1/1/team1/comments", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == [
        {
            "id": "5f9f1b9b9b9b9b9b9b9b9b9c",
            "message": "Stop saying that!",
            "team": "team1",
            "sprint_number": 1,
            "created_at": "2020-01-01T00:00:00Z",
            "last_modified_at": "2020-01-02T00:00:00Z",
        }
    ]


def test_get_comments_empty(client, token):
    """Test getting comments for a team with no comments."""
    res = client.get(
        "/teams/course1/0/team2/comments", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == []


def test_get_comments_invalid_sprint(client, token):
    """Test getting comments for a non-existent sprint"""
    res = client.get(
        "/teams/course1/42/team1/comments", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Sprint 42 does not exist"}


def test_get_comments_invalid_course(client, token):
    """Test getting comments for a non-existent course"""
    res = client.get(
        "/teams/course2/0/team1/comments", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course2 does not exist"}


def test_get_comments_unauthorized(client):
    """Test getting comments without being authorized."""
    res = client.get(
        "/teams/course1/0/team1/comments",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_add_comments(client, token):
    """Test adding a comment to the database."""
    res = client.post(
        "/teams/course1/comments",
        json={"message": "As you wish.", "team": "team1", "sprint_number": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204


def test_add_comments_unauthorized(client):
    """Test adding a comment without being authorized."""
    res = client.post(
        "/teams/course1/comments",
        json={"message": "Hello", "team": "team1", "sprint_number": 1},
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_edit_comments(client, token):
    """Test editing a comment in the database."""
    res = client.patch(
        "/teams/course1/comments/5f9f1b9b9b9b9b9b9b9b9b9b",
        json={"message": "As you wish.", "team": "team1", "sprint_number": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204
    # Ensure that it is updated.
    res = client.get(
        "/teams/course1/0/team1/comments", headers={"Authorization": f"Bearer {token}"}
    )
    found = next(
        (
            comment
            for comment in res.json()
            if comment["id"] == "5f9f1b9b9b9b9b9b9b9b9b9b"
            and comment["message"] == "As you wish."
            and comment["team"] == "team1"
        ),
        None,
    )
    assert found is not None


def test_edit_comments_one_field(client, token):
    """Test editing a comment with only one field."""
    res = client.patch(
        "/teams/course1/comments/5f9f1b9b9b9b9b9b9b9b9b9c",
        json={"message": "Stop!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204
    # Ensure that the other fields are not changed.
    res = client.get(
        "/teams/course1/0/team1/comments", headers={"Authorization": f"Bearer {token}"}
    )
    found = next(
        (
            comment
            for comment in res.json()
            if comment["id"] == "5f9f1b9b9b9b9b9b9b9b9b9c"
            and comment["message"] == "Stop!"
            and comment["team"] == "team1"
        ),
        None,
    )
    assert found is not None


def test_edit_comments_invalid_id(client, token):
    """Test editing a comment with an invalid ID."""
    res = client.patch(
        "/teams/course1/comments/invalid_id",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert res.json() == {"detail": "Invalid comment ID"}


def test_edit_comments_invalid_course(client, token):
    """Test editing a comment with an invalid course."""
    res = client.patch(
        "/teams/course42/comments/5f5b5e1b9b9b9b9b9b9b9b9b",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course42 does not exist"}


def test_edit_comments_nonexistent_id(client, token):
    """Test editing a comment with a non-existent ID."""
    res = client.patch(
        "/teams/course1/comments/636007ce4a43dd1082f75464",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Comment not found"}


def test_edit_comments_unauthorized(client):
    """Test editing a comment without being authorized."""
    res = client.patch(
        "/teams/course1/comments/5f9f1b9b9b9b9b9b9b9b9b9b",
        json={"message": "Hello"},
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_delete_comments(client, token):
    """Test deleting a comment from the database."""
    res = client.delete(
        "/teams/course1/comments/5f9f1b9b9b9b9b9b9b9b9b9b",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204
    # Ensure that it is deleted.
    res = client.get(
        "/teams/course1/0/team1/comments", headers={"Authorization": f"Bearer {token}"}
    )
    assert {
        "id": "636007ce4a43dd1082f75464",
        "message": "Hello, my name is Inigo Montoya.",
        "team": "team1",
        "timestamp": "2019-01-01T00:0:00Z",
    } not in res.json()


def test_delete_comments_invalid_id(client, token):
    """Test deleting a comment with an invalid ID."""
    res = client.delete(
        "/teams/course1/comments/invalid_id",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert res.json() == {"detail": "Invalid comment ID"}


def test_delete_comments_invalid_course(client, token):
    """Test deleting a comment with an invalid course."""
    res = client.delete(
        "/teams/course42/comments/5f5b5e1b9b9b9b9b9b9b9b9b",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course course42 does not exist"}


def test_delete_comments_nonexistent_id(client, token):
    """Test deleting a comment with a non-existent ID."""
    res = client.delete(
        "/teams/course1/comments/636007ce4a43dd1082f75464",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Comment not found"}


def test_delete_comments_unauthorized(client):
    """Test deleting a comment without being authorized."""
    res = client.delete(
        "/teams/course1/comments/5f9f1b9b9b9b9b9b9b9b9b9b",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}
