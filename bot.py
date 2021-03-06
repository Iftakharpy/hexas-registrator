from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#exceptions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException

from selenium.webdriver.remote.webelement import WebElement

from time import sleep
from datetime import datetime
from functools import reduce
from typing import List, Union



TIME_FORMAT = "%I:%M %p"
t1 = datetime.strptime('09:00 AM', TIME_FORMAT)
t2 = datetime.strptime('10:00 AM', TIME_FORMAT)
#datetime.timedelta
t2-t1

def get_driver():
    driver = webdriver.Chrome("chromedriver.exe")
    return driver

DRIVER = None

login_url = "http://appsznd.hexaszindabazar.com/index.php"
#login selectors
login_user_name_xpath = "//input[@name='user_name']"
login_password_xpath = "//input[@name='password']"
login_btn_xpath = "//button[@name='commit']"
logged_in_element_check_xpath = "//p"
text_to_compare_with = "Welcome"


#urls for regristration
listening_registration_url = "http://appsznd.hexaszindabazar.com/listening.php"
speaking_registration_url = "http://appsznd.hexaszindabazar.com/speaking.php"
# speaking_registration_url = "file:///D:/Hexas/HEXA'S%20Student%20Management%20System.html" # testing link
reading_registration_url = "http://appsznd.hexaszindabazar.com/reading.php"
writing_registration_url = "http://appsznd.hexaszindabazar.com/writing.php"
#registrations time locator
element_xpath_to_locate_registration_time = "//tbody"



def reload_until_element_located(url, element_xpath, driver=DRIVER):
    driver.get(url)
    while True:
        try:
            WebDriverWait(driver, .1).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
            if driver.find_element_by_xpath(element_xpath):
                return True
        except TimeoutException:
            driver.refresh()

def get_times_items(tbody: WebElement):
    # collecting applicable items
    items = tbody.find_elements_by_xpath("tr")
    # getting times from the items
    times = []
    for row in items:
        str_time = row.find_element_by_xpath("td[2]").text.upper()
        datetime_obj = datetime.strptime(str_time, TIME_FORMAT)
        times.append((row, datetime_obj, str_time))
    # returning tuple(WebElement, datetime, str_time)
    return times

