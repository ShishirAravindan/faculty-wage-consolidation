#!python3

import utils
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import logging.config
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from decaptcha import decaptcha

config = {
    "css_target": ".rc-imageselect-desc-no-canonical > strong:nth-child(1)",
    "x_path": "/html/body/div/div/div[2]/div[1]/div[1]/div/strong",
    "iframe_id": "/html/body/div/div[2]/iframe",
    "instructions_CSS_target": "strong:nth-child(1)",
    "images_CSS": "html body div div#rc-imageselect div.rc-imageselect-payload div.rc-imageselect-challenge div#rc-imageselect-target.rc-imageselect-target table.rc-imageselect-table-33",
    "all_images": "html body div div#rc-imageselect div.rc-imageselect-payload div.rc-imageselect-challenge div#rc-imageselect-target.rc-imageselect-target table.rc-imageselect-table-33 tbody tr td.rc-imageselect-tile div.rc-image-tile-target div.rc-image-tile-wrapper img.rc-image-tile-33"
}

def solve_captcha(driver: WebDriver):
    payload, driver = identify_and_extract_captcha_form(driver)
    if not payload: 
        return driver
    else:
        target_class, images = payload[0], payload[1]
        img_path = utils._download_image_locally(images)
        results = decaptcha(target_class, img_path)
        click_images(driver, results)

def identify_and_extract_captcha_form(driver: WebDriver):
    try:
        captcha_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, config["iframe_id"]))
        )
        logging.info(f"CAPTCHA iFrame identified. Extracting info ...")
        payload, driver = extract_captcha_details(driver, captcha_iframe)
        driver.switch_to.default_content()
        return payload, driver
    except NoSuchElementException as e:
        logging.error(f"solve_captcha exception: {e.msg}")
    except TimeoutException as e:
        logging.info(f"No CAPTCHA found on page {e.msg}")
    return None, driver

def extract_captcha_details(driver: WebDriver, captcha_iframe: WebElement):
    try:
        driver.switch_to.frame(captcha_iframe)
        target_class, driver = _get_target_class(driver)
        images_src, driver = _get_images(driver)
        return [target_class, images_src], driver
    except Exception as e:
        logging.error(f"solve_captcha exception: {e}")
        driver.switch_to.default_content()
    return None, driver

def _get_target_class(driver):
    try:
        instruction_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config["instructions_CSS_target"]))
        )
        logging.info(f"CAPTCHA target: {instruction_element.text}")
        return instruction_element.text, driver
    except Exception as e:
        logging.error(f"Error Processing CAPTCHA form's instructions: {e}")
    return None, driver

def _get_images(driver):
    try:
        images_table_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config["all_images"]))
        )
        images_src = images_table_element.get_attribute("src")
        logging.info(f"CAPTCHA image source: {images_src}")
        return images_src, driver
    except NoSuchElementException as e:
        logging.error(f"[NoSuchElementException] Error Processing CAPTCHA form's images: {e}")
    except TimeoutException as e:
        logging.error(f"[TimeoutException] Error Processing CAPTCHA form's images: {e}")
    return '', driver

def click_images(driver: WebDriver, results: list[int]):
    """Given the driver and the results (i.e. predictions from the vLLM) click
    the corresponding tiles in the captcha form.

    For easier testing just use a dummy list for results
    eg: r = [0, 0, 0, 0, 1, 1, 1, 0, 1]
    should click the middle, middle-right, bottom-left and bottom-right
    then should hit the verify button
    """
    pass

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