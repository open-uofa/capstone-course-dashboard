from behave import given, when, then
from selenium.webdriver.common.by import By
from setup import driver
import time

@given('The user is on the login page')
def go_to_loginPage(context):
    driver.get("http://127.0.0.1:5173")
    res = driver.find_element(By.CSS_SELECTOR, 'button[class^="login_btn"]').is_displayed()
    assert res == True

@when('The user clicks on the login button')
def click_login(context):
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[1]/main/section/div/div/button").click()

@then('a new window should open')
def new_window(context):
    window = driver.window_handles
    assert(len(window) == 2)
 
