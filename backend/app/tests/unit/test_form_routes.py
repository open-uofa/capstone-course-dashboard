"""Unit tests for the form routes."""

from server.routes import forms
from tests.unit import mock_data


def test_get_form(mocker):
    """Test successfully get link from the database."""
    mock_check_course_in_db = mocker.patch("server.routes.forms.check_course_in_db")
    mock_form = mocker.patch(
        "pymongo.collection.Collection.find_one",
        return_value=mock_data.FORM,
    )
    link = forms.get_forms("test_course", 1)
    mock_check_course_in_db.assert_called_once()
    mock_form.assert_called_once()
    assert link == mock_data.LINK
