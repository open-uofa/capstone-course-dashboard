"""
Utils for data export endpoints and related tasks.
These functions are tightly related to those in
the util/students.py module. Changes here should
be reflected there and vice versa with the goal
of keeping files exported compatible with being
imported without modification.

Subsequently, if different formats are needed
only this and the students.py module should be modified
or added to.
"""
from collections import OrderedDict

import pandas as pd


def roster_data_to_df(docs):
    """
    Convert a list of Student objects to a pandas dataframe.
    Resulting dfs should be compatible with the import format
    when converted to csv.
    """
    # spreadsheet column names
    col_names = [
        "Email Address",
        "Full name (preferred)",
        "Github Account",
        "Project",
        "Github repo",
        "TA",
        "Coursework",
        "Please describe your experience with other languages and development tools",
        "What do you hope to get out of your CMPUT 401 experience?",
        "Do you expect CMPUT 401 to be any different than your prior courses? If so, how?",
        "Experience",
    ]
    # map from spreadsheet column names to Student model attributes
    col_to_model_map = {
        "Email Address": "email",
        "Full name (preferred)": "full_name",
        "Github Account": "source_control_username",
        "Project": "project",
        "Github repo": "repo_name",
        "TA": "ta",
        "Coursework": "course_work",
        "Please describe your experience with other languages and development tools": "langs",
        "What do you hope to get out of your CMPUT 401 experience?": "hopes",
        "Do you expect CMPUT 401 to be any different than your prior courses? If so, how?": "diffs",
        "Experience": "experience",
    }
    roster_dict = OrderedDict()
    for doc in docs:
        # get flat data from doc to dict
        for i in range(6):
            try:
                roster_dict[col_names[i]].append(
                    getattr(doc, col_to_model_map[col_names[i]])
                )
            except KeyError:
                roster_dict[col_names[i]] = [
                    getattr(doc, col_to_model_map[col_names[i]]),
                ]
        # get survey data from doc to dict
        for i in range(6, 11):
            try:
                roster_dict[col_names[i]].append(
                    doc.experience_survey[col_to_model_map[col_names[i]]]
                )
            except KeyError:
                roster_dict[col_names[i]] = [
                    doc.experience_survey[col_to_model_map[col_names[i]]],
                ]
    roster_df = pd.DataFrame(roster_dict)

    return roster_df


def sprint_data_to_df(docs, team_map):
    """
    Convert a list of StudentSprintData objects to a pandas dataframe.
    Resulting dfs should be compatible with the import format
    when converted to csv.
    """
    personal_pr_col_names = [
        "In how many meetings did you participate during this past sprint?",
        "What was discussed/decided in these meetings?",
        "Were there other team meetings that you missed?",
        "Do you think that this project is appropriate (in complexity and scope) for the course?",
        "Please respond to each of the following items in terms of how true it is for you with respect to your learning software development through this sprint [I feel confident in my ability to learn software development]",
        "Please respond to each of the following items in terms of how true it is for you with respect to your learning software development through this sprint [I am capable of learning software development]",
        "Please respond to each of the following items in terms of how true it is for you with respect to your learning software development through this sprint [I am able to achieve my software development learning goals]",
        "Please respond to each of the following items in terms of how true it is for you with respect to your learning software development through this sprint [I feel able to meet the challenge of performing well when developing software.]",
        "I feel that students in this course care about each other",
        "I feel connected to others in this course",
        "I feel that it is hard to get help when I have a question",
        "I feel uneasy exposing gaps in my understanding",
        "I feel reluctant to speak openly",
        "I feel that I can rely on others in this course",
        "I feel that I am given ample opportunities to learn",
        "I feel confident that others will support me",
    ]
    peer_rev_col_names = [
        "Choose a team member-",
        "How would you rate their contribution?",
        "Please provide your reasons for this rating and share more details about their contribution.",
    ]
    col_to_model_map = {
        personal_pr_col_names[0]: "meeting_participation",
        personal_pr_col_names[1]: "meeting_content",
        personal_pr_col_names[2]: "missed_meetings",
        personal_pr_col_names[3]: "project_appropriate",
        personal_pr_col_names[4]: "confident_to_learn_sd",
        personal_pr_col_names[5]: "capable_to_learn_sd",
        personal_pr_col_names[6]: "able_to_achieve_learning_goals",
        personal_pr_col_names[7]: "able_to_meet_sd_challenge",
        personal_pr_col_names[8]: "students_care",
        personal_pr_col_names[9]: "connected_with_others",
        personal_pr_col_names[10]: "hard_to_get_help",
        personal_pr_col_names[11]: "uneasy_exposing_gaps",
        personal_pr_col_names[12]: "reluctant_to_speak_openly",
        personal_pr_col_names[13]: "can_rely_on_others",
        personal_pr_col_names[14]: "given_opportunities_to_learn",
        personal_pr_col_names[15]: "confident_others_will_support_me",
    }
    count = 0
    sprint_dict = OrderedDict()
    for doc in docs:
        # get email and team data into dict
        # col one needs to be padded to be compatible with import format
        try:
            sprint_dict["Count"].append(count)
            sprint_dict["Email Address"].append(doc.email)
            try:
                # handle case where a student is not in the roster and subsequently does not have a team
                sprint_dict["Team"].append(team_map[doc.email])
            except KeyError:
                sprint_dict["Team"].append(
                    "This student does not appear in the roster."
                )
        except KeyError:
            sprint_dict["Count"] = [count]
            sprint_dict["Email Address"] = [doc.email]
            try:
                sprint_dict["Team"] = [team_map[doc.email]]
            except KeyError:
                sprint_dict["Team"] = ["This student does not appear in the roster."]
        count += 1

        # get personal peer review data from doc to dict
        for i in range(16):
            try:
                sprint_dict[personal_pr_col_names[i]].append(
                    doc.personal_peer_rev[col_to_model_map[personal_pr_col_names[i]]]
                )
            except KeyError:
                sprint_dict[personal_pr_col_names[i]] = [
                    doc.personal_peer_rev[col_to_model_map[personal_pr_col_names[i]]],
                ]

        # get other peer review data from doc to dict
        reviewers = list(doc.received_peer_revs.keys())
        while len(reviewers) < 7:
            reviewers.append("")
        for i in range(7):
            rating = (
                doc.received_peer_revs[reviewers[i]]["rating"]
                if reviewers[i] != ""
                else ""
            )
            work = (
                doc.received_peer_revs[reviewers[i]]["what_did_they_do"]
                if reviewers[i] != ""
                else ""
            )
            try:
                sprint_dict[peer_rev_col_names[0] + str(i + 1)].append(reviewers[i])
                sprint_dict[peer_rev_col_names[1] + str(i + 1)].append(rating)
                sprint_dict[peer_rev_col_names[2] + str(i + 1)].append(work)
            except KeyError:
                sprint_dict[peer_rev_col_names[0] + str(i + 1)] = [reviewers[i]]
                sprint_dict[peer_rev_col_names[1] + str(i + 1)] = [rating]
                sprint_dict[peer_rev_col_names[2] + str(i + 1)] = [work]

        # include avg and stddev stats
        try:
            sprint_dict["Average peer review rating"].append(doc.avg_rating)
            sprint_dict["Peer review rating standard deviation"].append(
                doc.stddev_rating
            )
        except KeyError:
            sprint_dict["Average peer review rating"] = [doc.avg_rating]
            sprint_dict["Peer review rating standard deviation"] = [doc.stddev_rating]

    return pd.DataFrame(sprint_dict)
