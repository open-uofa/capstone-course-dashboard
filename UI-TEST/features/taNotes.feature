Feature: TA Notes
    This feature allows the user to view, add, remove, and modify notes for a team

    Background: User is logged in
        Given a working MongoDB database
        And a valid account
        And a course exists with at least one team
        And the user is on a team's page

    Scenario: User adds a note
        When the user clicks a button to add a note
        Then the user should see a popup with text fields to enter a note
        When the user fills in the note and submits it
        Then the popup should close
        And the note should be available for viewing

    Scenario: User views a note
        Given a team has at least one note
        When the user opens a note
        Then a popup should appear with the note's information
        When the user closes the note
        Then the popup should close

    Scenario: User updates a note
        Given a team has at least one note
        When the user opens a note
        Then a popup should appear with the note's information
        When the user updates the note and submits it
        Then the popup should close
        And the note should be available for viewing with updated information

    Scenario: User deletes a note
        Given a team has at least one note
        When the user opens a note
        Then a popup should appear with the note's information
        When the user deletes the note
        Then the popup should close
        And the note should no longer be available for viewing
