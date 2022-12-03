from behave import *
from setup import driver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

@given('The user is on the dashboard page')
def go_to_dashboardPage(context):
    driver.get("http://localhost:5173/dashboard")

@when('The user selects a course from the list of courses')
def select_course(context):
    driver.find_element(By.CSS_SELECTOR, ".course:nth-child(4)").click()

@then('The user is navigated to the course page')
def verify_coursePage(context):
    header_text = driver.find_element(By.CSS_SELECTOR, "h2").text
    assert header_text.__contains__("Teams")
