"""
scraper_understat.py

This program defines a class for scraping team and player xG/xA data from Understat using the ScraperFC library.
It supports scraping specific leagues and seasons, returning structured player-level data in a pandas DataFrame.

Author: Marcos Wofford
"""



import os
import pandas as pd
from ScraperFC import Understat

class UnderstatDataScraper:
    """
    A class to scrape team and player xG/xA data from Understat using ScraperFC.
    """

    # These are the supported leagues that Understat can scrape
    POSSIBLE_LEAGUES = [
        "EPL", "La Liga", "Bundesliga", "Serie A", "Ligue 1",
        "RFPL", "Primeira Liga", "Eredivisie", "Championship"
    ]

    def __init__(self):
        """
        Initializing the UnderstatDataScraper with placeholders for league and season.
        """
        self.league = None    
        self.season = None   
        self.scraper = None    

    def initialize_scraper(self):
        """
        Function to initialize the Understat scraper instance
        """
        if not self.scraper:
            self.scraper = Understat()

    def scrape_all_teams_data(self):
        """
        Function to scrape all team and player data for a given league and season.
        Returns A dictionary where each key is a team name, and each value is a dictionary
          of that team’s data including 'players_data' 
        """
        if not self.scraper or not self.league or not self.season:
            raise ValueError("Initialize scraper and set league/season first")

        return self.scraper.scrape_all_teams_data(
            year=self.season,
            league=self.league,
            as_df=True 
        )

    def extract_players_data(self, all_teams_data):
        """
        Function to pull out the player-level data from all the team data.
        Returns: A single pandas DataFrame containing all player data, with team info.
        """
        player_dfs = []

        for team, data in all_teams_data.items():
            if 'players_data' in data and not data['players_data'].empty:
                df = data['players_data'].copy()
                df['team'] = team  # add team name to each player's row
                player_dfs.append(df)

        if player_dfs:
            return pd.concat(player_dfs, ignore_index=True)
        # returning empty DataFrame if nothing scraped
        return pd.DataFrame()  

    def scrape_players(self):
        """
        Function with complete flow to scrape player data:
        - Initialize scraper
        - Get all teams' data
        - Extract player data

        Returns: pandas DataFrame with player-level stats across all teams
        """
        self.initialize_scraper()
        all_teams_data = self.scrape_all_teams_data()
        return self.extract_players_data(all_teams_data)
