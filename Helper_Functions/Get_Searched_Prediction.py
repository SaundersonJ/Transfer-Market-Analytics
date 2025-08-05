import csv

def find_player_row(database_file, player_name):
    """This function returns a player and their data as a dictionary
    Arguments:
    database_file -- (str) a file name of a file containing all relavent player infortmation from understat and transfermrtkt
    player_name -- (str) a name that is to be searched by the user"""
    with open(database_file,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['name'] == player_name:
                return row
    return None

def euclidean_distance(point1, point2):

    distance = 0
    for p1, p2 in zip(point1, point2):
        distance += (p1 - p2) ** 2
    return distance ** 0.5

def Get_Predicted_Range(centroids_file, centroid_labels_file, ranges, player_dict):
    """This function takes the centroid file name and the 
    dictionary from find_player_row and finds the shortest euclidean distance
    to return the prediction string formatted
    Arguments:
    centroids_file -- (str) the name of the centroid file output from kmeans.py
    player_dict -- (dict) player dictionary output from find_player_row() """

#the feature list is currently a hard coded list of keys as strings 
#to determine what is needed for comparison with centroids
#refer to kmeans implementation
                    
    featureList = ['Age', 'time', 'xA', 'xG']
# featureList copied from RemoveColumsNaN() in clean_data/old_csvs/data_sort.py new_order variable
    playerFeatures = []
    for word in featureList:
        playerFeatures.append(float(player_dict[word]))
    # print(playerFeatures)
    with open(centroids_file,'r') as f:
        centroid_vector_list = []
        distance_list =[]
        for line in f.readlines():
            centroid_vector = [float(x) for x in line.split()]
            distance = euclidean_distance(centroid_vector, playerFeatures)
            centroid_vector_list.append(centroid_vector)
            distance_list.append(distance)

        #centroidIndex should tell which line the selected centroid came from
        #this will be used to find the string that represents the output string
        #from a seperate file represented by centroid_price_ranges
        min_distance = min(distance_list)
        CentroidIndex = distance_list.index(min_distance)
        CentroidFileLine = CentroidIndex + 1

        # perhaps we could do 
        with open(centroid_labels_file,'r') as clf:
            labelList = clf.readlines()
            label = labelList[CentroidIndex] #single value that represents range
            with open(ranges, 'r') as r:
                rangeList = r.readlines()
                for item in rangeList:
                    if label[0:5] == item[0:5]:
                        rawRange = item.split()
            
            rawRangeLower = rawRange[0]
            rawRangeUpper = rawRange[1]
            rangeLower = float(rawRangeLower[0:4]) * 1 #** int(rawRangeLower[-1])
            if rawRangeLower[-1] == 5:
                rangeLower*=0.1
            elif rawRangeLower[-1] == 7:
                rangeLower*=10
            elif rawRangeLower[-1] == 8:
                rangeLower*=100
            rangeUpper = float(rawRangeUpper[0:4]) * 1 #** int(rawRangeUpper[-1])
            if rawRangeUpper[-1] == 5:
                rangeUpper*=0.1
            elif rawRangeUpper[-1] == 7:
                rangeUpper*=10
            elif rawRangeUpper[-1] == 8:
                rangeUpper*=100
            
        #      
        #    cleanRange = f'Price prediction is €{rangeLower)}M - {rangeUpper}M'
        #    return cleanRange

        
        closest_centroid = centroid_vector_list[CentroidIndex]
        # print(f'closest centroid is: {closest_centroid}\n its index is {CentroidIndex}\n its line number is {CentroidFileLine}\n its label:{label}\n')
        # return pricePred
        return closest_centroid, CentroidFileLine, label, rangeLower, rangeUpper

def main():
    filename = 'merged_players.csv' #accquire dynamically in future!
    searchedPlayer = input("Enter a player name to predict their transfer price: ")
    playerName = searchedPlayer
    player_row = find_player_row(filename,playerName)
    print(f'The selected players full profile:\n{player_row}\n')
    chosen_centroid, centroid_lineNumber, label, rangeLower, rangeUpper = Get_Predicted_Range("centroids95_50.txt", 'cluster_labels_95_50.txt', 'ranges.txt', player_row)
    print(f'This is the Label: {label}\nThis is the Centroid{chosen_centroid} at line {centroid_lineNumber} in the file {filename}\n')
    print(f'The price prediction is... €{rangeLower}M - {rangeUpper}M')

main()
