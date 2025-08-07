
import os                    # For file/directory operations
import pandas as pd          # For data manipulation and CSV handling
from soccerdata import FBref # Third-party library for scraping FBref (Football Reference) data

def get_user_input():
    """
    This function:
    1. Gets league selection from user
    2. Shows examples of valid season formats
    3. Gets season(s) selection from user 
    
    """   

    print("Available League Examples:")
    print("- ENG-Premier League")    # English Premier League
    print("- ESP-La Liga")           # Spanish La Liga
    print("- ITA-Serie A")           # Italian Serie A
    print("- FRA-Ligue 1")           # French Ligue 1
    print("- GER-Bundesliga")        # German Bundesliga
    print("- Big 5 European Leagues Combined")  # Special combined dataset
    
    # Get league input from user and remove extra whitespace
    league = input("Enter the league ID (ex: ENG-Premier League): ").strip()
    
    # Display examples of valid season formats
    print("\nSeason Format Examples:")
    print("22-23")       # Two-digit year range format
    print("2023-24")     # Four-digit year range format
    
    # Get season input - can be single season or multiple seasons separated by commas
    season_input = input("Enter one or more seasons (comma-separated if multiple): ").strip()
    
    # Split the input by commas and clean up each season string
    seasons = [s.strip() for s in season_input.split(",")]
    
    return league, seasons

def save_to_csv(df, filename, output_dir="../data/fbref_output"):
    """
    
    This function:
    1. Creates the output directory if it doesn't exist
    2. Combines directory path with filename
    3. Saves DataFrame as CSV without row indices
    4. Confirms successful save with full file path
    """
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Combine directory path with filename to get full file path
    filepath = os.path.join(output_dir, filename)
    
    # Save DataFrame to CSV file
    # index=False means don't save row numbers as a column
    df.to_csv(filepath, index=False)
    
    print(f"Saved: {filepath}")

def main():
    """
    Main function:
    1. Gets user input for league and seasons
    2. Initializes FBref scraper with user's choices
    3. Scrapes three types of data:
       - Player season statistics
       - Team season statistics 
       - Match schedule/results 
    4. Saves each dataset to CSV files
    
    """
    
    # user's league and season 
    league, seasons = get_user_input()
    
   
    print(f"\n Initializing FBref scraper for league: {league}, seasons: {seasons}")
    
    # FBref scraper object
    scraper = FBref(leagues=league, seasons=seasons)

    # Get standard player statistics 
    player_stats = scraper.read_player_season_stats(stat_type='standard')
    
    # Create filename by cleaning league name and joining seasons
    
    player_filename = f"{league.replace(' ', '_')}_players_{'_'.join(seasons)}.csv"
    save_to_csv(player_stats, player_filename)
    
    # Get standard team statistics 
    team_stats = scraper.read_team_season_stats(stat_type='standard')
    
    # Create filename for team data
    team_filename = f"{league.replace(' ', '_')}_teams_{'_'.join(seasons)}.csv"
    save_to_csv(team_stats, team_filename)
    
  
    # Get match schedule and results 
    schedule = scraper.read_schedule()
    
    # Create filename for schedule data
    schedule_filename = f"{league.replace(' ', '_')}_schedule_{'_'.join(seasons)}.csv"
    save_to_csv(schedule, schedule_filename)
    
    print(f"Check the '../data/fbref_output' folder for your files")

if __name__ == "__main__":
    main()
