"""
scraper_fbref.py

This program defines a class to scrape player, team, and schedule data from FBref using the soccerdata library.
The data is returned as pandas DataFrames with source identifiers included.

Author: Marcos Wofford
"""

import os
from soccerdata import FBref

class FBrefDataScraper:
    """
    A class to scrape football data (player stats, team stats, schedule)
    from the FBref website using the soccerdata library.
    """

    def __init__(self):
        """
        Function to initialize the FBrefDataScraper instance with default values.
        Sets the scraper, league, and seasons to None until configured.
        """
        self.scraper = None
        self.league = None
        self.seasons = None

    def initialize_scraper(self):
        """
        Function to creates an instance of the FBref scraper using the given league and season. 
        called after setting `self.league` and `self.seasons`.
        """
        self.scraper = FBref(leagues=self.league, seasons=self.seasons)

    def scrape_all_data(self):
        """
        Scrapes all available data for the specified league and season:
        - Player stats
        - Team stats
        - Match schedule
        Returns:
        - Stats for individual players.
        - Aggregate stats for teams.
        -  Match schedule and results.
        """
        # Scrape player statistics
        players = self.scraper.read_player_season_stats()

        # Scrape team statistics
        teams = self.scraper.read_team_season_stats()

        # Scrape schedule and results
        schedule = self.scraper.read_schedule()

        # Adding a column to show where each DataFrame came from
        players["source"] = "fbref_players"
        teams["source"] = "fbref_teams"
        schedule["source"] = "fbref_schedule"

        return players, teams, schedule
