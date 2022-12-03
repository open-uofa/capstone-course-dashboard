"""Unit tests for data export routes."""
import pandas as pd

from server.routes import dataexport
from tests.unit import mock_data


def test_export_roster_data(mocker):
    """Test exporting roster data."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.dataexport.check_course_in_db"
    )
    mock_roster_data_to_df = mocker.patch(
        "server.routes.dataexport.roster_data_to_df",
        return_value=pd.DataFrame(mock_data.ROSTER_DF_DICT),
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find",
        return_value=[dict(mock_data.STUDENT_ROSTER_RETURN[0])],
    )

    dataexport.export_roster_data("course1")
    mock_check_course_in_db.assert_called_once()
    mock_roster_data_to_df.assert_called_once_with(mock_data.STUDENT_ROSTER_RETURN)
    mock_find.assert_called_once()


def test_export_sprint_data(mocker):
    """Test exporting sprint data."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.dataexport.check_course_in_db"
    )
    mock_sprint_data_to_df = mocker.patch(
        "server.routes.dataexport.sprint_data_to_df",
        return_value=pd.DataFrame(mock_data.SPRINT_DF_DICT),
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find",
        side_effect=[
            [dict(mock_data.STUDENT_SPRINT_RETURN[0])],
            [dict(mock_data.STUDENT_ROSTER_RETURN[0])],
        ],
    )

    dataexport.export_sprint_data("course1", 1)
    mock_check_course_in_db.assert_called_once()
    mock_sprint_data_to_df.assert_called_once_with(
        mock_data.STUDENT_SPRINT_RETURN, mock_data.TEAM_MAP
    )
    assert mock_find.call_count == 2


def test_export_all_data(mocker):
    """Test exporting all data to an excel workbook."""
    mock_check_course_in_db = mocker.patch(
        "server.routes.dataexport.check_course_in_db"
    )
    mock_get_sprint_list = mocker.patch(
        "server.routes.dataexport.get_sprint_list",
        return_value=[1],
    )
    mock_roster_data_to_df = mocker.patch(
        "server.routes.dataexport.roster_data_to_df",
        return_value=pd.DataFrame(mock_data.ROSTER_DF_DICT),
    )
    mock_sprint_data_to_df = mocker.patch(
        "server.routes.dataexport.sprint_data_to_df",
        return_value=pd.DataFrame(mock_data.SPRINT_DF_DICT),
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find",
        side_effect=[
            [dict(mock_data.STUDENT_ROSTER_RETURN[0])],
            [dict(mock_data.STUDENT_SPRINT_RETURN[0])],
        ],
    )

    dataexport.export_all_data("course1")
    mock_check_course_in_db.assert_called_once()
    mock_get_sprint_list.assert_called_once()
    mock_roster_data_to_df.assert_called_once_with(mock_data.STUDENT_ROSTER_RETURN)
    mock_sprint_data_to_df.assert_called_once_with(
        mock_data.STUDENT_SPRINT_RETURN, mock_data.TEAM_MAP
    )
    assert mock_find.call_count == 2


def test_export_all_data_no_sprints(mocker):
    """
    Test exporting all data when there are no sprints.
    The xslx should only contain a roster sheet.
    """
    mock_check_course_in_db = mocker.patch(
        "server.routes.dataexport.check_course_in_db"
    )
    mock_get_sprint_list = mocker.patch(
        "server.routes.dataexport.get_sprint_list",
        return_value=[],  # no sprints
    )
    mock_roster_data_to_df = mocker.patch(
        "server.routes.dataexport.roster_data_to_df",
        return_value=pd.DataFrame(mock_data.ROSTER_DF_DICT),
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find",
        return_value=[dict(mock_data.STUDENT_ROSTER_RETURN[0])],
    )

    dataexport.export_all_data("course1")
    mock_check_course_in_db.assert_called_once()
    mock_get_sprint_list.assert_called_once()
    mock_roster_data_to_df.assert_called_once_with(mock_data.STUDENT_ROSTER_RETURN)
    mock_find.assert_called_once()


def test_export_all_data_no_roster(mocker):
    """
    Test exporting all data when there is no roster.
    The roster sheet is expected to be empty and the team fields in the sprint sheet will be
    "This student does not appear in the roster.".
    """
    mock_check_course_in_db = mocker.patch(
        "server.routes.dataexport.check_course_in_db"
    )
    mock_get_sprint_list = mocker.patch(
        "server.routes.dataexport.get_sprint_list",
        return_value=[1],
    )
    mock_sprint_data_to_df = mocker.patch(
        "server.routes.dataexport.sprint_data_to_df",
        return_value=pd.DataFrame(mock_data.SPRINT_DF_DICT),
    )
    mock_find = mocker.patch(
        "pymongo.collection.Collection.find",
        side_effect=[
            [],  # no roster
            [dict(mock_data.STUDENT_SPRINT_RETURN[0])],
        ],
    )

    dataexport.export_all_data("course1")
    mock_check_course_in_db.assert_called_once()
    mock_get_sprint_list.assert_called_once()
    mock_sprint_data_to_df.assert_called_once_with(mock_data.STUDENT_SPRINT_RETURN, {})
    assert mock_find.call_count == 2
