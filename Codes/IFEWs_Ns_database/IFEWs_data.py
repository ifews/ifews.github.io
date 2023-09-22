# -*- coding: utf-8 -*-
"""
============================================
Author: Julia Brittes Tuthill
Date Start: June 21, 2022
Last Change: Sept 6, 2023

IFEWs Data Fetch
This code fetches IFEWs necessary data from USDA and other sources.

Variables:
Beef Cattle = Beef Cattle Inventory (heads)  
Milk Cattle = Milk Cattle Inventory (heads)  
Other Cattle = Other Cattle Inventory (heads) - All cattle minus milk and beef
Hogs = Hogs Inventory (heads)
CP = Corn Area Planted (acres)
CH= Corn Grain Area Harvested (acres)
CGY = Corn Grain Yield (bu/ac)
SP = Soybeans planted (acres)
SH = Soybeans Area Harvested (acres)
SY = Soybeans Yield (bu/ac)

Time Scale = 1968 till CurrentYear-1
Spatial Scale = Iowa Counties

*Why 1968: animal data constrained 
============================================
"""
import os
# Get data
os.chdir(r'C:\Users\jbrittes\Documents\Research\IFEWs_model_v3_1\data')
# Import necessary libraries
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import urllib.parse
from parameters import (
    parameters1, parameters2, parameters4, parameters5, parameters7, parameters8,
    parameters9c, parameters10c, parameters11c, parameters12c, parameters9s,
    parameters10s, parameters11s, parameters12s, ap, cp
    )
from helper_functions import (
    process_data, join_census_survey, expand_df,
     calculate_manure_n, calculate_fix_n, calculate_grain_n, calculate_ns, interpolation, best_interpol
    )
from caopeiyu_nrate import nrate_iowa_counties


# Define animal and crop parameters
animal_parameters_census = [parameters9c, parameters10c, parameters11c, parameters12c]
animal_parameters_survey = [parameters9s, parameters10s, parameters11s, parameters12s]
animal_names = ['hogs', 'beef', 'milk', 'other']
animal_wanted = ['county_name', "year",  'Value_beef','Value_hogs','Value_milk',  'Value_other']  
crop_parameters = [parameters1, parameters2, parameters4, parameters5, parameters7, parameters8]
crop_names = ['corn_yield', 'soybeans_yield', 'corn_planted', 'corn_harvested', 'soybeans_planted', 'soybeans_harvested']
crop_wanted = ['county_name', "year", "Value_corn_planted", "Value_corn_harvested", 
          "Value_corn_yield", "Value_soybeans_harvested","Value_soybeans_planted",
          "Value_soybeans_yield"]   

# Process animal and crop data
animal_df_census = process_data(animal_parameters_census, animal_names, animal_wanted)
animal_df_survey = process_data(animal_parameters_survey, animal_names, animal_wanted)
crop_df = process_data(crop_parameters, crop_names, crop_wanted)

# Rename colums
animal_df_survey = animal_df_survey.rename(columns={
    'county_name': 'CountyName',
    'Value_beef': 'Beef Cattle',
    'Value_hogs': 'Hogs',
    'Value_milk': 'Milk Cattle',
    'Value_other': 'Other Cattle',
    'year': "Year"})

animal_df_census = animal_df_census.rename(columns={
    'county_name': 'CountyName',
    'Value_beef': 'Beef Cattle',
    'Value_hogs': 'Hogs',
    'Value_milk': 'Milk Cattle',
    'Value_other': 'Other Cattle',
    'year': "Year"})

crop_df.rename(columns = {'county_name': "CountyName", "year": "Year", "Value_corn_planted": 'CP',
                 "Value_corn_harvested":"CH", "Value_corn_yield": "CGY",
                 "Value_soybeans_harvested":"SH", "Value_soybeans_planted":"SP",
                 "Value_soybeans_yield": "SY"}, inplace = True)
crop_df.drop(crop_df[crop_df['CountyName'] == 'OTHER COUNTIES'].index, inplace = True)
crop_df.drop(crop_df[crop_df['CountyName'] == 'OTHER (COMBINED) COUNTIES'].index, inplace = True)