def get_registration_item(start_time:datetime, end_time:datetime, time_priority="start|middle|end", driver=DRIVER):
    tbody = driver.find_element_by_xpath(element_xpath_to_locate_registration_time)
    items_times = get_times_items(tbody)
    
    items_times.sort(key = lambda item: item[1])
    registerable_times = list(filter(lambda x: end_time>=x[1]>=start_time, items_times))
    if len(registerable_times)>0:
        if len(registerable_times)==1:
            return registerable_times[0]
        if time_priority=="start":
            return registerable_times[0]
        elif time_priority=="end":
            return registerable_times[-1]
        elif time_priority=="middle":
            return registerable_times[len(registerable_times)//2]
        else:
            raise ValueError(f"time_priority=\"{time_priority}\" is not allowed")
    else:
        print("Coudn't find any suitable time.")


#================================================================================================================================================

def login(user_name:str, password: str, URL=login_url, Wait_Time=60, driver=DRIVER) -> bool:
    #going to the website
    driver.get(URL)
    
    WebDriverWait(driver, Wait_Time).until(EC.presence_of_element_located((By.XPATH, login_btn_xpath)))

    #getting the form fields
    user_name_field = driver.find_element_by_xpath(login_user_name_xpath)
    password_field = driver.find_element_by_xpath(login_password_xpath)
    login_btn = driver.find_element_by_xpath(login_btn_xpath)
    
    #sending credentials
    user_name_field.send_keys(user_name)
    password_field.send_keys(password)
    login_btn.click()
    
    try:
        WebDriverWait(driver, Wait_Time).until(EC.presence_of_element_located((By.XPATH, logged_in_element_check_xpath)))    
    except UnexpectedAlertPresentException:
        return False
    
    logged_in_element = driver.find_element_by_xpath(logged_in_element_check_xpath)
    text = logged_in_element.text.strip()
    text = text.split(",")[0]
    if text == text_to_compare_with:
        return True
    print(f"\"{text_to_compare_with}\" != \"{text}\"")
    return False

#================================================================================================================================================

def register_for_speaking(
        start_time = "09:00 AM",
        end_time = "07:00 PM",
        priority = "start|middle|end",
        password = "",
        url = speaking_registration_url,
        registration_time_locator = element_xpath_to_locate_registration_time,
        wait_for_alert = 5, #seconds
        driver = DRIVER
            ):
    """
    Format: "HH:MM PM/AM"

    This function will register for speaking test in between the time range provided.
    """
    start_time = datetime.strptime(start_time.upper(), TIME_FORMAT)
    end_time = datetime.strptime(end_time.upper(), TIME_FORMAT)
    priority = priority.lower()

    while True:
        reload_until_element_located(url, registration_time_locator, driver)
        reg_item = get_registration_item(start_time, end_time, priority, driver)
        if reg_item:
            reg_url = reg_item[0].find_element_by_xpath("td/a").get_attribute("href")
            break

    #register for the test
    reload_until_element_located(reg_url, "//input[@name='type' and @value='Academic']",driver)
    driver.find_element_by_xpath("//input[@name='type' and @value='Academic']").click()
    driver.find_element_by_xpath("//input[@id='pass']").send_keys(password)
    driver.find_element_by_xpath("//input[@name='type' and @value='Academic']").click()
    driver.find_element_by_xpath("//button[@id='apply']").click()
    try:
        WebDriverWait(driver, wait_for_alert).until(EC.alert_is_present())
        alert_obj = driver.switch_to_alert()
        print(alert_obj.text)
        alert_obj.accept()
    except UnexpectedAlertPresentException:
        raise(AssertionError)


def register_for_reading(
        start_time = "09:00 AM",
        end_time = "07:00 PM",
        priority = "start|middle|end",
        password = "",
        url = reading_registration_url,
        registration_time_locator = element_xpath_to_locate_registration_time,
        wait_for_alert = 10, #seconds
        driver = DRIVER
            ):
    register_for_speaking(start_time, end_time, priority, password, url, registration_time_locator, wait_for_alert, driver)

def register_for_writing(
        start_time = "09:00 AM",
        end_time = "07:00 PM",
        priority = "start|middle|end",
        password = "",
        url = writing_registration_url,
        registration_time_locator = element_xpath_to_locate_registration_time,
        wait_for_alert = 5, #seconds
        driver = DRIVER
            ):
    register_for_speaking(start_time, end_time, priority, password, url, registration_time_locator, wait_for_alert, driver)

def register_for_listening(
        start_time = "09:00 AM",
        end_time = "07:00 PM",
        priority = "start|middle|end",
        password = "",
        url = listening_registration_url,
        registration_time_locator = element_xpath_to_locate_registration_time,
        wait_for_alert = 6, #seconds
        driver = DRIVER
            ):
    register_for_speaking(start_time, end_time, priority, password, url, registration_time_locator, wait_for_alert, driver)


class Bot:
    def __init__(self,
        hexas_id = "HZ15626",
        password = "AS26",
        start_time = "09:00 AM",
        end_time = "05:00 PM",
        priority = "start|middle|end",
        register_for = "listening|speaking|reading|writing"
        ):
        self.DRIVER = get_driver()
        self.hexas_id = hexas_id.upper()
        self.password = password.upper()
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority.lower()
        self.register_for = register_for.lower()
        
        # login to the user account
        login(self.hexas_id, self.password, driver=self.DRIVER)
        # register for the exam
        self.register()
    
    def register(self):
        if self.register_for == "listening":
            register_for_listening(self.start_time, self.end_time, self.priority, self.password, driver=self.DRIVER)
        elif self.register_for == "speaking":
            register_for_speaking(self.start_time, self.end_time, self.priority, self.password, driver=self.DRIVER)
        elif self.register_for == "reading":
            register_for_reading(self.start_time, self.end_time, self.priority, self.password, driver=self.DRIVER)
        elif self.register_for == "writing":
            register_for_writing(self.start_time, self.end_time, self.priority, self.password, driver=self.DRIVER)
        else:
            print("ValueError: register_for != 'listening'|'speaking'|'reading'|'writing'")
        self.DRIVER.close()
