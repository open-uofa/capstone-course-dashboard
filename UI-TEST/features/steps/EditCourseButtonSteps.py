from behave import *
from setup import driver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

@given('The user is on Students page')
def go_to_studentsPage(context):
    driver.get("http://127.0.0.1:5173/dashboard/students")
    time.sleep(3)

@when('The user clicks on Edit Course button')
def click_editCourse(context):
    driver.find_element(By.CSS_SELECTOR, ".edit-button").click()
    time.sleep(3)
    
@then('The user is redirected To Edit Course page')
def verify_editCoursePage(context):
    header_text = driver.find_element(By.CSS_SELECTOR, "h1").text
    assert header_text.__contains__("Edit")
