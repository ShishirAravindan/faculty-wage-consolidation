#!.finPayVenv/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def _setup_driver():
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    return webdriver.Firefox(options=firefox_options)

def _wait_for_elements(driver, class_name, timeout=10):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )


def make_connection(URL, elementName):
    driver = _setup_driver()
    driver.get(URL)
    _wait_for_elements(driver, elementName)
    return driver

def scrape_faculty_information_for_chunk(chunk):
    pass

def identify_captcha_check(driver):
    try:
        captcha_element = driver.find_element(By.ID, "captcha")
        return True
    except:
        return False

def passing_captcha_logic():
    pass