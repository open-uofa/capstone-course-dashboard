from behave import *
from setup import driver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#todo
@given('The user is on the course page')
def go_to_coursePage(context):
    # can not test it properly until login is done
    driver.get("http://127.0.0.1:5173/dashboard/course")


@when('The user hovers the move over the side navigation bar')
def mover_over_sideNavBar(context):
    time.sleep(2)
    navBar = driver.find_element(By.CLASS_NAME, "navbar")
    ActionChains(driver).move_to_element(navBar).perform()
    time.sleep(2)

@then('The user clicks the Teams tab')
def click_teams(context):
    navBar = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/nav/a[3]/span")
    ActionChains(driver).move_to_element(navBar).click().perform()
    time.sleep(2)
   
@then('The user should be redirected to teams page')
def teams_page(context):
    header_text = driver.find_element(By.CSS_SELECTOR, "h1").text
    assert header_text.__contains__("Teams")

@when('The user clicks the Students tab')
def click_students(context):
    navBar = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/nav/a[4]/span")
    ActionChains(driver).move_to_element(navBar).click().perform()
    time.sleep(2)

@then('The user should be redirected to students page')
def students_page(context):

    header_text = driver.find_element(By.CSS_SELECTOR, "h1").text
    assert header_text.__contains__("Students")





