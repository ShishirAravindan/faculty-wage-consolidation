#!.finPayVenv/bin/python3

import pandas as pd
import json

def make_initial_state_file(file_path, json_out_path):
    """Get unique names from files [...]"""
    df = pd.read_excel(file_path)
    data = []
    unique_names = df['Name'].dropna().apply(lambda x: x.strip()).unique()
    for name in unique_names:
        year = df[df['Name'] == name].iloc[0]['Year']
        person = {
            "name": name,
            "year": year,
            "faculty": None
        }
        data.append(person)
    with open(json_out_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)
        print(f"JSON data has been written to {json_out_path}")
    

def get_fresh_chunk(state_file_path, chunk_size):
    with open(state_file_path, 'r') as json_file:
        state_data = json.load(json_file)
    
    chunk = []
    null_found = False
    
    for entry in state_data:
        if entry['faculty'] is None:
            if not null_found: null_found = True
            chunk.append(entry)
            if len(chunk) == chunk_size: break
        elif null_found:
            continue
    
    return chunk

def update_state_file(state_file_path, new_data):
    pass
    


# make_initial_state_file('2_salaries/UoI/uoi_2023.xlsx', '2_salaries/UoI/state_2023.json')
