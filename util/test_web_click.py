import selenium
from selenium import webdriver
import time


driver = webdriver.Chrome()
driver.get("https://portal.feedandgo.com/")

email = driver.find_element_by_id("user_email")
password = driver.find_element_by_id("user_password")
submit_button = driver.find_element_by_class_name("login_submit_btn")

email.send_keys("robot.pointing.feeder.1@gmail.com")
password.send_keys("keepondancing")
submit_button.click()

is_continue = True
while is_continue:
    user_input = raw_input("press any key to continue, press q to quit: ")
    if user_input == "q":
        is_continue = False
        continue
    else:
        is_found = False
        while not is_found:
            try:
                feedNowButton = driver.find_element_by_partial_link_text("Feed Now")
                feedNowButton.click()
                is_found = True
            except selenium.common.exceptions.ElementNotVisibleException:
                print "wait for logging in..."
        
        is_found = False
        while not is_found:
            try:
                feedConfirmButton = driver.find_element_by_id("feed-yes")
                feedConfirmButton.click()
                is_found = True
            except selenium.common.exceptions.ElementNotVisibleException:
                print "wait for loading"
        
        is_found = False
        while not is_found:
            try:
                buttonParent = driver.find_element_by_id("callPetOver")
                cancelWebcamButton = buttonParent.find_element_by_css_selector(".btn.btn-default.left")
                cancelWebcamButton.click()
                is_found = True
            except selenium.common.exceptions.ElementNotVisibleException:
                print "wait for finishing"
