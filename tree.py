# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:07:34 2016

@author: zbf
"""

import numpy as np
import scipy
import io
import pandas as pd
import random
# import tree

#read file into table (parser)
df = pd.read_table('house-votes-84.data',delimiter=",")
print(df)
df1= df.values[1][1]
print(df1)

#pick 30 data as data set
datalength = len(df)
#ascending data
my_randoms = sorted(random.sample(xrange(datalength), 30))
df2 = df.loc[my_randoms]
df3 = df2.values
df4 = df2.iloc[:, 1]
df5 = np.bincount(df4.values)
print(df5)


#calculate entropy
# def entropy(dataset)
# 	dataset_length = len(dataset)
