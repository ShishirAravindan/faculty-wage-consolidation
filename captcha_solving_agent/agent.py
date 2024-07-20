#!python3

import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import logging.config
from selenium.common.exceptions import NoSuchElementException, TimeoutException

config = {
    "css_target": ".rc-imageselect-desc-no-canonical > strong:nth-child(1)",
    "x_path": "/html/body/div/div/div[2]/div[1]/div[1]/div/strong"
}

def solve_captcha(driver: WebDriver):
    # targetElement = driver.find_element(By.CSS_SELECTOR, config["css_target"])
    try:
        targetElement = WebDriverWait(driver, 20).until(
            # EC.presence_of_element_located((By.CSS_SELECTOR, config["css_target"]))
            EC.presence_of_element_located((By.XPATH, config["x_path"]))
        )
        logging.info(f"solve_captcha: {targetElement}")
    # try:
    #     targetElement = driver.find_element(By.XPATH, config["x_path"])
    #     logging.info(f"solve_captcha: target={targetElement.text}")
    except NoSuchElementException as e:
        logging.error(f"solve_captcha exception: {e.msg}")
    


def identify_captcha_form(driver: WebDriver):
    captcha_form_element = driver.find_element(By.CSS_SELECTOR, '.rc-imageselect')
    try:
        instructions_element = captcha_form_element.find_element(By.CSS_SELECTOR, "rc-imageselect-desc-no-canonical")
        print(instructions_element.text)
    except Exception as e:
        print("An error occurred:", str(e))

# def extract_captcha_details():
#     pass

# def call_decaptcha():
#     pass

# def solve_captcha_form():
#     pass

#--------------------------------------------------------------------------------
# Test code
def test_main():
    logging.config.fileConfig("test_log.ini")
    URL = "https://iam.uiowa.edu/whitepages/search"
    name = "THOMAS S GRUCA"
    logging.info("PAGE LOADING")
    driver = utils.fill_form(URL, name)
    logging.info("FORM FILLED")
    solve_captcha(driver)
    logging.info("CAPTCHA reached")

    # TODO: All other test case
        
    
if __name__ == "__main__":
    test_main()