from behave import *
from setup import driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

# TODO: Mock backend (setup another FastAPI instance)
# Background setup
@given('a working MongoDB database')
def setup_db(context):
    pass

@given('a valid account')
def login(context):
    pass

@given('a course exists with at least one team')
def validate_courses(context):
    pass

@given("the user is on a team's page")
def navigate_to_team(context):
    # Assume our dev backend is running
    course = 'course1'
    team = 'capstone-dashboard-duplicate'
    driver.get(f"http://localhost:5173/dashboard/teams/team?team_name={team}&course={course}")
    # TODO: May want to replace sleep with WebDriverWait
    sleep(1)

# TESTS BEGIN HERE #

# Scenario: User adds a note
@when('the user clicks a button to add a note')
def click_add_note(context):
    # TODO: Check element is not None
    driver.find_element(By.CSS_SELECTOR, 'button[class^="notes-btn1"]').click()

@then('the user should see a popup with text fields to enter a note')
def check_note_popup(context):
    # Driver raises exception on failure
    driver.find_element(By.CSS_SELECTOR, 'div[class^="modal"] textarea')

@when('the user fills in the note and submits it')
def submit_note(context):
    driver.find_element(By.CSS_SELECTOR, 'div[class^="modal"] textarea').send_keys('Test value')
    driver.find_element(By.CSS_SELECTOR, 'button[class^="notes-btn2"]').click()
    sleep(1)

@then('the popup should close')
def check_modal_closed(context):
    scenario = context.scenario
    try:
        # Modal element should no longer exist
        if scenario.name.lower() == 'user adds a note':
            driver.find_element(By.CSS_SELECTOR, 'div[class^="modal-wrapper"]')
            raise AssertionError('Modal not closed')

        check_note_opened()
    except NoSuchElementException:
        return True

@then('the note should be available for viewing')
def check_note_available(context):
    notes = driver.find_elements(By.CSS_SELECTOR, 'item')
    for note in notes:
        text_field = note.find_element(By.XPATH, './article/textarea')
        if text_field.text == 'Test value':
            return True

    raise AssertionError('New note not found')

# Scenario: User views a note
@given('a team has at least one note')
def check_team_has_notes(context):
    driver.find_elements(By.CSS_SELECTOR, 'item')

@when('the user opens a note')
def open_note(context):
    driver.find_element(By.CSS_SELECTOR, 'item').click()

@then("a popup should appear with the note's information")
def check_note_opened(context):
    driver.find_element(By.CSS_SELECTOR, 'dialog[open]')

@when('the user closes the note')
def close_note(context):
    driver.find_element(By.CSS_SELECTOR, 'dialog[open] > button').click()
    try:
        check_note_opened(context)
    except NoSuchElementException:
        return True

    raise AssertionError('Note never closed')

# Scenario: User updates a note
@when('the user updates the note and submits it')
def update_note(context):
    # Previous behaviours should have opened the note
    driver.find_element(By.CSS_SELECTOR, 'dialog[open] > textarea').send_keys('Test value 2')
    driver.find_element(By.CSS_SELECTOR, 'dialog[open] notes-btn2').click()
    sleep(1)

@then('the note should be available for viewing with updated information')
def check_note_updated(context):
    notes = driver.find_elements(By.CSS_SELECTOR, 'item')
    for note in notes:
        text_field = note.find_element(By.XPATH, './article/textarea')
        if text_field.text == 'Test value 2':
            return True

    raise AssertionError('New note not found')

# Scenario: User deletes a note
@when('the user deletes the note')
def delete_note(context):
    # Previous behaviours should have opened the note
    driver.find_element(By.CSS_SELECTOR, 'dialog[open] > textarea').send_keys('Test value 2')
    driver.find_element(By.CSS_SELECTOR, 'dialog[open] notes-btn3').click()
    sleep(1)

@then('the note should no longer be available for viewing')
def check_note_deleted(context):
    notes = driver.find_elements(By.CSS_SELECTOR, 'item')
    for note in notes:
        text_field = note.find_element(By.XPATH, './article/textarea')
        if text_field.text == 'Test value 2':
            raise AssertionError('Note not deleted')

    return True
