"""
Transfer Price Prediction Tool

This script takes a player name as input and predicts their transfer price range using
KMeans cluster centroids and a labeled range file. It compares the player's
stats with centroids using Euclidean distance to find the closest cluster, then outputs
a predicted price range.

Requirements:
- Player data must be provided from a CSV file 
- Centroids and label files must be precomputed (from kmeans.py output)

Authors: Logan Seitz, Marcos Wofford, Joseph Saunderson
"""

import csv
import os

def find_player_row(database_file, player_name):
    """Returns the dictionary of the player row if a matching name is found."""
    with open(database_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['name'] == player_name:
                return row
    return None

def euclidean_distance(point1, point2):
    """Computes the Euclidean distance between two vectors."""
    distance = 0
    for p1, p2 in zip(point1, point2):
        distance += (p1 - p2) ** 2
    return distance ** 0.5

def Get_Predicted_Range(centroids_file, centroid_labels_file, ranges, player_dict):
    """
    Given a player's feature dictionary, compares it to the centroids,
    finds the closest one, and returns the price range mapped to that cluster.
    """
    # Features used in clustering (must match centroid structure)
    featureList = ['Age', 'time', 'xA', 'xG']

    try:

        # Convert selected player features to float
        playerFeatures = [float(player_dict[word]) for word in featureList]
    except:
        print("The player's data is insufficient for prediction")
        return None

    with open(centroids_file, 'r') as f:
        centroid_vector_list = []
        distance_list = []
        for line in f.readlines():
            centroid_vector = [float(x) for x in line.split()]
            distance = euclidean_distance(centroid_vector, playerFeatures)
            centroid_vector_list.append(centroid_vector)
            distance_list.append(distance)

        # Find index of closest centroid
        min_distance = min(distance_list)
        CentroidIndex = distance_list.index(min_distance)
        CentroidFileLine = CentroidIndex + 1

        # Get label of the matched centroid
        with open(centroid_labels_file, 'r') as clf:
            labelList = clf.readlines()
            label = labelList[CentroidIndex]
            with open(ranges, 'r') as r:
                rangeList = r.readlines()
                for item in rangeList:
                    items = item.split()
                    if float(items[0]) < float(label) <float(items[1]):
                        rawRange = items
                    #if label[0:5] == item[0:5]:
                        #rawRange = item.split()

        # Extracting and scaling lower range
        rawRangeLower = rawRange[0]
        rangeLower = float(rawRangeLower[0:4])
        if rawRangeLower[-1] == '5':
            rangeLower *= 0.1
        elif rawRangeLower[-1] == '7':
            rangeLower *= 10
        elif rawRangeLower[-1] == '8':
            rangeLower *= 100

        # Extracting and scaling upper range
        rawRangeUpper = rawRange[1]
        rangeUpper = float(rawRangeUpper[0:4])
        if rawRangeUpper[-1] == '5':
            rangeUpper *= 0.1
        elif rawRangeUpper[-1] == '7':
            rangeUpper *= 10
        elif rawRangeUpper[-1] == '8':
            rangeUpper *= 100

        # Returning all relevant prediction data
        closest_centroid = centroid_vector_list[CentroidIndex]
        return closest_centroid, CentroidFileLine, label, rangeLower, rangeUpper

def save_prediction_to_txt(player_name, player_row, label, centroid, line_number, lower, upper):
    """Saves player stats and predicted price range to a formatted .txt file."""
    filename = f"{player_name.replace(' ', '_')}_prediction.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Player Profile {player_name}\n")
        f.write("="*40 + "\n\n")
        
        f.write("Player Stats:\n")
        for k, v in player_row.items():
            if v.strip(): 
                f.write(f"{k}: {v}\n")

        f.write(f"\n===Transfer Price Prediction for {player_name}\n====")
        f.write(f"Closest Centroid: {centroid}\n")
        f.write(f"Centroid Line Number: {line_number}\n")
        f.write(f"Cluster Label: {label.strip()}\n")
        f.write(f"Predicted Price Range: €{lower}M - €{upper}M\n")
    
    print(f"\n Prediction saved to '{filename}'")

def main():
    """Main runner for predicting transfer price range."""
    
    print("=== Transfer Price Prediction Tool ===\n")

    # Prompting user for player database file
    default_db_file = 'merged_players.csv'
    db_file = default_db_file
    if not db_file:
        db_file = default_db_file
    if not os.path.exists(db_file):
        print(f" File not found: {db_file}")
        return

    # Prompting user for player name
    searched_player = input("Enter a player name to predict their transfer price: ").strip()
    player_row = find_player_row(db_file, searched_player)
    if player_row is None:
        print(f" Player '{searched_player}' not found in {db_file}")
        return

    # Prompting user for necessary model files
    default_centroids = "centroids31_65.txt"
    default_labels = "cluster_labels_31_65.txt"
    default_ranges = "ranges.txt"

    centroids_file = default_centroids
    labels_file = default_labels
    ranges_file = default_ranges

    # Making sure files exist
    for file in [centroids_file, labels_file, ranges_file]:
        if not os.path.exists(file):
            print(f" Required file not found: {file}")
            return
    try:

        # Predicting price range
        centroid, line_num, label, low, high = Get_Predicted_Range(
            centroids_file,
            labels_file,
            ranges_file,
            player_row
        )
    except:
        print("Ending program now, please try another player")
        return

    # Printing results
    # print(f"\nThis is the Label: {label.strip()}")
    # print(f"This is the Centroid {centroid} at line {line_num} in the file {centroids_file}")
    print(f"The price prediction is... €{low}M - €{high}M")

    # Saving results to file
    save_prediction_to_txt(searched_player, player_row, label, centroid, line_num, low, high)

main()
