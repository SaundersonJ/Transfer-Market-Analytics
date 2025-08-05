#Joseph Saunderson
#This file creates price ranges and averages each one and assigns that as the class label for each record

import numpy as np


data = np.loadtxt("merged_players.txt")

prices = data[:,-1]
print(f'mean: {np.mean(prices)}')
print(f'median: {np.median(prices)}')
print(f'min: {np.min(prices)}')
print(f'max: {np.max(prices)}')
print()
# Generate evenly spaced points
points = np.linspace(np.min(prices), np.max(prices), 60 + 1)

# Create the ranges
ranges = []
#changed to range 60
for i in range(60):
    ranges.append((points[i], points[i+1]))

print(ranges)

for i in range(len(prices)):
    for lower, upper in ranges:
        if lower <= prices[i] < upper: # Check if the value falls within the current range
            data[i,-1] = int((lower + upper) / 2)
            
np.savetxt('merged_players_final.txt', data, fmt='%d')
ranges_numpy = np.array(ranges)
np.savetxt('ranges.txt', ranges_numpy)
