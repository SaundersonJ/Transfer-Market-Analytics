# Joseph Saunderson
# 07/30/2025
# This program takes input of a csv file of combined stats on players and cleans it up to be in the correct format
# k-means clustering algorithm and then outputs it to a txt file.

import pandas as pd

def RemoveColumsNaN(data, columns_to_remove):
    data_cleaned = data.drop(columns=columns_to_remove)
    new_order = ['Age', 'time', 'xA', 'xG', 'Value']
    return data_cleaned[new_order].dropna()

def ConvertPrice(dataframe, outfile):
    for line in dataframe:
        price = line[-1]
        price = price.strip('€')
        if price[-1] == 'm':
            price = price.strip('m').split('.')
            price = price[0] + price[1] + "0000"
        elif price[-1] == 'k':
            price = price.strip('k')
            price += "000"
        #print(price)
        line[-1] = price
        output_string = ' '.join(line)
        outfile.write(output_string + '\n')

#opens file, lists columns to remove, calls function to remove columns and rows with NaN values and sends this data frame into a function that formats the price correctly and then writes it to a txt file with each record on a single line with each stat separated by a space
merged = pd.read_csv("merged_players.csv")
columns_to_remove = ["name", "Citizenship", "Contract expiration", "DOB", "Height (m)", "ID", "Joined", "Last club", "Market value history", "Nationality", "Other positions", "Position", "Since", "Team", "Transfer history", "Value last updated", "assists", "games", "goals", "id", "key_passes", "npg", "npxG", "position", "red_cards", "shots", "source", "team", "team_title", "xGBuildup", "xGChain", "yellow_cards"]
#columns_to_remove = ["Citizenship", "Contract expiration", "DOB", "Height (m)", "ID", "Joined", "Last club", "Market value history", "Nationality", "Other positions", "Position", "Since", "Team", "Transfer history", "Value last updated", "assists", "games", "goals", "id", "key_passes", "npg", "npxG", "position", "red_cards", "shots", "source", "team", "team_title", "xGBuildup", "xGChain", "yellow_cards"]


#print(merged)
merged_text_outfile = open("merged_format_final_noname.txt", 'w')
ConvertPrice(RemoveColumsNaN(merged, columns_to_remove).astype(str).values.tolist(), merged_text_outfile)
merged_text_outfile.close()

