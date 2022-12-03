from behave import *
from setup import driver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

@when('The user clicks on the sprint dropdown')
def click_sprintDropdown(context):
    driver.find_element(By.CSS_SELECTOR, ".sprint-selector").click()
    time.sleep(2)

@then('The user should see a list of available sprints')
def verify_sprintDropdown(context):
    sprint_text = driver.find_element(By.CSS_SELECTOR, ".sprint-selector").text
    assert sprint_text.__contains__("All Sprints")

@then('The user should be able to select the sprint')
def select_sprint(context):
    dropdown = driver.find_element(By.CSS_SELECTOR, ".sprint-selector")
    dropdown.find_element(By.XPATH, "//option[. = 'Sprint 1']").click()