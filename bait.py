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

    def setup_page(self, is_refresh=False):
        self.driver.maximize_window()
        if is_refresh:
            self.driver.refresh()

    # def cleanup_page(self):
    #     self.driver.refresh()
    
    def feed(self):
        
        self.driver.execute_script("window.focus();")
        count = 0
        max_count = 4

        has_rotated = False
        while not has_rotated:
            print "round"
            is_found = False
            while count < max_count and not is_found:
                try:
                    feedNowButton = self.driver.find_element_by_partial_link_text("Feed Now")
                    feedNowButton.click()
                    is_found = True
                except selenium.common.exceptions.ElementNotVisibleException:
                    count += 1
                    print "wait for logging in..."
            print "first count ", count
            
            count = 0
            is_found = False
            while count < max_count and not is_found:
                try:
                    feedConfirmButton = self.driver.find_element_by_id("feed-yes")
                    feedConfirmButton.click()
                    is_found = True
                except selenium.common.exceptions.ElementNotVisibleException:
                    count += 1
                    print "wait for loading"
            print "second count ", count
            
            count = 0
            is_found = False
            while count < max_count and not is_found:
                try:
                    buttonParent = self.driver.find_element_by_id("callPetOver")
                    cancelWebcamButton = buttonParent.find_element_by_css_selector(".btn.btn-default.left")
                    cancelWebcamButton.click()
                    is_found = True
                    has_rotated = True
                except selenium.common.exceptions.ElementNotVisibleException:
                    count += 1
                    print "wait for finishing"
            print "third count ", count
        
        time.sleep(5)

    def close(self):
        self.driver.quit()