#Joseph Saunderson
#File to convert labels into ranges

ranges_infile = open("ranges.txt", "r")

list_of_tuples_ranges = []

for line in ranges_infile:
    parts = line.split(" ")
    list_of_tuples_ranges.append((float(parts[0]),float(parts[1])))


ranges_infile.close()
label_infile = open("cluster_labels_31_65.txt", "r")
cluster_outfile = open("cluster_labels_ranges_31_65.txt", "w")

for label in label_infile:
    for x,y in list_of_tuples_ranges:
        if x <= float(label) < y:
            cluster_outfile.write(str(x) + " " + str(y) +"\n")

label_infile.close()
cluster_outfile.close()