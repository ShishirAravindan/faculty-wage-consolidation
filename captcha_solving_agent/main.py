#!python3 

import utils, agent, decaptcha
import logging, logging.config
import sys
import json

def process(config):
    logging.info("PAGE LOADING")
    URL, NAMES = config.get("URL"), config.get("NAMES")
    driver = utils.fill_form(URL, NAMES[0])
    logging.info("FORM FILLED")
    driver = agent.captcha_workflow(driver)
    logging.info("CAPTCHA COMPLETED")
    

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