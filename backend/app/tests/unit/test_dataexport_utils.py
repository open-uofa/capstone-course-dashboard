"""Unit tests for data export util functions"""
from server.util import dataexport
from tests.unit import mock_data


def test_roster_data_to_df(mocker):
    """Test successfully converting roster data to a pandas dataframe."""
    return_df = dataexport.roster_data_to_df(mock_data.STUDENT_ROSTER_RETURN)
    assert return_df.to_dict(orient="list") == mock_data.ROSTER_DF_DICT


def test_sprint_data_to_df(mocker):
    """Test successfully converting sprint data to a pandas dataframe."""
    return_df = dataexport.sprint_data_to_df(
        mock_data.STUDENT_SPRINT_RETURN, mock_data.TEAM_MAP
    )
    assert return_df.to_dict(orient="list") == mock_data.SPRINT_DF_DICT


def test_sprint_data_to_df_student_not_in_teammap(mocker):
    """Test successfully converting sprint data where it encounters a student that doesn't exist in the roster."""
    return_df = dataexport.sprint_data_to_df(mock_data.STUDENT_SPRINT_RETURN, {})
    assert return_df.to_dict(orient="list") == mock_data.SPRINT_DF_DICT_NO_TEAM
