Feature: Dashboard Login
Description: This feature allows you to login to the dashboard using google oauth


# will fix in next sprint, sign in on my machine gives unauthorized error
# need a sample account to run google login tests
Scenario: Login with google oauth
    Given The user is on the login page
    When The user clicks on the login button
    Then a new window should open
    # # When The user logins with google  todo
    # # Then verify the user is logged in todo


