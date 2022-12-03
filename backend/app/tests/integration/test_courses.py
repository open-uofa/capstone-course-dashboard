"""Test FastAPI endpoints for courses-related data."""


def test_get_courses(client, token):
    """Test getting a list of all courses."""
    res = client.get("/courses", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json() == [
        {
            "name": "course1",
            "roster_file_name": "roster1.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        {
            "name": "course2",
            "roster_file_name": "roster2.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
    ]


def test_get_courses_unauthorized(client):
    """Test getting a list of all courses without authorization."""
    res = client.get("/courses", headers={"Authorization": "Bearer invalid_token"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_get_courses_for_user(client, token):
    """Test getting a list of all courses for a user."""
    res = client.get(
        "/courses/admin@gmail.com", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == [
        {
            "name": "course1",
            "roster_file_name": "roster1.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        }
    ]


def test_get_courses_for_user_unauthorized(client):
    """Test getting a list of all courses for a user without authorization."""
    res = client.get(
        "/courses/admin@gmail.com", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_create_course(client, token):
    """Test creating a new course."""
    res = client.post(
        "/courses",
        json={
            "name": "course3",
            "roster_file_name": "roster3.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204


def test_create_course_invalid(client, token):
    """Test creating a new course with invalid data."""
    res = client.post(
        "/courses",
        json={"name": "course3"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422


def test_create_course_already_exists(client, token):
    """Test creating a new course that already exists."""
    res = client.post(
        "/courses",
        json={
            "name": "course1",
            "roster_file_name": "roster1.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert res.json() == {"detail": "Course course1 already exists"}


def test_create_course_unauthorized(client):
    """Test creating a new course without authorization."""
    res = client.post(
        "/courses",
        json={
            "name": "course3",
            "roster_file_name": "roster3.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_delete_course(client, token):
    """Test deleting a course. Dependent on the create course tests running first."""
    res = client.delete(
        "/courses/course3", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 204


def test_delete_course_invalid(client, token):
    """Test deleting a non-existent course."""
    res = client.delete(
        "/courses/invalid_course", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course invalid_course does not exist"}


def test_delete_course_unauthorized(client):
    """Test deleting a course without authorization."""
    res = client.delete(
        "/courses/course3", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_delete_course_unassigned_user(client, token_no_courses):
    """Test deleting a course that the user is not assigned to."""
    res = client.delete(
        "/courses/course1", headers={"Authorization": f"Bearer {token_no_courses}"}
    )
    assert res.status_code == 401
    assert res.json() == {
        "detail": "User test_email2@gmail.com is not authorized to access course1"
    }


def test_get_sprints(client, token):
    """Test getting a list of all sprints for a course."""
    res = client.get(
        "/courses/course1/sprints", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json() == [
        {
            "sprint_number": 1,
            "start_date": "2020-01-01T00:00:00Z",
            "end_date": "2020-01-29T00:00:00Z",
            "sprint_file_name": "sprint1.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?output=csv",
        },
        {
            "sprint_number": 2,
            "start_date": "2020-02-01T00:00:00Z",
            "end_date": "2020-02-28T00:00:00Z",
            "sprint_file_name": "sprint2.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?output=csv",
        },
    ]


def test_get_sprints_invalid_course(client, token):
    """Test getting a list of all sprints for a non-existent course."""
    res = client.get(
        "/courses/invalid_course/sprints", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course invalid_course does not exist"}


def test_get_sprints_unauthorized(client):
    """Test getting a list of all sprints for a course without authorization."""
    res = client.get(
        "/courses/course1/sprints", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_get_sprints_user_unassigned(client, token_no_courses):
    """Test getting a list of all sprints for a course that the user is not assigned to."""
    res = client.get(
        "/courses/course1/sprints",
        headers={"Authorization": f"Bearer {token_no_courses}"},
    )
    assert res.status_code == 401
    assert res.json() == {
        "detail": "User test_email2@gmail.com is not authorized to access course1"
    }


def test_create_sprint(client, token):
    """Test creating a new sprint for a course."""
    res = client.post(
        "/courses/course1/sprints",
        json={
            "sprint_number": 3,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint3.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204


def test_create_sprint_invalid(client, token):
    """Test creating a new sprint for a course with invalid data."""
    res = client.post(
        "/courses/course1/sprints",
        json={
            "sprint_number": 3,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint3.csv",
            # missing forms_url field
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422


def test_create_sprint_invalid_course(client, token):
    """Test creating a new sprint for a non-existent course."""
    res = client.post(
        "/courses/invalid_course/sprints",
        json={
            "sprint_number": 3,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint3.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course invalid_course does not exist"}


def test_create_sprint_already_exists(client, token):
    """Test creating a new sprint that already exists."""
    res = client.post(
        "/courses/course1/sprints",
        json={
            "sprint_number": 1,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint3.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 400
    assert res.json() == {"detail": "Sprint 1 already exists"}


def test_create_sprint_unauthorized(client):
    """Test creating a new sprint for a course without authorization."""
    res = client.post(
        "/courses/course1/sprints",
        json={
            "sprint_number": 3,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint3.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_create_sprint_user_unassigned(client, token_no_courses):
    """Test creating a new sprint for a course that the user is not assigned to."""
    res = client.post(
        "/courses/course1/sprints",
        json={
            "sprint_number": 3,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint3.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": f"Bearer {token_no_courses}"},
    )
    assert res.status_code == 401
    assert res.json() == {
        "detail": "User test_email2@gmail.com is not authorized to access course1"
    }


def test_delete_sprint(client, token):
    """Test deleting a sprint for a course. Dependent on the create sprint tests running first."""
    res = client.delete(
        "/courses/course1/sprints/3", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 204


def test_delete_sprint_invalid_course(client, token):
    """Test deleting a sprint for a non-existent course."""
    res = client.delete(
        "/courses/invalid_course/sprints/3",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course invalid_course does not exist"}


def test_delete_sprint_invalid_sprint(client, token):
    """Test deleting a non-existent sprint for a course."""
    res = client.delete(
        "/courses/course1/sprints/3", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Sprint not found"}


def test_delete_sprint_unauthorized(client):
    """Test deleting a sprint for a course without authorization."""
    res = client.delete(
        "/courses/course1/sprints/3", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_delete_sprint_user_unassigned(client, token_no_courses):
    """Test deleting a sprint for a course that the user is not assigned to."""
    res = client.delete(
        "/courses/course1/sprints/3",
        headers={"Authorization": f"Bearer {token_no_courses}"},
    )
    assert res.status_code == 401
    assert res.json() == {
        "detail": "User test_email2@gmail.com is not authorized to access course1"
    }


def test_update_course(client, token):
    """Test updating a course. Dependent on the create course tests running first."""
    res = client.put(
        "/courses",
        json={
            "name": "course1",
            "roster_file_name": "roster1_new.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204


def test_update_course_invalid_course(client, token):
    """Test updating a non-existent course."""
    res = client.put(
        "/courses",
        json={
            "name": "invalid_course",
            "roster_file_name": "roster3_new.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course invalid_course does not exist"}


def test_update_course_unauthorized(client):
    """Test updating a course without authorization."""
    res = client.put(
        "/courses",
        json={
            "name": "course1",
            "roster_file_name": "roster1_new.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_update_course_user_unassigned(client, token_no_courses):
    """Test updating a course that the user is not assigned to."""
    res = client.put(
        "/courses",
        json={
            "name": "course1",
            "roster_file_name": "roster1_new.csv",
            "use_github": True,
            "use_student_experience_form": True,
            "use_team_structure": True,
        },
        headers={"Authorization": f"Bearer {token_no_courses}"},
    )
    assert res.status_code == 401
    assert res.json() == {
        "detail": "User test_email2@gmail.com is not authorized to access course1"
    }


def test_update_course_invalid_json(client, token):
    """Test updating a course with invalid json."""
    res = client.put(
        "/courses",
        json={"invalid": "json"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422


def test_update_sprint(client, token):
    """Test updating a sprint for a course."""
    res = client.put(
        "/courses/course1/sprints",
        json={
            "sprint_number": 2,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint2_new.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 204


def test_update_sprint_invalid_course(client, token):
    """Test updating a sprint for a non-existent course."""
    res = client.put(
        "/courses/invalid_course/sprints",
        json={
            "sprint_number": 2,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint2_new.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Course invalid_course does not exist"}


def test_update_sprint_invalid_sprint(client, token):
    """Test updating a non-existent sprint for a course."""
    res = client.put(
        "/courses/course1/sprints",
        json={
            "sprint_number": 3,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint3_new.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 404
    assert res.json() == {"detail": "Sprint 3 does not exist"}


def test_update_sprint_unauthorized(client):
    """Test updating a sprint for a course without authorization."""
    res = client.put(
        "/courses/course1/sprints",
        json={
            "sprint_number": 2,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint2_new.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_update_sprint_user_unassigned(client, token_no_courses):
    """Test updating a sprint for a course that the user is not assigned to."""
    res = client.put(
        "/courses/course1/sprints",
        json={
            "sprint_number": 2,
            "start_date": "2020-03-01T00:00:00Z",
            "end_date": "2020-03-29T00:00:00Z",
            "sprint_file_name": "sprint2_new.csv",
            "forms_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQdIq-kg20x4kWwwfOFsc3xQotiAg_vZI5qfK0PBcHIs0CEv56s-v9Q-_SeiP1xGWcjBKjrNjxo16-B/pub?outpost=csv",
        },
        headers={"Authorization": f"Bearer {token_no_courses}"},
    )
    assert res.status_code == 401
    assert res.json() == {
        "detail": "User test_email2@gmail.com is not authorized to access course1"
    }


def test_update_sprint_invalid_json(client, token):
    """Test updating a sprint for a course with invalid json."""
    res = client.put(
        "/courses/course1/sprints",
        json={"invalid": "json"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422
