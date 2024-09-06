import json
import pandas as pd
import numpy as np


def update_subsequent_department(df, selected_name, new_department):
    # Find the index of the selected name
    selected_index = df[df['Name'] == selected_name].index
    
    # Check if the name is found and it's not the last one in the DataFrame
    if not selected_index.empty and selected_index[0] < len(df) - 1:
        # Update the department of the subsequent name
        df.at[selected_index[0] + 1, 'Department'] = new_department
        return "Updated"
    else:
        return None  
    
def get_subsequent_department(df, selected_name):
    # Find the index of the selected name
    selected_index = df[df['Name'] == selected_name].index
    
    # Check if the name is found and it's not the last one in the DataFrame
    if not selected_index.empty and selected_index[0] < len(df) - 1:
        # Get the department of the subsequent name
        subsequent_department = df.iloc[selected_index[0] + 1]['Department']
        return subsequent_department
    else:
        return None
        

def get_state_file(state_file:str):
    with open(state_file, 'r') as file:
        data = json.load(file)
    return data

def merge_data(excelpath:str):
    df_main_2023 = pd.read_excel('Iowa_Salaries2023_2.xlsx')
    df_excel = pd.read_excel(excelpath)
    name_list = df_excel["Name"].tolist()
    name_list_2023 = df_main_2023["Name"].tolist()
    for name in name_list:
        formatted_name = normalize_name(name)
        dept_excel = get_subsequent_department(df_excel,name)
        if get_subsequent_department is not None:
            if formatted_name in name_list_2023:
                print("Found a match!")
                status =update_subsequent_department(df_main_2023,formatted_name,dept_excel)
                if status is not None:
                    print(f"Updated")
                else:
                    print(f"No subsequent name found after '{name}'.")
                    
    df_main_2023.to_excel('Iowa_Salaries2023_2.xlsx')
    
def normalize_name(scraped_name):
    parts = scraped_name.upper().replace('.', '').split()
    
    if len(parts) == 2:
        first_name, last_name = parts
        return f"{last_name},{first_name}"
    elif len(parts) > 2:
        first_name_middle = ' '.join(parts[:-1])  # Join all parts except the last one for the first name + middle initial
        last_name = parts[-1]  # Last part is the last name
        return f"{last_name},{first_name_middle}"
    else:
        return scraped_name.upper()