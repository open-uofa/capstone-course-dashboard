"""
Utils for student endpoints and related tasks.
These functions are tightly related to those in
the util/dataexport.py module. Changes here should
be reflected there and vice versa with the goal
of keeping files exported compatible with being
imported without modification.

Ideally only this and the dataexport.py module should have to be modified
to add new data formats or support new file types.
"""
import pandas as pd

from server.models.students import Student, StudentSprintData


def parse_roster_data(file, coursename):
    """
    parse student data from csv file
    file is a python file-like object
    returns a list of student data objects
    """
    roster_df = pd.read_csv(file)
    # theres a strange issue where using pd.read_csv on some file objects, remove this check if thats not the case from frontend
    if roster_df.columns[0] != "Email Address":
        roster_df.rename(columns={roster_df.columns[0]: "Email Address"}, inplace=True)
        print(
            roster_df.columns,
            "pandas misinterpreted the passed file object or your first column is not named 'Email Address'",
        )
    # fill empty values with empty string
    roster_df.fillna("", inplace=True)
    # just grab the data needed for each student object from the dataframe
    student_list = []
    for _, row in roster_df.iterrows():
        student_list.append(
            Student(
                email=row["Email Address"],
                full_name=row["Full name (preferred)"],
                source_control_username=row["Github Account"],
                project=row["Project"],
                repo_name=row["Github repo"],
                ta=row["TA"],
                course_name=coursename,
                form_submitted=False,
                experience_survey={
                    "course_work": row["Coursework"],
                    "langs": row[
                        "Please describe your experience with other languages and development tools"
                    ],
                    "hopes": row[
                        "What do you hope to get out of your CMPUT 401 experience?"
                    ],
                    "diffs": row[
                        "Do you expect CMPUT 401 to be any different than your prior courses? If so, how?"
                    ],
                    "experience": row["Experience"],
                },
            )
        )

    return student_list


