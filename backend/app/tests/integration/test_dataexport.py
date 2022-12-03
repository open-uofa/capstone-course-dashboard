"""Test Fastapi endpoints for data export related routes."""


def test_export_roster_data(client, token):
    """Test exporting roster data."""
    res = client.get(
        "/export/roster/course1", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert (
        res.headers["Content-Disposition"] == "attachment; filename=course1_roster.csv"
    )
    assert res.headers["Access-Control-Expose-Headers"] == "Content-Disposition"


def test_export_roster_data_invalid_course(client, token):
    """Test exporting roster data for a non-existent course."""
    res = client.get(
        "/export/roster/course2", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404


def test_export_roster_data_unauthorized(client):
    """Test exporting roster data without authorization."""
    res = client.get(
        "/export/roster/course1", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_export_sprint_data(client, token):
    """Test exporting sprint data."""
    res = client.get(
        "/export/sprint/course1/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert (
        res.headers["Content-Disposition"]
        == "attachment; filename=course1_sprint_1.csv"
    )
    assert res.headers["Access-Control-Expose-Headers"] == "Content-Disposition"


def test_export_sprint_data_invalid_course(client, token):
    """Test exporting sprint data for a non-existent course."""
    res = client.get(
        "/export/sprint/course2/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404


def test_export_sprint_data_invalid_sprint(client, token):
    """Test exporting sprint data for a non integer invalid sprint parameter."""
    res = client.get(
        "/export/sprint/course1/hello", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 422


def test_export_sprint_data_nonexistent_sprint(client, token):
    """Test exporting sprint data for a non-existent sprint."""
    res = client.get(
        "/export/sprint/course1/0", headers={"Authorization": f"Bearer {token}"}
    )
    # expect 200 OK but csv payload should be an empty file
    assert res.status_code == 200
    assert (
        res.headers["Content-Disposition"]
        == "attachment; filename=course1_sprint_0.csv"
    )
    assert res.headers["Access-Control-Expose-Headers"] == "Content-Disposition"


def test_export_sprint_data_unauthorized(client):
    """Test exporting sprint data without authorization."""
    res = client.get(
        "/export/sprint/course1/1", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}


def test_export_all_data(client, token):
    """Test exporting all data successfully."""
    res = client.get(
        "/export/all/course1", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.headers["Content-Disposition"] == "attachment; filename=course1_all.xlsx"
    assert res.headers["Access-Control-Expose-Headers"] == "Content-Disposition"


def test_export_all_data_invalid_course(client, token):
    """Test exporting all data for a non-existent course."""
    res = client.get(
        "/export/all/course2", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 404


def test_export_all_data_unauthorized(client):
    """Test exporting all data without authorization."""
    res = client.get(
        "/export/all/course1", headers={"Authorization": "Bearer invalid_token"}
    )
    assert res.status_code == 401
    assert res.json() == {"detail": "Could not validate credentials"}
