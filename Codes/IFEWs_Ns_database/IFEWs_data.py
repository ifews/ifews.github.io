# -*- coding: utf-8 -*-
"""
============================================
Author: Julia Brittes Tuthill
Date Start: June 21, 2022
Last Change: Sept 6, 2023

IFEWs Data Fetch
This code fetches IFEWs necessary data from USDA and other sources.

Variables*:
beef = Beef Cattle Inventory (heads)  
milk = Milk Cattle Inventory (heads)  
cattle = All Cattle Inventory - includes calves, cows, steers and bulls (heads)
steers = Cattle on Feed (heads)
onfeed_sold = Cattle on Feed Sold (heads)
bulls = adult male cattle (heads)
calves = Young cattle (heads)
beef_heifers = Young Female Beef Cattle (heads)
dairy_150 = Young Female Dairy Cattle less than 1 year old (heads)
dairy_400 = Young Female Dairy Cattle between 1 and 2 years old (heads)
fin_cattle = Finishing Cattle (heads)
hogs = Hogs Inventory (heads)
hogs_sales = Hogs sold (heads)
hogs_breeding = Hogs used for breeding (heads)
hogs_fin = Hogs fattening (finish) (heads)
hogs_sow = adult female Hogs (heads)
hogs_boars = adult male Hogs (heads)
corng_pa = Corn Area Planted (acres)
corng_ha = Corn Grain Area Harvested (acres)
corng_y = Corn Grain Yield (bu/ac)
soy_pa = Soybeans planted (acres)
soy_ha = Soybeans Area Harvested (acres)
soy_y = Soybeans Yield (bu/ac)

*All yearly data.

Time Scale = 1968** till Current Year-1
Spatial Scale = Iowa Counties

**Why 1968: animal data constrained 
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
    hogs, hogs_others, beef, milk, other_cattle, on_feed,
    corng_y, corng_pa, corng_ha, soy_y, soy_pa, soy_ha,
    ap, cp
    )
from helper_functions import (
    process_data_crop, process_data_animal, expand_df, refine_animal_data,
     calculate_manure_n, calculate_fix_n, calculate_grain_n, calculate_ns, interpolation
    )
from caopeiyu_nrate import nrate_iowa_counties

# Define animal and crop parameters
animal_parameters = [hogs, hogs_others, beef, milk, other_cattle, on_feed]
crop_parameters = [corng_y, corng_pa, corng_ha, soy_y, soy_pa, soy_ha]

# Process animal and crop data
animal_df = process_data_animal(animal_parameters)
crop_df = process_data_crop(crop_parameters)

animal_df.rename(columns={'county_name': "CountyName", 'year':'Year'
            }, inplace=True)
crop_df.rename(columns={'county_name': "CountyName", 'year':'Year'
            }, inplace=True)

crop_df.drop(crop_df[crop_df['CountyName'] == 'OTHER COUNTIES'].index, inplace = True)
crop_df.drop(crop_df[crop_df['CountyName'] == 'OTHER (COMBINED) COUNTIES'].index, inplace = True)

# ---------------------Validation - Yearly values for Iowa from USDA ----------------------
crop_val = cp()
animal_val = ap()

# expanded - expand so both final df has the same amount of years
animal_df = expand_df(df = animal_df, validation_df = crop_val)
crop_df = expand_df(df = crop_df, validation_df = crop_val)

# numeric
cols = [ i for i in animal_df.columns if i not in ['CountyName', 'Year']]
for col in cols:
    animal_df[col] = pd.to_numeric(animal_df[col])

cols = [ i for i in crop_df.columns if i not in ['CountyName', 'Year']]
for col in cols:
    crop_df[col] = pd.to_numeric(crop_df[col])


animal_ifews = refine_animal_data(animal_df, animal_val)
crops_ifews = interpolation(crop_df)

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