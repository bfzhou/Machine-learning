import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
from numpy import array
from scipy.cluster.vq import vq, kmeans, whiten

data0 = []
n=1
with open('hw25.csv', newline='') as csvfile:
	dataset = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in dataset:
		data0.append(row)
		# print(', '.join(row))

data = np.array(data0)
# print(data)
inset = np.delete(data,0,0)
inset = np.delete(inset,0,1)
inset = np.delete(inset,0,1)
print(inset)

# features = array(inset)
# y = features.astype(np.int)
# whitened = whiten(y)
# book = array((y[0],y[2]))
# # print(book)
# print(kmeans(y,book))
# label = np.matrix(inset[:,0].astype(np.int)).T
# attr0 = inset[:,range(1,7)].astype(np.int)
# attr = np.hstack((attr0, np.ones((20,1),dtype=attr0.dtype)))
# tet = scipy.cluster.vq.kmeans(inset)
kmeans2 = KMeans(n_clusters=2, max_iter=1000).fit(inset)
print(kmeans2.labels_)
# print(kmeans.predict(['2','1','1','1','3','3']))
print(kmeans2.cluster_centers_)
print(kmeans2.get_params)