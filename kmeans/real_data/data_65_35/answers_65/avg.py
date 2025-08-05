import numpy as np
import sys

k = int(sys.argv[1])
all_data = []
for i in range(100):
    data = np.loadtxt("answer_" + str(k) +"_clusters_"+str(i)+".txt")
    #print(data)
    all_data.append(int(data))

all_data_np = np.array(all_data)
avg = np.mean(all_data_np)
max_index = np.argmax(all_data_np)
max_val = np.max(all_data_np)
print(max_index)
print(max_val)
print(avg)

    
