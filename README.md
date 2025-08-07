# Transfer-Market-Analytics
This project focuses on web scraping detailed information about soccer players, including performance statistics, positions, team history, and past transfer prices. The data will be organized in a structured database and analyzed to identify patterns that can be used to create predictions for future transfer prices. By developing custom metrics based on this information such as playing time, goal contribution, or age at the time of transfer the project aims to find the factors that influence transfer pricing and report trends within the player market. 

Objectives:
We are fans of soccer and would like to learn how to work with web scaping and perform data analysis in Python over the course of this class. This project is very flexible as we can scale it up to training a neural network that analyzes player stats to predict transfer prices, or scale it down to just scraping data and building a database to explore basic correlations. 

Dependencies:

Libraries: 
Numpy (data structures, and numerical operations) 
Pandas (data manipulation, analysis, and cleaning) 
Soccerdata (Scrapes and formats soccer data from Fbref) 
ScraperFC (Scraper framework to pull football data from Transfermarkt and Understat) 


Datasets: fbRef, Transfermarkt, understat



# Explanation of how to run project


## Step 1: Scraping the Data


For the following files:  

- `runScrapers.py` : The main script that coordinates scraping and merging  
- `scraper_understat.py`  : Contains the class for scraping Understat data  
- `scraper_transfermarkt.py` : Contains the class for scraping Transfermarkt data  
- `fbref_data.py`  : Contains the class for scraping FBref data
- `merge_player_data.py`  : Handles the logic for merging two scraped CSVs  

These programs work together to scrape football player and team data from three public sources: **Transfermarkt**, **Understat**, and **FBref**, and then merge the results into a single dataset. The scraping logic is implemented using the **ScraperFC** and **SoccerData** Python libraries.

# runScrapers.py-merge_player_data.py

1. Before running the scrapers, install the ScraperFC and SoccerData libraries using pip.
   
3. To run the scraping process, execute the `runScrapers.py` file. This script provides prompts where you can choose which sources to scrape, specify the league and season, and merge output files.
   
5. Each prompt in `runScrapers.py` calls the respective scraper class:  
   - FBref prompts call `FBrefDataScraper` from `fbref_data.py`  
   - Transfermarkt prompts call `TransfermarktDataScraper` from `scraper_transfermarkt.py`
      - Currently, `scraper_transfermarkt` will only scrape a set amount of 10 players.
      - If you would like to scrape the full amount, you may change the `max_players` value to `None` in the `__init__` function of the `runScrapers` class (within the `runScrapers` file). 
   - Understat prompts call `UnderstatDataScraper` from `scraper_understat.py`
     
6. You can run one, two, or all three scrapers. For each source, you will be asked to enter the correct league and season format. After scraping, you will also have the option to merge two CSV files from the output directory.
   
7. The merge in `runScrapers.py` calls the `interactive_merge()` function from `merge_player_data.py`, which handles combining the two selected CSV files and formatting the output.
   
8. After merging, `interactive_merge()` calls cleaning function `clean_and_format_merged_csv()` from `data_sort.py`. This step standardizes the merged data and prepares it for the implemented prediction algorithm.
    
9. All CSVs and cleaned TXT files are automatically saved to the `data` folder. Filenames include the source, league, and season.

   
   
## Step 2: Cleaning the Data and Implementing Prediction Algorithm 

# data_sort.py-reassign_labels.py
1. data_sort.py runs and outputs merged_players.txt.

2. final_prep.py takes merged_players.txt as input and converts the prices/labels (the last number on each row) into 60 ranges. It saves these ranges to ranges.txt and replaces each price/label with the midpoint of the corresponding range. The updated records are output to the file merged_players_final.txt.

3. kmeans.py takes merged_players_final.txt, the number of centroids k, and the iteration number as input. The K-means algorithm uses the text file split by split.bash into training and validation data. Below is the recommended command to run this. The K-means algorithm is run 100 times. kmeans.py defines centroids, learns patterns from the training data, assigns cluster labels to each centroid, and classifies the validation data. It then saves the centroids and cluster labels to text files:

data_to_file(cluster_labels, "cluster_labels_" + str(iteration) + "_" + str(k) + ".txt") #Where iteration is the current iteration and k is the number of clusters
data_to_file(centroids, "centroids" + str(iteration) + "_" + str(k) + ".txt")

The command to run these iterations also saves the count of validation records that K-means classified correctly to another text file. Below is the command to run kmeans.py:

for ((x=0;x<100;x++)); do echo "cat merged_players_final.txt | ./split.bash 40 python3 kmeans.py 50 ${x} > answer_50_clusters_${x}.txt"; done | ./parallelize.bash 
#This runs kmeans.py 100 times, where merged_players_final.txt is split such that 40 lines are used as validation data and the rest as training data. 50 is the number of centroids, and ${x} is the current iteration.

By running this, you generate 100 cluster_labels, centroids, and answer files.
To run the bash files in the command: split.bash and parallelize.bash, you need to grant execute permissions. Use the following command: chmod +x <filename>

4. after_kmeans.sh creates folders for cluster labels, centroids, and answer files. It moves all related files into their respective directories, moves avg.py into the answers directory, runs it, and writes the output to average_answer.txt. To run after_kmeans.sh, use the following command:
./after_kmeans.sh 50 #Where 50 is the number of centroids you used in the kmeans algorithm. You will also need to give this file permission to execute: chmod +x <filename>

5. after_kmeans.sh calls avg.py. Once avg.py is moved to the answers directory by after_kmeans.sh, it is run. It takes the 100 answer files as input and outputs the index and value of the iteration that classified the most validation data correctly, as well as the average number classified correctly, to both average_answer.txt and the terminal.

6. I identified the centroid and cluster label files that correctly classified the most validation data: centroids31_65.txt and cluster_labels_31_65.txt. I manually determined the iteration number (31) for each file. These files were generated using 65 centroids.

7. reassign_labels.py takes ranges.txt and cluster_labels_31_65.txt as input, determines the range into which each cluster label falls, and outputs the new cluster label ranges to cluster_labels_ranges_31_65.txt.

8. centroids31_65.txt and cluster_labels_ranges_31_65.txt are then used for classifying user input dynamically when the main program runs. These steps are not repeated each time the user interacts with the program. They are performed once to generate the centroids and cluster label ranges that will be used for classification. These steps can be repeated to update the classification logic using different parameters, but the scripts would need to be modified to accept any input files, rather than the specific ones used in our current run. You can use the files provided mentioned in the above steps. 

## Step 3: User Interface to Request Price Prediction

# Get_Searched_Prediction.py

**Prerequisites:**  
- `merged_players.csv` (or your updated player database)  
- Centroid file (default `centroids31_65.txt`)  
- Cluster labels file (default `cluster_labels_31_65.txt`)  
- Ranges file (default `ranges.txt`)

1. **Usage**  
   Simply run:
   python Get_Searched_Prediction.py

1. running the program on the user end is fairly straight foreward and simple. There are no direct third-party dependencies for this part of the program. This part of the program interfaces with the other pieces through files that were generated. Simply run 'python Get_Searched_Prediction.py', and follow the prompts.
   
Note: (you can reference the merged_players.csv for searchable players the program can access)

2. In order to update the database of players or centroids being utilized to make predictions, you can simply change the filenames being assigned to the variables "default_db_file, default_centroids, default_labels, and default_ranges" in the main function definition. The program needs these files to function properly. 
   
3. Each of these files comes from previous steps in the readme and can be updated in the future for increased accuracy, greater generalization, and a larger database to search from.



