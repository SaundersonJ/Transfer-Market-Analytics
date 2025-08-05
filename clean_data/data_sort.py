# Joseph Saunderson
# 07/30/2025
# This program takes input of a csv file of combined stats on players and cleans it up to be in the correct format
# k-means clustering algorithm and then outputs it to a txt file.

# data_sort.py

import pandas as pd

def remove_columns_nan(data, columns_to_remove):
    data_cleaned = data.drop(columns=columns_to_remove)
    new_order = ['Age', 'time', 'xA', 'xG', 'Value']
    return data_cleaned[new_order].dropna()

def convert_price(dataframe, outfile):
    for line in dataframe:
        price = line[-1]
        price = price.strip('€')
        if price[-1] == 'm':
            price = price.strip('m').split('.')
            price = price[0] + price[1] + "0000"
        elif price[-1] == 'k':
            price = price.strip('k')
            price += "000"
        line[-1] = price
        output_string = ' '.join(line)
        outfile.write(output_string + '\n')

def clean_and_format_merged_csv(input_csv, output_txt):
    merged = pd.read_csv(input_csv)
    columns_to_remove = [
        "name", "Citizenship", "Contract expiration", "DOB", "Height (m)", "ID", 
        "Joined", "Last club", "Market value history", "Nationality", "Other positions", 
        "Position", "Since", "Team", "Transfer history", "Value last updated", 
        "assists", "games", "goals", "id", "key_passes", "npg", "npxG", "position", 
        "red_cards", "shots", "source", "team", "team_title", "xGBuildup", "xGChain", "yellow_cards"
    ]
    cleaned_df = remove_columns_nan(merged, columns_to_remove).astype(str)
    with open(output_txt, 'w') as outfile:
        convert_price(cleaned_df.values.tolist(), outfile)
