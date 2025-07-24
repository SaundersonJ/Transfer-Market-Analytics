# scraper_understat.py

import os                    # For file/directory operations
import pandas as pd          # For data manipulation and CSV handling
from ScraperFC import Understat  # Third-party library for scraping Understat football statistics

def select_league_and_season():
    """
    This function:
    1. Creates an Understat scraper object
    2. Checks which leagues are actually available 
    3. Shows available leagues and their seasons to the user
    4. Gets user's league choice through numbered selection
    5. Gets user's season choice through numbered selection
    
    """
    
    # Create Understat scraper object

    us = Understat()
    
    # List of football leagues that Understat covers
    possible_leagues = [
        "EPL",           # English Premier League
        "La Liga",       # Spanish La Liga
        "Bundesliga",    # German Bundesliga
        "Serie A",       # Italian Serie A
        "Ligue 1",       # French Ligue 1
        "RFPL",          # Russian Premier League
        "Primeira Liga", # Portuguese League
        "Eredivisie",    # Dutch League
        "Championship"   # English Championship
    ]
    
    # List to store leagues that are actually available with their seasons
    available_leagues = []
    
    # Check each potential league to see if it's currently available
    for league in possible_leagues:
        try:
            # Try to get valid seasons for this league
            seasons = us.get_valid_seasons(league)
            
            # If we got seasons back, this league is available
            if seasons:
                available_leagues.append((league, seasons))
        except Exception:
            # If there's any error, skip this league 
            continue
    
    print("Available leagues:")
    for i, (league, seasons) in enumerate(available_leagues, 1):
        # Show league name and all available seasons
        print(f"{i}. {league} (Seasons: {', '.join(seasons)})")
    
    # Get user's league choice by number
    league_choice = int(input("Select a league by number: "))
    
    # Extract the chosen league name and its available seasons
    league = available_leagues[league_choice - 1][0]
    valid_seasons = available_leagues[league_choice - 1][1]
    
    print(f"\nValid seasons for {league}:")
    for i, season in enumerate(valid_seasons, 1):
        print(f"{i}. {season}")
    
    # user's season choice by number
    season_choice = int(input("Select a season by number: "))
    
    # chosen season year
    year = valid_seasons[season_choice - 1]
    
    return league, year

def scrape_players_to_csv(league: str, year: str):
    """
    Function to scrape all player data for a specific league and season.
    This function:
    1. Creates Understat scraper object
    2. Scrapes data for all teams in the specified league/season
    3. Extracts player data from each team
    4. Combines all player data into one DataFrame
    5. Saves the combined data to a CSV file
    """
    
    # Create Understat scraper object
    us = Understat()
    
    print(f"\n Scraping all team/player data for {league} {year}...")
    
    # Scrape data for all teams in the specified league and season
    all_data = us.scrape_all_teams_data(year=year, league=league, as_df=True)
    
    # List to store individual team's player DataFrames
    player_dfs = []
    
    # Loop through each team's data
    for team, data in all_data.items():
        # Check if this team has player data and it's not empty
        if 'players_data' in data and not data['players_data'].empty:
            # Make a copy of the player data to avoid modifying original
            df = data['players_data'].copy()
            
            # Add a 'team' column so we know which team each player belongs to
            df['team'] = team
            
            # Add this team's player data to our collection
            player_dfs.append(df)
    
    # Check if we found any player data at all
    if not player_dfs:
        print(" No player data found.")
        return
    
    # Combine all individual team DataFrames into one large DataFrame
    all_players_df = pd.concat(player_dfs, ignore_index=True)
    
    # safe filenames by replacing problem characters
    safe_league = league.replace("/", "_").replace(" ", "_")
    safe_year = year.replace("/", "_")
    
    # Create the output directory structure: data/understat/
    output_dir = os.path.join("data", "understat")
    # Create directory if it doesn't exist 
    os.makedirs(output_dir, exist_ok=True)
    
    # data/understat/EPL_2023_players.csv
    filename = os.path.join(output_dir, f"{safe_league}_{safe_year}_players.csv")
    
    # Save the combined DataFrame to CSV file
    all_players_df.to_csv(filename, index=False)
    
    print(f" Saved player data to: {filename}")
    print(f" Total players saved: {len(all_players_df)}")

def main():
    """
    Main function that orchestrates the entire scraping process.
    
    This is the entry point of the program that:
    1. Gets user's league and season selection
    2. Scrapes the player data for that selection
    3. Saves everything to a CSV file
    """
    # Get user's choice of league and season
    league, year = select_league_and_season()
    
    # Scrape and save the data
    scrape_players_to_csv(league, year)

if __name__ == "__main__":
    main()
