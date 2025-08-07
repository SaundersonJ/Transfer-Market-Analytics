"""
Author: Marcos Wofford
Date: 08/05/2025

This script allows users to interactively scrape player data from three major football data sources: 
     FBref, Transfermarkt, Understat

Each source supports multiple leagues and seasons. After collecting the data, users can merge and clean
CSV files to produce a single, unified dataset.

How to use:
------
1. Pip Install SoccerData and ScraperFC Libraries. 

2. Run the script directly:
    $ python runScrapers.py

3. Follow the prompts to:
   - Select which sources to scrape
   - Choose the league and season format, appropriate for each source
   - Merge two scraped CSV files (Only Transfermarkt and Understat are used for demo purposes) 

Requirements:
-------------
- The following modules are needed:
    - fbref_data.py (defines FBrefDataScraper)
    - scraper_transfermarkt.py (defines TransfermarktDataScraper)
    - scraper_understat.py (defines UnderstatDataScraper)
    - merge_player_data.py (defines interactive_merge function)

- Output files will be saved in: ./data/

"""

import os
import re
from merge_player_data import interactive_merge

class RunScrapers:
    """
    Class to manage running scrapers for different soccer data sources:
    FBref, Transfermarkt, and Understat. Each scraper collects data for a specific
    league and season and saves the results as CSV files.
    """

    def __init__(self, max_players = 10, output_dir="data"):
        """
        Function to initialize the RunScrapers class with settings for output directory
        and number of players to scrape for Transfermarkt.
        """
        self.max_players = max_players
        self.output_dir = output_dir

        # Lists of which leagues are available for each source
        self.fbref_leagues = ['Big 5 European Leagues Combined','ENG-Premier League', 
                              'ESP-La Liga','FRA-Ligue 1','GER-Bundesliga',
                              'INT-European Championship']
        self.transfermarkt_leagues = [
            'EPL', 'EFL Championship', 'EFL1', 'EFL2',         
            'Bundesliga', '2.Bundesliga',                                                
            'La Liga', 'MLS', 'Campionato U18'
        ]
        self.understat_leagues = ["EPL", "La Liga", "Bundesliga", "Serie A", "Ligue 1",
        "RFPL", "Primeira Liga", "Eredivisie", "Championship" ]

    @staticmethod
    def sanitize(s):
        """
        Function to replace any characters in a string that are not allowed in filenames.
        Returns: A safe version of the string for file naming.
        """
        return re.sub(r'[\\/:"*?<>|]+', '-', s)

    def run_fbref_only(self, league, season):
        """
        Run the FBref scraper for a single league and season.
        Returns: players (DataFrame): Player data collected.
        """
        from fbref_data import FBrefDataScraper
        os.makedirs(self.output_dir, exist_ok=True)

        # Setting up scraper
        fbref_scraper = FBrefDataScraper()
        fbref_scraper.league = league
        fbref_scraper.seasons = [season]
        fbref_scraper.initialize_scraper()

        # Scraping player, team, and schedule data
        players, teams, schedule = fbref_scraper.scrape_all_data()

        # Saving results as CSV
        safe_league = self.sanitize(league)
        safe_season = self.sanitize(season)
        players.to_csv(f"{self.output_dir}/fbref_players_{safe_league}_{safe_season}.csv", index=False)
        teams.to_csv(f"{self.output_dir}/fbref_teams_{safe_league}_{safe_season}.csv", index=False)
        schedule.to_csv(f"{self.output_dir}/fbref_schedule_{safe_league}_{safe_season}.csv", index=False)
        print("FBref data saved")

        return players

    def run_transfermarkt_only(self, league, season):
        """
        Function to run the Transfermarkt scraper for a single league and season
        Returns: df (DataFrame): Player data collected.
        """
        from scraper_transfermarkt import TransfermarktDataScraper
        os.makedirs(self.output_dir, exist_ok=True)

        # Setting up scraper
        tm_scraper = TransfermarktDataScraper(max_players=self.max_players)
        tm_scraper.league = league
        tm_scraper.season = season
        tm_scraper.initialize_scraper()

        # Scraping and save player data
        df = tm_scraper.scrape_and_save_players()
        df["source"] = "transfermarkt"

        # Saving CSV
        safe_league = self.sanitize(league)
        safe_season = self.sanitize(season)
        df.to_csv(f"{self.output_dir}/transfermarkt_{safe_league}_{safe_season}.csv", index=False)
        print("Transfermarkt data saved")

        return df

    def run_understat_only(self, league, season):
        """
        Function to run the Understat scraper for a single league and season.
        Returns: df (DataFrame): Player data collected.
        """
        from scraper_understat import UnderstatDataScraper
        os.makedirs(self.output_dir, exist_ok=True)

        # Setting up scraper
        us_scraper = UnderstatDataScraper()
        us_scraper.league = league
        us_scraper.season = season
        us_scraper.initialize_scraper()

        # Scraping and save player data
        df = us_scraper.scrape_players()
        df["source"] = "understat"

        # Saving CSV
        safe_league = self.sanitize(league)
        safe_season = self.sanitize(season)
        df.to_csv(f"{self.output_dir}/understat_{safe_league}_{safe_season}.csv", index=False)
        print("Understat data saved")

        return df
        
    def run_merge(self):
        """ Function to merge the collected data files into one. """
        interactive_merge()

    def run_interactive(self):
        """
        Function to run command-line prompts to choose and run any of the three scrapers:
        FBref, Transfermarkt, and Understat. Each will prompt for league and season,
        then scrape and save the data.
        """
        fbref_df = tm_df = us_df = None

        # Prompt for FBref scraping
        if input("\nRun FBref scraper? (y/n): ").strip().lower() == 'y':
            print("FBref leagues:", ", ".join(self.fbref_leagues))
            print("Season format example: 22-23")
            league = input("\nFBref - Enter league: ").strip()
            season = input("FBref - Enter season: ").strip()
            fbref_df = self.run_fbref_only(league, season)

        # Prompt for Transfermarkt scraping
        if input("\nRun Transfermarkt scraper? (y/n): ").strip().lower() == 'y':
            print("Transfermarkt leagues:", ", ".join(self.transfermarkt_leagues))
            print("Season format example: 22/23 [MLS uses the full year like '2024' ONLY] ")
            league = input("\nTransfermarkt - Enter league: ").strip()
            season = input("Transfermarkt - Enter season: ").strip()
            tm_df = self.run_transfermarkt_only(league, season)

        # Prompt for Understat scraping
        if input("\nRun Understat scraper? (y/n): ").strip().lower() == 'y':
            print("Understat leagues:", ", ".join(self.understat_leagues))
            print("Season format example: 2022/2023")
            league = input("\nUnderstat - Enter league: ").strip()
            season = input("Understat - Enter season: ").strip()
            us_df = self.run_understat_only(league, season)


        # Returning all dataframes 
        return fbref_df, tm_df, us_df


if __name__ == "__main__":
    runner = RunScrapers()
    runner.run_interactive()
    runner.run_merge()