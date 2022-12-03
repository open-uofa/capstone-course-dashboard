Feature: Dashboard Side Navigation
Description : This feature allows the user to navigate through the dashboard using the side navigation bar.


Scenario: Side Navigation functionality
    Given The user is on the course page
    When The user hovers the move over the side navigation bar
    Then The user clicks the Teams tab
    Then The user should be redirected to teams page
    When The user clicks the Students tab
    Then The user should be redirected to students page