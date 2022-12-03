import time

from behave import *
from setup import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


@then('The user drags and drop grids to change their positions')
def drag_grid(context):
    element =driver.find_element(By.CSS_SELECTOR, ".item-content > :nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(element).click_and_hold().perform()
    time.sleep(2)

    element = driver.find_element(By.CSS_SELECTOR, ".item-content > :nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(2)

    element = driver.find_element(By.CSS_SELECTOR, ".item-content > :nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(element).release().perform()
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, ".item-content > :nth-child(1)").click()
    element = driver.find_element(By.CSS_SELECTOR, ".item3 > .grid-content > :nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(element).click_and_hold().perform()
