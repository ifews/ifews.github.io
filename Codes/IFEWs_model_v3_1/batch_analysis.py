# -*- coding: utf-8 -*-
"""
============================================
# Created: 12/13/2022
# Author: Siddhesh Naidu

This code runs the IFEWs model analysis for a chain of inputs that can be read from an excel file

============================================
"""

import numpy as np
import pandas as pd
import os

from IFEWs_model_v3_1 import IFEW

# Constants
May_P = 80 # May planting progress averaged at 80%  for 2009 - 2019
RCN_c = 185  # Sawyer(2018) Avg (155-215)
RCN_s = 17 # Avg = 17.7 kg/ha std = 4.8kg/ha based on the fertilizer use and price data between 2008-2018 (USDA, 2019)

# Read CSV Files

# Load Weather data -----------
loc3 = 'weather_data/PRISM_201401_202001_sorted.csv' # Weather dataframe
df_W = pd.read_csv(loc3)

# Load Animal Agriculture data -----------
loc4 = 'animal_agriculture_data/IFEW.csv'
df_AA = pd.read_csv(loc4) # Animal Agricultural dataframe

# Parse Weather Data
# July_data = df_W[(df_W['year']>=2014) & (df_W['month']==1)]
T_July = df_W['tmean (degrees C)'][(df_W['Year']>=2014) & (df_W['Month']==7)]
PPT_June = df_W['ppt (mm)'][(df_W['Year']>=2014) & (df_W['Month']==6)]
PPT_July = df_W['ppt (mm)'][(df_W['Year']>=2014) & (df_W['Month']==7)]

# Parse Animal Agricultural Data
cattle_B = df_AA["BeefCows"]
cattle_M = df_AA["MilkCows"]
cattle_H = df_AA["Hogs"]
cattle_O = df_AA["OtherCattle"]

for i in range(len(df_AA)):
    x = [RCN_c, RCN_s, cattle_H.iloc[i], cattle_B.iloc[i], cattle_M.iloc[i], cattle_O.iloc[i]] 
    w = [May_P, T_July.iloc[i], PPT_July.iloc[i], PPT_July.iloc[i] ** 2, PPT_June.iloc[i]]
    raw_results = IFEW(x, w, False)
    if i == 0:
        ns_data = [raw_results[0]]
        yc_data = [raw_results[1]]
        ys_data = [raw_results[2]]
    else:
        ns_data =  ns_data + [raw_results[0]]
        yc_data =  yc_data + [raw_results[1]]
        ys_data =  ys_data + [raw_results[2]]

np.savetxt('Raw Results.csv', list(zip(ns_data, yc_data, ys_data)), fmt='%s', delimiter=',')
# %%
