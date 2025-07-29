import os
import pandas as pd
from ScraperFC.transfermarkt import Transfermarkt
from tqdm import tqdm

class TransfermarktDataScraper:
    """
    A class to scrape player data from Transfermarkt using the ScraperFC library.
    """

    # supported leagues by this scraper.
    VALID_LEAGUES = [
        'EPL', 'EFL Championship', 'EFL1', 'EFL2', 'Bundesliga', '2.Bundesliga',
        'Serie A', 'Serie B', 'La Liga', 'La Liga 2', 'Ligue 1', 'Ligue 2',
        'Eredivisie', 'Scottish PL', 'Super Lig', 'Turkish Super Lig',
        'Jupiler Pro League', 'Liga Nos', 'Russian Premier League',
        'Brasileirao', 'Argentina Liga Profesional', 'MLS',
        'Primavera 1', 'Primavera 2 - A', 'Primavera 2 - B', 'Campionato U18'
    ]

    def __init__(self, max_players=None):
        """
        Function to initialize the TransfermarktDataScraper.

        Parameters:
        - max_players (int or None): limit on the number of players to scrape.
        """
        self.max_players = max_players  # How many players to scrape (None = all)
        self.league = None              # League to scrape (e.g., 'EPL')
        self.season = None              # Season to scrape (e.g., '22/23')
        self.scraper = None             # Instance of the Transfermarkt scraper

    def initialize_scraper(self):
        """
        Function to create an instance of the Transfermarkt scraper from ScraperFC.
        """
        if not self.scraper:
            self.scraper = Transfermarkt()

    def get_player_links(self):
        """
        Function to fetch player profile URLs for the given league and season.
        Returns:
        - A list of player profile links (limited by max_players if set).
        """
        if not self.scraper or not self.league or not self.season:
            raise ValueError("Initialize scraper and set league/season first")

        # returning the list of player URLs from Transfermarkt
        return self.scraper.get_player_links(self.season, self.league)[:self.max_players]

    def scrape_single_player(self, player_link):
        """
        Function to scrape a single player's data.
        Returns:
        - A pandas DataFrame with player data, or None if scraping failed.
        """
        try:
            return self.scraper.scrape_player(player_link)
        except Exception:
            # Exception so that we may skip any players that fail to scrape
            return None  

    def scrape_players(self):
        """
        Function to scrape all players from the selected league and season.
        Returns:
        - A combined pandas DataFrame with all player data, or an empty DataFrame if none were scraped.
        """
        self.initialize_scraper()  # Ensure scraper is ready

        # Getting all the player URLs
        player_links = self.get_player_links()

        # List of all player data frames
        all_players = []  

        # Loop through each player link and scrape the data
        for link in tqdm(player_links, desc="Transfermarkt scraping"):
            player_data = self.scrape_single_player(link)
            if player_data is not None:
                all_players.append(player_data)

        # Combining all player DataFrames into one
        if all_players:
            return pd.concat(all_players, ignore_index=True)

        # empty DataFrame returned if nothing scraped
        return pd.DataFrame() 

    def scrape_and_save_players(self):
        """
        Function to scrape all players and return the DataFrame.
        """
        return self.scrape_players()
