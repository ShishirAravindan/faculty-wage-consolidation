#!.finPayVenv/bin/python3

import pandas as pd
import json


def make_initial_state_file(file_path, json_out_path):
    """Get unique names from files [...]"""
    df = pd.read_excel(file_path)
    df['Name'] = df['Name'].apply(lambda x: x.strip())
    df = df.drop_duplicates()
    grouped_df = df.groupby('Name')['Year'].apply(list).reset_index()
    grouped_df['Department'] = None
    grouped_list = grouped_df.to_dict(orient='records')
    with open(json_out_path, 'w') as json_file:
        json.dump(grouped_list, json_file, indent=2)
        print(f"JSON data has been written to {json_out_path}")


def get_fresh_chunk(state_file_path, chunk_size):
    with open(state_file_path, 'r') as json_file:
        state_data = json.load(json_file)

    chunk = {}
    null_found = False
    for entry in state_data:
        if entry['Department'] is None:
            if not null_found: null_found = True
            chunk[entry['Name']] = None
            if len(chunk) == chunk_size: break
        elif null_found:
            continue
    return chunk


def update_state_file(state_file_path, new_data):
    with open(state_file_path, 'r') as json_file:
        state_data = json.load(json_file)

    for entry in state_data:
        if entry['Name'] in new_data:
            entry['Department'] = new_data[entry['Name']]

    with open(state_file_path, 'w') as json_file:
        json.dump(state_data, json_file, indent=2)
        print(f"JSON data has been updated in {state_file_path}")


#make_initial_state_file('2_salaries/UoI/uoi_2023.xlsx', '2_salaries/UoI/state_2023.json')
#make_initial_state_file('../IOWAsalary1993-2023upd.xlsx', '2_salariesUoIstate_2023.json')
# chunk = get_fresh_chunk('data/2_salariesUoIstate_2023.json', 5)
# print(chunk)
