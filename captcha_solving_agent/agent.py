#!python3

import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import logging
import logging.config

config = {
    "css_target": ".rc-imageselect-desc-no-canonical > strong:nth-child(1)"
}

def solve_captcha(driver: WebDriver):
    targetElement = driver.find_element(By.CSS_SELECTOR, config["css_target"])
    print(f"solve_captcha: target={targetElement.text}")


def identify_captcha_form(driver: WebDriver):
    captcha_form_element = driver.find_element(By.CSS_SELECTOR, '.rc-imageselect')
    try:
        instructions_element = captcha_form_element.find_element(By.CSS_SELECTOR, "rc-imageselect-desc-no-canonical")
        print(instructions_element.text)
    except Exception as e:
        print("An error occurred:", str(e))

def extract_captcha_details():
    pass

def call_decaptcha():
    pass

def solve_captcha_form():
    pass

def main():
    logging.basicConfig(level=logging.DEBUG, 
                        format="[%(levelname)s] %(message)s")
    URL = "https://iam.uiowa.edu/whitepages/search"
    name = "THOMAS S GRUCA"
    logging.info("PAGE LOADING")
    driver = utils.fill_form(URL, name)
    logging.info("FORM FILLED")
    identify_captcha_form(driver)
    logging.info("CAPTCHA reached")

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


if __name__ == "__main__":
    main()