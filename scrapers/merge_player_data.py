"""
merge_player_data.py 

Authors: Logan Seitz, Marcos Wofford, Joseph Saunderson
Date: 08/05/2025

This program merges two CSV files located in the ./data folder.
It does the following steps:
    1. Prompts the user to input the names of two CSV files and the column for player names.
    2. Loads both CSV files into dictionaries, using player names as the key.
    3. Merges the two dictionaries, combining stats for matching players and preserving all available data.
    4. Writes the merged result into a new CSV file.
        5. Cleans and formats the merged CSV by calling clean_and_format_merged_csv from data_sort
    6. Outputs the final cleaned and formatted player data into a .txt file.


"""


import csv  
import os  

# Import the custom data cleaning function from another script
from data_sort import clean_and_format_merged_csv

# Setting the directory where input and output CSV files are stored
DATA_DIR = "data"

# Function to load player data from a CSV file into a dictionary
def load_csv(filename, key):
    # Build the full path to the CSV file
    path = os.path.join(DATA_DIR, filename)
    
    # Open the CSV file
    with open(path, newline='', encoding='utf-8-sig') as f:
        # Read CSV rows as dictionaries (column names are keys)
        reader = csv.DictReader(f, skipinitialspace=True)
        
        rows = {}  # Dictionary to store player data
        for row in reader:
            name = row[key].strip()  # Extract and clean the player's name using the specified column
            
            # Rename the name column to a consistent 'name'
            row = {("name" if k == key else k): v for k, v in row.items()}
            
            # Store the row under the player name as key
            rows[name] = row
        
        return rows

# Function to merge two dictionaries of player data
def merge_dicts(base, new):
    for name, row in new.items():
        if name in base:
            # If the player already exists, update missing fields
            for k, v in row.items():
                if v:  # Only update if the new value is not empty
                    base[name][k] = v
        else:
            # If the player is new, just add the full row
            base[name] = row
    return base

# Interactive function to merge two CSVs and post-process
def interactive_merge():
    print("\n=== Player Data Merger (from ./data folder) ===")

    sources = []  # List to store input sources (filename and key)

    # Asking the user for two CSV files to merge
    for i in range(2):
        print(f"\nSource {i + 1}")
        filename = input("Enter CSV filename (ex: understat.csv): ").strip()
        key = input("Enter player name column header (ex: Name or player_name): ").strip()
        sources.append((filename, key))

    # Asking user for output filenames
    output_csv = input("\nEnter output CSV filename (ex: merged.csv): ").strip()
    output_txt = input("Enter output TXT filename (ex: merged_format_final_noname.txt): ").strip()

    # Creating full paths for saving the output files
    output_csv_path = os.path.join(DATA_DIR, output_csv)
    output_txt_path = os.path.join(DATA_DIR, output_txt)

    print("\nMerging files...")

    # Loading and merging data from the two sources
    merged_data = load_csv(sources[0][0], sources[0][1])
    merged_data = merge_dicts(merged_data, load_csv(sources[1][0], sources[1][1]))

    # Automatically building a consistent list of columns (field names) across all player rows
    fieldnames = ['name'] + sorted({k for row in merged_data.values() for k in row if k != 'name'})

    # Writing the merged data into a new CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(merged_data.values())

    print(f"Merged CSV saved to: {output_csv_path}")

    print("\n=== Data Cleanse ===")

    # Calling the cleaning function to format and save the merged data to a .txt file
    print("\nCleaning and formatting merged CSV...")
    clean_and_format_merged_csv(output_csv_path, output_txt_path)
    print(f"Final formatted TXT saved to: {output_txt_path}")


if __name__ == "__main__":
    interactive_merge()