# ---------------------Validation - Yearly values for Iowa from USDA ----------------------
crop_val = cp()
animal_val = ap()

# expanded - expand so both final df has the same amount of years
animal_df_survey = expand_df(df = animal_df_survey, validation_df = crop_val)
crop_df = expand_df(df = crop_df, validation_df = crop_val)

# fill in gaps of census vs survey
animal_df = join_census_survey(df_survey = animal_df_survey, df_census = animal_df_census)

# find best interpolation based on SSE comparison with Iowa Yearly values 
# ---------- Animal---------------------------------------------------------------------
animal_ifews = interpolation(ifews_df=animal_df, method=best_interpol(ifews_df = animal_df, validation = animal_val)) 
# -------- Crops ----------------------------------------------------------------------
crops_ifews = interpolation(ifews_df=crop_df, method=best_interpol(ifews_df = crop_df, validation = crop_val))

#--------------- merge USDA data ---------------------------------------------------
df_USDA = pd.merge(animal_ifews, crops_ifews, on=['CountyName', 'Year'], how='left')

# ---------------------- N fetilizer to Counties (Peiyu Cao) ------------------------------
parent_dir = os.getcwd()
nrate_gdf = nrate_iowa_counties(parent_dir)

# ---------------------- Merge USDA and Nrate data ----------------------------------------
"""
This section calculates the surplus based on Vishal's work:
The below modeling addresses the agricutlure and water (nitrogen surplus as a water
quality indicador) of the IFEWs.
The calculation of nitrogen surplus (Ns) is based on the construction of a rough agronomic
annual nitrogen budget (Blesh and Drinkwater, 2013; Jones et al., 2019a) given as:

Ns = CN + MN + FN - GN

where CN is the input from the application of commercial nitrogen, MN is the nitrogen generated
from manure, FN is the nitrogen fixed by soybean crop, and GN is the nitrogen present in
harvested grain.

CN = Nrate [kg/ha]

FN = (81.1*x2-98.5)Asoy/AP [kg/ha]

GN = (x1*(1.18/100)*Acorn + x2(6.4/100)*Asoy)/AH [kg/ha]

MNlivestockgroup = P*Nm*LF
MN = MNhogs + MNbeef + MNmilk + MNother)/AP [kg/ha]

Variables:
Nrate = Commercial fertilizer in lb N/ac
x1 = CGY in [tons per hectare]
x2 = SY in [tons per hectare]
Asoy = SP [acres]
Acorn = CP [acres]
AP = SP + CP [acres]
AH = SH + CH [acres]
P = livestock group population [heads]
Nm = Nitrogen in animal manure [kg/animal/day]
LF = life cycle of animal [days per year]


Output: 
Ns = N surplus [kg/ha]
CN = commercial nitrogen applied in planted corn crop (No fertilizer to soybean in Iowa)[kg/ha]
MN = nitrogen generated from manure[kg/ha]
FN = nitrogen fixed by soybean crop[kg/ha]
GN = nitrogen present in harvested grain [kg/ha]
"""
# merge only years existing in both dfs
IFEWs = pd.merge(df_USDA, nrate_gdf, on = ['CountyName', 'Year'], how = 'inner')

# CN 
IFEWs['CN'] = round(IFEWs["CN_lb/ac"]*1.121, 1)

# MN - Apply the function to create the ManureN_kg_ha field
IFEWs['MN'] = IFEWs.apply(calculate_manure_n, axis=1)

# FN - Apply the function to create the ManureN_kg_ha field
IFEWs['FN'] = IFEWs.apply(calculate_fix_n, axis=1)

# GN - Apply the function to create the ManureN_kg_ha field
IFEWs['GN'] = IFEWs.apply(calculate_grain_n, axis=1)

# Ns - Apply the function to create the ManureN_kg_ha field
IFEWs['NS'] = IFEWs.apply(calculate_ns, axis=1)