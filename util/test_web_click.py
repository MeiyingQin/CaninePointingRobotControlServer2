import selenium
from selenium import webdriver
import time
import threading

class Dispenser():
    def __init__(self, user_email, user_password):
        self.driver = webdriver.Chrome()
        self.driver.get("https://portal.feedandgo.com/")
        email = self.driver.find_element_by_id("user_email")
        password = self.driver.find_element_by_id("user_password")
        submit_button = self.driver.find_element_by_class_name("login_submit_btn")
        email.send_keys(user_email)
        password.send_keys(user_password)
        submit_button.click()
    
    def feed(self):
        is_found = False
        while not is_found:
            try:
                feedNowButton = self.driver.find_element_by_partial_link_text("Feed Now")
                feedNowButton.click()
                is_found = True
            except selenium.common.exceptions.ElementNotVisibleException:
                print "wait for logging in..."
        
        is_found = False
        while not is_found:
            try:
                feedConfirmButton = self.driver.find_element_by_id("feed-yes")
                feedConfirmButton.click()
                is_found = True
            except selenium.common.exceptions.ElementNotVisibleException:
                print "wait for loading"
        
        is_found = False
        while not is_found:
            try:
                buttonParent = self.driver.find_element_by_id("callPetOver")
                cancelWebcamButton = buttonParent.find_element_by_css_selector(".btn.btn-default.left")
                cancelWebcamButton.click()
                is_found = True
            except selenium.common.exceptions.ElementNotVisibleException:
                print "wait for finishing"        

dispenser_1 = Dispenser("robot.pointing.feeder.1@gmail.com", "")

dispenser_1_thread = threading.Thread(target=Dispenser.feed, args=(dispenser_1,))

dispenser_1_thread.start()