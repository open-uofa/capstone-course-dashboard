Feature: Add a new sprint button
Description: This feature allows a user to add a new sprint to the course

Scenario: User Clicks on add sprint button
    Given The user is on Edit course page
    When The user clicks on add sprint button
    Then The user should be able to see a pop up with a form to add a new sprint