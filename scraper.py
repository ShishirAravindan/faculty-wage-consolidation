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
    if elementName:
        _wait_for_elements(driver, elementName)
    return driver

def scrape_faculty_information_for_prof(name):
    """
    This function scrapes the department information for a given professor.
    :param name: The name of the professor
    :return: The department of the professor
    """
    #trying the faculty one first
    try:
        driver = make_connection("https://iam.uiowa.edu/whitepages/search",None)
        time.sleep(2)

        name_field = driver.find_element(By.NAME, 'SearchEntry')
        name_field.send_keys(name)
        time.sleep(2)  # Adding a pause to simulate human interaction
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        time.sleep(2)  # Adding a longer pause to allow the page to load
        #Captcha check
        if identify_captcha_check(driver):
            print("Captcha Check")
            #passing_captcha_logic()
            return
        html = driver.page_source
        # html =response.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='table search-result-table')
        if table is not None:
            tr_tags = table.find_all('tr')
            if len(tr_tags) > 7:
                # print(tr_tags)
                dept = tr_tags[7].text.strip('\n').split('\n')[4].strip()
                # dept = tr_tags[7].text.split('\n')[0]
                print(name, ' ', dept)
                return dept
            else:
                print("Not enough rows in the table.")
        else:
            print("Table not Found")
        driver.quit()

    except TimeoutException as e:
        print("TimeoutException", e)
    except NoSuchElementException as e:
        print("NoSuchElementException", e)
    finally:
        driver.quit()





def scrape_faculty_information_for_chunk(chunk):
    """
    This function scrapes the department information for a chunk of professors. using threads

    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = [executor.submit(scrape_faculty_information_for_prof, person['name']) for person in chunk]
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

scrape_faculty_information_for_chunk([{'name': 'THOMAS S GRUCA'}, {'name': 'JEFFREY C GIESE'}, {'name': 'JULIA GARLICK'}, {'name': 'STEPHANIE C GANTZ'}, {'name': 'THOMAS P GALLANIS'}])