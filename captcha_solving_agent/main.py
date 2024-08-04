#!python3 

import utils, agent, decaptcha
import logging, logging.config
import sys
import json
import state
from selenium.common.exceptions import ElementClickInterceptedException

STATE_FILE_PATH = '../data/2_salariesUoIstate_2023.json'

def process(config):
    URL, NAMES = config.get("URL"), state.get_fresh_chunk(STATE_FILE_PATH, 5)
    NAMES = {
        "ABDEL-MALEK,KARIM": "null",
        "ABOUL HOSN,MAEN": "null", 
        "Abbas, Paul J": "null", 
        "ABDEL WAHED,LAMA": "null"
    }
    driver = utils.make_connection(URL, None)
    logging.info("PAGE LOADING")
    

    for name, _ in NAMES.items():
        logging.info(f"---------GETTING FACULTY INFORMATION FOR {name}---------")
        driver = utils.fill_form(driver, name)
        try:
            NAMES[name] = utils.get_faculty_department(driver, name)
            logging.info(f'FACULTY DEPT for {name}: {NAMES[name]}')
            logging.info(f"---------WRITING RESULTS TO STATE FILE---------")
            state.update_state_file(STATE_FILE_PATH, NAMES)
        except ElementClickInterceptedException as e:
            driver = agent.captcha_workflow(driver)
            logging.info("CAPTCHA COMPLETED")
            NAMES[name] = utils.get_faculty_department(driver, name)
            logging.info(f'FACULTY DEPT for {name}: {NAMES[name]}')
            logging.info(f"---------WRITING RESULTS TO STATE FILE---------")
            state.update_state_file(STATE_FILE_PATH, NAMES)

    

def main():
    logging.config.fileConfig("test_log.ini")
    if len(sys.argv) != 2:
        print("Usage: ./main.py <config_file>")
        sys.exit(1)
    config_file = sys.argv[1]
    with open(config_file, 'r') as file:
        config = json.load(file)
    process(config)


if __name__ == "__main__":
    main()