Feature: Course selection
Description : This feature allows a user to be navigated to course page upton selection of a course from the list of courses.

Scenario: User selects a course from the list of courses
    Given the user is on the dashboard page
    When the user selects a course from the list of courses
    Then the user is navigated to the course page