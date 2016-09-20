# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:07:34 2016

@author: zbf
"""

import numpy as np
import scipy
import io
import pandas as pd

#read file into table (parser)
df = pd.read_table('house-votes-84.data',delimiter=",")
print(df)