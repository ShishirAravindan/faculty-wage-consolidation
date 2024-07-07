#!.finPayVenv/bin/python3

import os
from state import make_initial_state_file, get_fresh_chunk, update_state_file
from scraper import scrape_faculty_information_for_chunk

STATE_FILE = "2_salaries/US/UoI/state_2023.json"
IN_FILE = "2_salaries/US/UoI/uoi_2023.xlsx"

def main():
    # Create the state file
    if not os.path.exists(STATE_FILE):
        make_initial_state_file(IN_FILE, STATE_FILE)
    else:
        print(f"The file {STATE_FILE} already exists.")

    # Get a chunk of the state file
    chunk = get_fresh_chunk(STATE_FILE, 10)

    # run the process of scraping
    updated_chunk = scrape_faculty_information_for_chunk(chunk)
    
    # update the state file
    update_state_file(STATE_FILE, chunk)



if __name__ == "__main__":
    main()