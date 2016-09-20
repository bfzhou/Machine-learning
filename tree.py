# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:07:34 2016

@author: zbf
"""

#import numpy as np
import pandas as pd
import random
from collections import Counter

#read file into table (parser)
df = pd.read_table('house-votes-84.data',delimiter=",")
print(df)

#pick 30 data as data set
datalength = len(df)
#ascending data
my_randoms = sorted(random.sample(xrange(datalength), 30))
trainingset = df.loc[my_randoms]

# get classification index


cnt_pos = 0
cnt_neg = 0
idx_pos = []
idx_neg = []
subset_pos = {}
subset_neg = {}
for num_attri in range(1,17):
	df4 = trainingset.iloc[:, num_attri]
	for i, j in enumerate(df4):
		print(i)
		if j == 'y':
			cnt_pos += 1
			idx_pos.append(i)
		elif j == 'n':
			cnt_neg += 1 
			idx_neg.append(i)
	print(cnt_pos, cnt_neg)
	print(trainingset.iloc[idx_pos])
	print(trainingset.iloc[idx_neg])



# df5 = Counter(df4)
# df6 = df5.most_common
entropy = {}
for idx,val in enumerate( Counter( trainingset.iloc[:, 1] ).items() ):
	# print(idx,val)
	entropy[idx] = val[1]
	print(entropy[idx])



#calculate entropy
def calc_entropy(dataset):
	dataset_length = len(dataset)
	dataset_width = len(dataset[0])

	# from i to 