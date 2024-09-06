import time
import requests
import mechanize
from bs4 import BeautifulSoup
import os
import tabula
import pandas as pd
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import json
import scraperutils

'''
This scraper is used for tippie college of business
'''
def get_tippie_dept2():
    try:
        df = pd.read_excel("IOWAsalary2023.xlsx")
        options = Options()
        options.set_preference("dom.popup_maximum", 0)
        options.set_preference("privacy.popups.disable_from_plugins", 3)
        options.add_argument("--headless")  # Uncomment this line if you need to run the script in headless mode
        driver = webdriver.Firefox(options=options)
        for i in range(1, 36):
            time.sleep(1)
            if i == 1:
                url = f'https://tippie.uiowa.edu/people/'
            else:
                url = f'https://tippie.uiowa.edu/people/?page={i}'
            driver.get(url)
            time.sleep(2)
            wait = WebDriverWait(driver, 1)
            # input_element = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search..."]')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            ol = soup.find('ol', class_='grid gap-y-4')
            if ol is not None:
                lis = ol.find_all('li')
                for li in lis:
                    if li is not None:
                        h2_name_tag = li.find('h2')
                        if h2_name_tag is not None:
                            h2_name = h2_name_tag.text
                            #print(h2_name)
                        h3_tags = li.find_all('h3')
                        if h3_tags is not None and len(h3_tags) > 1:
                            h3_tag_dept = h3_tags[1]
                            h3_title_tag = h3_tags[0]
                            dept = h3_tag_dept.text
                            title = h3_title_tag.text
                            if 'professor' in title.lower():
                                normalised_name = normalize_name(h2_name)
                                print(h2_name, "is a professor")
                                if normalised_name in df['Name'].tolist():
                                    print("Found a match!")
                                    print(h2_name, ' ', dept)
                                    df.loc[df['Name'] == normalised_name, 'Department'] = dept
            print("Done with page ", i)
        driver.quit()

        #print(h2_name, ' ', dept)

        return df
    except Exception as e:
        print("CANT SCRAPE")
        print(e)
        driver.quit()

'''
This scraper is used for public health faculty
'''
def get_public_health_faculty():
    try:
        # Set up Selenium options
        options = Options()
        options.set_preference("dom.popup_maximum", 0)
        options.set_preference("privacy.popups.disable_from_plugins", 3)
        options.add_argument("--headless")  # Run in headless mode (no GUI)

        # Initialize the Firefox driver with the specified options
        driver = webdriver.Firefox(options=options)

        # Navigate to the main URL
        main_url = 'https://www.public-health.uiowa.edu/faculty-list/'
        driver.get(main_url)
        name_dept_map = {}

        # Locate all table rows on the page
        table = driver.find_element(By.CLASS_NAME, 'directory')
        tr_elements = table.find_elements(By.XPATH, './tbody/tr')

        for tr in tr_elements:
            td_element = tr.find_element(By.XPATH, './td[@style="white-space: nowrap;"]')
            a_tag = td_element.find_element(By.TAG_NAME, 'a')
            name = a_tag.text
            link_a = a_tag.get_attribute('href')
            response = requests.get(link_a)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the specific 'div' with the class 'entry-content'
            div = soup.find('div', class_='entry-content')

            if div:
                # Find the second 'p' tag within the 'div'
                p_tags = div.find_all('p')
                p_intersted = p_tags[1]
                dept_text = p_intersted.text
                for line in dept_text.split('/n'):
                    if "Department:" in line:
                        dept = line.split("Department: ")[1].split('\n')[0]
                        print(name, ' ', dept)
                        name_dept_map[name] = dept
        driver.quit()               
        df_2 = pd.DataFrame(list(name_dept_map.items()), columns=['Name', 'Department'])
        df_2.to_excel('public-healthIowa.xlsx', index=False)
        return df
        
    except Exception as e:
        print("CANT SCRAPE")
        print(e)
        driver.quit()

'''
This scraper is used for engineering faculty
'''
def get_engineering_department():
    try:
        name_dept_map = {}
        # Set up Selenium options
        options = Options()
        options.set_preference("dom.popup_maximum", 0)
        options.set_preference("privacy.popups.disable_from_plugins", 3)
        options.add_argument("--headless")  # Run in headless mode (no GUI)

        # Initialize the Firefox driver with the specified options
        driver = webdriver.Firefox(options=options)
        # Navigate to the main URL
        for page in range(12):
            url = f'https://engineering.uiowa.edu/directory?page={page}'
            driver.get(url)
            time.sleep(2)
            div_tags = driver.find_elements(By.CLASS_NAME, 'card__body')
            for div in div_tags:
                inner_div = div.find_element(By.CLASS_NAME, 'field__items')
                name_span_tag = div.find_element(By.TAG_NAME, 'h2')
                name  = name_span_tag.text
                split_1_string = inner_div.text.split('\n')[0]
                if ',' in split_1_string:
                    dept = split_1_string.split(',')[1].strip()
                    #print(name, ' ', dept)
                    name_dept_map[name] = dept
                else:
                    dept = split_1_string.split(' ')[1].strip()
                    #print(name, ' ', dept)
                    name_dept_map[name] = dept
                    
                #print(inner_div.text.split('\n')[0].split(',')[1].strip())
               
        driver.quit()
        df = pd.DataFrame(list(name_dept_map.items()), columns=['Name', 'Department'])
        df.to_excel('engineeringIowa.xlsx', index=False)
                
        
        
    except Exception as e:
        print("CANT SCRAPE")
        print(e)
        driver.quit()
    

                    
                
