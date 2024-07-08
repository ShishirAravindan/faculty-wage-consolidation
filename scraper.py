#!.finPayVenv/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import concurrent.futures

def _setup_driver():
    firefox_options = Options()
    firefox_options.set_preference("dom.popup_maximum", 0)
    firefox_options.set_preference("privacy.popups.disable_from_plugins", 3)
    firefox_options.add_argument("--headless")  # Uncomment this line if you need to run the script in headless mode
    return webdriver.Firefox(options=firefox_options)

def _wait_for_elements(driver, path_name, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, path_name))
    )


def make_connection(URL, elementName):
    driver = _setup_driver()
    driver.get(URL)
    #_wait_for_elements(driver, elementName)
    return driver

def scrape_faculty_information_for_prof(name):
    driver = make_connection(f'https://tippie.uiowa.edu/people/', '//input[@placeholder="Search..."]')
    time.sleep(2)
    input_element = _wait_for_elements(driver, '//input[@placeholder="Search..."]')
    input_element.send_keys(name)
    time.sleep(2)
    submit_button = driver.find_element(By.XPATH, '//button[@variant="primary"]')
    submit_button.click()
    time.sleep(2)
    if identify_captcha_check(driver):
        passing_captcha_logic()
    html = driver.page_source
    #Discuss which page to scrape.





def scrape_faculty_information_for_chunk(chunk):
    #Pre-captcha scraping
    driver = make_connection(f'https://tippie.uiowa.edu/people/', '//input[@placeholder="Search..."]')
    # Do multithreading here to scrape multiple faculty members at once
    #initiate multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = [executor.submit(get_diff_link_dept, person['name']) for person in chunk]
        for f in concurrent.futures.as_completed(results):
            print(f.result())




def identify_captcha_check(driver):
    try:
        captcha_element = driver.find_element(By.ID, "captcha")
        return True
    except:
        return False

def passing_captcha_logic():
    pass