def parse_sprint_data(file, sprint):
    """
    parse sprint data from csv file
    file is a python file-like object
    returns a list of sprint data objects

    extremely hardcoded atm, a more flexible solution would be nice
    otherwise replace this function to support new formats
    """
    sprint_df = pd.read_csv(file)
    # theres a strange issue where using pd.read_csv on some file objects, remove this check if thats not the case from frontend
    if sprint_df.columns[1] != "Email Address":
        sprint_df.rename(columns={sprint_df.columns[1]: "Email Address"}, inplace=True)
        print(
            sprint_df.columns,
            "pandas misinterpreted the passed file object or your second column is not named 'Email Address'",
        )
    # get the data not related to other students
    personal_data = pd.concat([sprint_df.iloc[:, [1]], sprint_df.iloc[:, 3:19]], axis=1)
    personal_data.fillna("", inplace=True)
    # get the data related to other students (ie ratings and feedback)
    peer_ratings = pd.concat([sprint_df.iloc[:, [1]], sprint_df.iloc[:, 19:]], axis=1)
    # below is mostly adapted from the provided jupyter aggregation script
    # Renaming columns
    for i in range(0, 6):
        peer_ratings.rename(
            columns={peer_ratings.columns[1 + (i * 3)]: f"student_{i}"}, inplace=True
        )
        peer_ratings.rename(
            columns={peer_ratings.columns[1 + (i * 3) + 2]: f"feedback_{i}"},
            inplace=True,
        )
        peer_ratings.rename(
            columns={peer_ratings.columns[1 + (i * 3) + 1]: f"score_{i}"}, inplace=True
        )
    # convert ratings to numbers
    mapping = {
        "most valuable team member": 4,
        "contributed substantially": 3,
        "did ok": 2,
        "did not do enough": 1,
        "did practically nothing": 0,
    }
    peer_ratings[
        ["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]
    ] = peer_ratings[
        ["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]
    ].applymap(
        lambda s: mapping.get(s) if s in mapping else s
    )
    peer_ratings[
        ["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]
    ] = peer_ratings[
        ["score_0", "score_1", "score_2", "score_3", "score_4", "score_5"]
    ].apply(
        pd.to_numeric, errors="coerce"
    )

    # Combine students and scores into their own columns
    feedback_df = pd.DataFrame(
        {
            "Student": pd.concat(
                [
                    peer_ratings["student_0"],
                    peer_ratings["student_1"],
                    peer_ratings["student_2"],
                    peer_ratings["student_3"],
                    peer_ratings["student_4"],
                    peer_ratings["student_5"],
                ],
                axis=0,
            ),
            "Score": pd.concat(
                [
                    peer_ratings["score_0"],
                    peer_ratings["score_1"],
                    peer_ratings["score_2"],
                    peer_ratings["score_3"],
                    peer_ratings["score_4"],
                    peer_ratings["score_5"],
                ],
                axis=0,
            ),
        }
    )

    # Grouping, sorting
    # get avg and std deviation of scores per student
    feedback_df = feedback_df.groupby("Student").agg({"Score": ["mean", "std"]})
    feedback_df.columns = ["Score_Mean", "Score_Std"]
    # get all emails of students who received a review
    # accepts "email - name" and "name - email" formats
    emails = pd.Series(
        [
            email.split()[2] if email.split()[0].find("@") == -1 else email.split()[0]
            for email in feedback_df.index
        ]
    )
    feedback_df.set_index(emails, inplace=True)
    feedback_df.fillna(0, inplace=True)

    # Associate student with their feedback
    for i in range(0, 6):
        peer_ratings[f"score_{i}"].fillna("", inplace=True)
        peer_ratings[f"student_{i}"].fillna("", inplace=True)
    # peer ratings are associated with the student receiving the rating and include the student who gave the rating
    received_feedback = {}
    for _, row in peer_ratings.iterrows():
        for i in range(0, 6):
            if row[f"student_{i}"] != "":
                email_idx = (
                    row[f"student_{i}"].split()[2]
                    if row[f"student_{i}"].split()[0].find("@") == -1
                    else row[f"student_{i}"].split()[0]
                )
                try:
                    received_feedback[email_idx][row.iloc[0]] = {
                        "rating": row[f"score_{i}"],
                        "what_did_they_do": row[f"feedback_{i}"],
                    }
                except KeyError:
                    received_feedback[email_idx] = {}
                    received_feedback[email_idx][row.iloc[0]] = {
                        "rating": row[f"score_{i}"],
                        "what_did_they_do": row[f"feedback_{i}"],
                    }

    # create and return sprint data objects
    sprint_data = []
    submitted_emails = set()
    for _, row in personal_data.iterrows():
        if row["Email Address"] != "":
            submitted_emails.add(row["Email Address"])
            sprint_data.append(
                StudentSprintData(
                    email=row["Email Address"],
                    sprint=sprint,
                    personal_peer_rev={
                        "meeting_participation": row.iloc[1],
                        "meeting_content": row.iloc[2],
                        "missed_meetings": row.iloc[3],
                        "project_appropriate": row.iloc[4],
                        "confident_to_learn_sd": row.iloc[5],
                        "capable_to_learn_sd": row.iloc[6],
                        "able_to_achieve_learning_goals": row.iloc[7],
                        "able_to_meet_sd_challenge": row.iloc[8],
                        "students_care": row.iloc[9],
                        "connected_with_others": row.iloc[10],
                        "hard_to_get_help": row.iloc[11],
                        "uneasy_exposing_gaps": row.iloc[12],
                        "reluctant_to_speak_openly": row.iloc[13],
                        "can_rely_on_others": row.iloc[14],
                        "given_opportunities_to_learn": row.iloc[15],
                        "confident_others_will_support_me": row.iloc[16],
                    },
                    received_peer_revs=received_feedback[row["Email Address"]],
                    avg_rating=feedback_df.loc[row["Email Address"]]["Score_Mean"],
                    stddev_rating=feedback_df.loc[row["Email Address"]]["Score_Std"],
                )
            )
    # add students who did not submit a peer review but were reviewed
    emails = set(emails).difference(submitted_emails)
    for email in emails:
        sprint_data.append(
            StudentSprintData(
                email=email,
                sprint=sprint,
                personal_peer_rev={
                    "meeting_participation": "Peer review was not sumitted.",
                    "meeting_content": "Peer review was not sumitted.",
                    "missed_meetings": "Peer review was not sumitted.",
                    "project_appropriate": "Peer review was not sumitted.",
                    "confident_to_learn_sd": "Peer review was not sumitted.",
                    "capable_to_learn_sd": "Peer review was not sumitted.",
                    "able_to_achieve_learning_goals": "Peer review was not sumitted.",
                    "able_to_meet_sd_challenge": "Peer review was not sumitted.",
                    "students_care": "Peer review was not sumitted.",
                    "connected_with_others": "Peer review was not sumitted.",
                    "hard_to_get_help": "Peer review was not sumitted.",
                    "uneasy_exposing_gaps": "Peer review was not sumitted.",
                    "reluctant_to_speak_openly": "Peer review was not sumitted.",
                    "can_rely_on_others": "Peer review was not sumitted.",
                    "given_opportunities_to_learn": "Peer review was not sumitted.",
                    "confident_others_will_support_me": "Peer review was not sumitted.",
                },
                received_peer_revs=received_feedback[email],
                avg_rating=feedback_df.loc[email]["Score_Mean"],
                stddev_rating=feedback_df.loc[email]["Score_Std"],
            )
        )
    return sprint_data
