# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:07:34 2016

@author: zbf
"""

import numpy as np
import scipy
import io
import pandas as pd

#h=open('house-votes-84.data','r')
df = pd.read_table('house-votes-84.data',delimiter=",")

#datas = np.loadtxt(m,delimiter=",")
#print (datas)
print(df)