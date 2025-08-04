#Joseph Saunderson
#Kmeans algorithm
#Have been running Kmeans like this:
#for ((x=0;x<100;x++)); do echo "cat merged_players_final.txt | ./split.bash 45 python3 kmeans.py 40 ${x} > answer_40_clusters_${x}.txt"; done | ./parallelize.bash
# where 45 is the number of lines of validation data and 40 is the number of clusters.

#for ((x=0;x<100;x++)); do echo "cat merged_players_final.txt | ./split.bash 40 python3 kmeans.py 50 ${x} > answer_50_clusters_${x}.txt"; done | ./parallelize.bash
#./after_kmeans.sh 50

import sys
import numpy as np

def euclidean_distance(point1, point2):

    distance = 0
    for p1, p2 in zip(point1, point2):
        distance += (p1 - p2) ** 2
    return distance ** 0.5

def assign_clusters(data, centroids):

    clusters = [[] for _ in range(len(centroids))]
    
    for i in range(len(data)):
        example = data[i]
        
        #calculate distances to each centroid
        distances = [euclidean_distance(example[:-1], centroid) for centroid in centroids]
        
        #find closest centroid
        cluster_index = np.argmin(distances)
        
        #assign example to closest cluster
        clusters[cluster_index].append(i)
    
    return clusters

def calculate_new_centroids(data, clusters, k):

    #initialize centroids as zeros using k clusters and data's dimentions minus the labels
    new_centroids = np.zeros((k, data.shape[1] - 1))

    for i in range(k):
        cluster = clusters[i]
        
        #if cluster is empty, ignore it to prevent errors
        if len(cluster) > 0:
            #calc mean of each cluster
            new_centroids[i] = np.mean(data[cluster, :-1], axis=0)

    return new_centroids

def assign_labels(data, clusters):

    cluster_labels = []


    for cluster in clusters:
        if cluster:  #make sure cluster not empty to avoid errors
            labels = data[cluster, -1]  #get labels for points in cluster
            label_counts = {}

            #count each label in the cluster
            for label in labels:
                if label in label_counts:
                    label_counts[label] += 1
                else:
                    label_counts[label] = 1

            #find most common label
            majority_label = None
            max_count = -1
            for label, count in label_counts.items():
                if count > max_count or (count == max_count and label < majority_label):
                    majority_label = label
                    max_count = count

            cluster_labels.append(majority_label)
        else:
            cluster_labels.append(-1)  #empty cluster

    return cluster_labels

def classify(validation_data, centroids, cluster_labels):

    correct_count = 0
    for example in validation_data: 
        #calc distances from each centroid
        distances = [euclidean_distance(example[:-1], centroid) for centroid in centroids]
        #find closest centroid
        cluster_index = np.argmin(distances)
        predicted_label = cluster_labels[cluster_index]
        #check if predicted label is right
        if predicted_label == example[-1]:
            correct_count += 1
    return correct_count

def kmeans(k, training_data, validation_data):

    #assign centroids as first k data points
    centroids = training_data[:k, :-1]

    #assign points to clusters
    clusters = assign_clusters(training_data, centroids)
    
    #calculate new positions of clusters
    new_centroids = calculate_new_centroids(training_data, clusters, k)
    
    while (new_centroids != centroids).all():
        centroids = new_centroids
        
        #assign points to clusters
        clusters = assign_clusters(training_data, centroids)
        
        #calculate new positions of clusters
        new_centroids = calculate_new_centroids(training_data, clusters, k)

    #assign class labels to clusters
    cluster_labels = assign_labels(training_data, clusters)
    
    #Write cluster labels and centroids to a file
    
    
    #classify validation samples
    count = classify(validation_data, centroids, cluster_labels)

    return count, cluster_labels, centroids

#New Stuff
def data_to_file(data, filename, delimiter=' '):
    """
    Writes a Python list or NumPy array to a text file.

    Args:
        data (list or np.ndarray): The data to write.
        filename (str): The name of the text file.
        delimiter (str): The delimiter to use between elements (default is space).
    """
    if isinstance(data, list):
        data = np.array(data)  # Convert list to NumPy array
    
    np.savetxt(filename, data, delimiter=delimiter)
    
def main():
    #command line args
    k = int(sys.argv[1])
    #training = sys.argv[2]
    #validation = sys.argv[3]
    iteration = int(sys.argv[2])
    training = sys.argv[3]
    validation = sys.argv[4]
    
    training_data = np.loadtxt(training)
    validation_data = np.loadtxt(validation)

    #K-means clustering and classification
    count, cluster_labels, centroids = kmeans(k, training_data, validation_data)

    data_to_file(cluster_labels, "cluster_labels_" + str(iteration) + "_" + str(k) + ".txt")
    data_to_file(centroids, "centroids" + str(iteration) + "_" + str(k) + ".txt")
    #output correctly classified samples
    print(count)

main()

