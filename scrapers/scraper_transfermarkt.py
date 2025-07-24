
import os                                    # For file/directory operations
import pandas as pd                          # For data manipulation and CSV handling
from ScraperFC.transfermarkt import Transfermarkt  # Third-party library for scraping Transfermarkt data

# List of all supported football leagues that can be scraped
VALID_LEAGUES = [
    'EPL', 'EFL Championship', 'EFL1', 'EFL2',           # English leagues
    'Bundesliga', '2.Bundesliga',                        # German leagues
    'Serie A', 'Serie B',                                # Italian leagues
    'La Liga', 'La Liga 2',                              # Spanish leagues
    'Ligue 1', 'Ligue 2',                                # French leagues
    'Eredivisie', 'Scottish PL',                         # Dutch and Scottish leagues
    'Super Lig', 'Turkish Super Lig',                    # Turkish leagues
    'Jupiler Pro League', 'Liga Nos',                    # Belgian and Portuguese leagues
    'Russian Premier League',                            # Russian league
    'Brasileirao', 'Argentina Liga Profesional',         # South American leagues
    'MLS',                                               # American league
    'Primavera 1', 'Primavera 2 - A', 'Primavera 2 - B', # Italian youth leagues
    'Campionato U18'                                     # Youth league
]

def get_user_input():
    """
    Function to get league and season input from the user.
    
    This function:
    1. Displays all valid leagues to the user
    2. Asks user to select a league
    3. Validates the league selection
    4. Shows available seasons for the selected league
    5. Asks user to select a season
    6. Validates the season selection
    
    """
    
    # Display all available leagues to help user make correct choice
    print(" Valid Transfermarkt Leagues:")
    for lg in VALID_LEAGUES:
        print(f"- {lg}")
    
    # Get league input from user and remove any extra spaces
    league = input("\nEnter a league exactly as listed above (ex: EPL): ").strip()
    
    # Check if the entered league is valid, raise error if not
    if league not in VALID_LEAGUES:
        raise ValueError(f" '{league}' is not a valid league.")
    
    # Create Transfermarkt scraper object to get available seasons
    tm = Transfermarkt()
    valid_seasons = tm.get_valid_seasons(league)  # Get all available seasons for this league
    
    # Display available seasons for the selected league
    print("\n Valid Seasons for", league)
    for season_str in valid_seasons:
        print(f"- {season_str}")
    
    # Get season input from user
    year = input("Enter a valid season from above (ex: 22/23): ").strip()
    
    # Validate the season selection
    if year not in valid_seasons:
        raise ValueError(f" {year} is not a valid season for {league}.")
    
    # Return both league and year for use in main function
    return league, year

def save_to_csv(df, filename, output_dir="data/transfermarkt"):
    """
    Function to save a pandas DataFrame to a CSV file.
    
    This function:
    1. Creates the output directory if it doesn't exist
    2. Saves the DataFrame as a CSV file
    3. Prints confirmation message
    """
    
    # Get the directory path from the filename
    output_dir = os.path.dirname(filename)
    
    # Create directory if it doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save DataFrame to CSV without including row indices
    df.to_csv(filename, index=False)
    
    print(f"Data saved to {filename}")

def scrape_players_safe(tm, year, league):
    """
    Function to safely scrape player data from Transfermarkt.
    
    This function:
    1. Gets links to all player pages for the specified league/season
    2. Limits to first 12 players (for demo)
    3. Attempts to scrape each player's data
    4. Handles errors (continues if one player fails)
    5. Combines all successful results into one DataFrame
    """
    
    # progress bar library for visual feedback
    from tqdm import tqdm
    
    # Get links to all player pages, but limit to first 12 for  demo
    player_links = tm.get_player_links(year, league)[:12]
    
    # List to store DataFrames from each successfully scraped player
    all_players = []
    
    # Loop through each player link with a progress bar
    for link in tqdm(player_links):
        try:
            # scrape individual player data
            df = tm.scrape_player(link)
            all_players.append(df)  # Add successful result to our list
        except Exception:
            # If scraping fails for player, skip and continue
            pass
    
    # Combine all individual player DataFrames into one large DataFrame
    if all_players:
        return pd.concat(all_players, ignore_index=True)
    else:
        # Return empty DataFrame if no players were successfully scraped
        return pd.DataFrame()

def main():
    """
    Main function:
    1. Gets user input for league and season
    2. Creates Transfermarkt scraper object
    3. Scrapes player data
    4. Saves results to CSV file
    """
    
    # Get league and season from user
    league, year = get_user_input()
    
    print(f"\n Scraping Transfermarkt data for {league} ({year})...")
    
    # Create Transfermarkt scraper object
    tm = Transfermarkt()
    
    # Scrape player data 
    df_players = scrape_players_safe(tm, year, league)
    
    # Show how many players were successfully scraped
    print(f"Retrieved {len(df_players)} players.")
    
    # Create filename by replacing dashes with underscores and adding file extension
    filename = f"{league.replace('-', '_')}_players_{year}.csv"
    
    # Save the scraped data to CSV file
    save_to_csv(df_players, filename)

if __name__ == "__main__":
    main()
