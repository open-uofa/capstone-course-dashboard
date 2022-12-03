from behave import *
from setup import driver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


@given('The user is on Edit course page')
def go_to_editCoursePage(context):
    driver.get("http://127.0.0.1:5173/dashboard/course/course-data")
    time.sleep(3)

@when('The user clicks on add sprint button')
def click_addSprint(context):
    driver.find_element(By.CSS_SELECTOR, "img").click()
    time.sleep(3)

@then('The user should be able to see a pop up with a form to add a new sprint')
def verify_addSprint_modal(context):
    header_text = driver.find_element(By.CSS_SELECTOR, ".modal").text
    assert header_text.__contains__("Add Sprint")
