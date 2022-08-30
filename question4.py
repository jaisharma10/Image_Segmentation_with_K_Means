# coding: utf-8


import cv2
import numpy as np
from random import sample
import matplotlib.pyplot as plt


img = cv2.imread('Q4image.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print('Image Shape: ', img.shape)
height = img.shape[0]
width = img.shape[1]
plt.imshow(img)
plt.show


def initial_centroids(data,k):
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    black = (0,0,0)
    centroid = (red, green, blue, black)
    return centroid
    
def eucDistance(pt1, pt2):
    distance = ((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2 + (pt1[2] - pt2[2])**2)**0.5 
    return(distance)

def get_labels(data, centroids):
    labels = []
    for point in data: # goes through all points
        min_dist = float('inf')
        label = None
        for i, centroid in enumerate(centroids): # goes through all centroids
            new_dist = eucDistance(point, centroid)
            if min_dist > new_dist:
                min_dist = new_dist
                label = i
        labels.append(label)
    return labels

def updateCent(points, labels, k):
    newCent = [[0,0,0] for i in range(k)]
    counts = [0]*k
    
    for pts, label in zip(points, labels):
        newCent[label][0] += pts[0]
        newCent[label][1] += pts[1]
        newCent[label][2] += pts[2]
        counts[label] += 1
        
    for i, (x,y,z) in enumerate(newCent):
        newCent[i] = (x/counts[i], y/counts[i], z/counts[i])
    return newCent

def stopLoop(oldCent, newCent, threshold):
    change = 0
    for old_C, new_C in zip(oldCent, newCent):
        change += eucDistance(old_C,new_C)
    return change < threshold

# data is rgb for each pixels
data = []
k = 4
threshold = 1

# collect data
for w in range(width-2):
    for h in range(height-2):
        (r, g, b) = img[h,w]  
        data.append((r, g, b))
            
def KMeans(data,k):  
        print('start')
        centroids = initial_centroids(data,k)
        while True:
            oldCent = centroids
            labels = get_labels(data,centroids)
            centroids = updateCent(data, labels, k)
            if stopLoop(oldCent, centroids, threshold):
                break
        print('K-Means Cluster Algorithm Executed')
        return(labels,centroids)

labels, newCluster = KMeans(data,k)

# assign new colour schemes
n = 0
for w in range(width-2):
    for h in range(height-2):
        if labels[n] == 0:
            img[h, w] = newCluster[0]
        elif labels[n] == 1:
            img[h, w] = newCluster[1]
        elif labels[n] == 2:
            img[h, w] = newCluster[2]
        elif labels[n] == 3:
            img[h, w] = newCluster[3]
        n += 1

print("=======================================================")

plt.figure(figsize=(6, 6))
plt.imshow(img)
plt.show()