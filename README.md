# Transfer-Market-Analytics
This project focuses on web scraping detailed information about soccer players, including performance statistics, positions, team history, and past transfer prices. The data will be organized in a structured database and analyzed to identify patterns that can be used to create predictions for future transfer prices. By developing custom metrics based on this information such as playing time, goal contribution, or age at the time of transfer the project aims to find the factors that influence transfer pricing and report trends within the player market. 

Objectives:
We are fans of soccer and would like to learn how to work with web scaping and perform data analysis in Python over the course of this class. This project is very flexible as we can scale it up to training a neural network that analyzes player stats to predict transfer prices, or scale it down to just scraping data and building a database to explore basic correlations. 

Dependencies:

Libraries: 
Numpy (data structures, and numerical operations) 
Pandas (data manipulation, analysis, and cleaning) 
sci-py (builds onto numpy with statistical testing, including Poisson distribution) 
scikit-learn (machine learning library for regression, classification, clustering, and model evaluation.) 
Soccerdata (Scrapes and formats soccer data from multiple sources) 
Statsbombpy (Official Python client for StatsBomb’s open data API) 
Mplsoccer (Visualization library for plotting soccer-specific graphics (pitches, pass maps, heatmaps, radar charts). 
ScraperFC (Scraper framework to pull football data from public websites) 
socceraction (mplements advanced soccer analytics frameworks like VAEP (Valuing Actions by Estimating Probabilities) and xT (Expected Threat).) 
soccer_xg (Toolkit for building expected goals (xG) models from event data)  
Kloppy(Normalizes and parses event and tracking data from multiple providers into a standard format.)  
Databallpy (Library for syncing tracking and event data into unified match timelines.) 
Pytorch  (deeplearning/neural nets framework) 

Datasets: Statsbomb, fbRef, Transfermarkt, understat, fotmod, whoScored 


# Explanation of how to run project


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


