# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:07:34 2016

@author: zbf
"""

import numpy as np
import scipy

f = np.loadtxt('house-votes-84.data',dtype={'names': ('class', 'handicapped', 'water', 'adoption', 'physician', 'el-salvador-aid', 'religious', 'anti', 'aid', 'mx', 'immigration', 'synfuels', 'education', 'superfund', 'crime', 'duty', 'export'))
print(f)
l = [line.split() for line in f ]
print (l[0])
m=np.split(l[0],3)
print (m)