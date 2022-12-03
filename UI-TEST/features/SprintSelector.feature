Feature: Select a sprint from a list of available sprint
Description: This feature allows a user to select different sprints

Scenario: Select a sprint from a list of available sprint
    Given The user is on Students page
    When The user clicks on the sprint dropdown
    Then The user should see a list of available sprints
    And The user should be able to select the sprint