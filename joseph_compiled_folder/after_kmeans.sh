#!/bin/bash
#This is for finding average of the correct validations
#rm -r answers_$1
#rm -r centroid_$1
#rm -r clusters_$1
mkdir answers_$1
mv answer_$1_* answers_$1/
mkdir centroid_$1
mv centroids* centroid_$1/
mkdir clusters_$1
mv cluster_labels_* clusters_$1
cp avg.py answers_$1/
cd answers_$1
python avg.py $1 > average_answer.txt
python avg.py $1
#rm answer_$1_*