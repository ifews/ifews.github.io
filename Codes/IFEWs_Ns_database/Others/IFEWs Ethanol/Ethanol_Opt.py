# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 08:57:53 2023

@author: jbrittes

Ethanol Optimization:
    The idea here is to extend the non-linear GRG analysis made for all Iowa to the sum of each county using scipy optimization methods.
"""

# Set up
import pandas as pd
#import numpy as np
#import datetime
#import matplotlib.pyplot as plt
#from sympy import *
from scipy.optimize import minimize


# Get Corn Yield (Bu/Ac) for 1997 to 2021 from IFEWs Counties
# Get Harvested Area in Acres
ifews = pd.read_csv(r'C:\Users\julia\OneDrive\Área de Trabalho\ISU\2023\Spring\A B E 516X\Project\IFEW_Counties_1997_2019.csv')

# corn = ifews[['CountyName',"CornGrainAcresHarvested",'CornGrainYield_bupacre' , 'Year']].copy()

# # Prepare data - Fill in NA values based on previous year
# corn["CornGrainAcresHarvested"] = corn["CornGrainAcresHarvested"].fillna(method='ffill')
# corn["CornGrainYield_bupacre"] = corn["CornGrainYield_bupacre"].fillna(method='ffill')
    



# #Calculate Total Bushels per year per County
# corn['Total Bushels'] = corn['CornGrainAcresHarvested']*corn['CornGrainYield_bupacre']
# corn['Year'] = pd.to_datetime(corn['Year'])
# corn['Year'] = corn['Year'].dt.year

# # Base equation IFEWs Ethanol Production 
# """
# Total corn in bushels
# Ethanol in Thousand Barrels
# 1 bushel of corn (56lbs) = ~2.8 gals = c
# Total corn that goes to ethanol = 50% = r
# 1 gal (US), 0.0238095238 bbl (oil)
# 42 gal is 1 barrel
# """

# corn['Ethanol (Gallons)'] = corn['Total Bushels']*2.8*0.5 #Ethanol in Gallons
# corn['Ethanol (Barrels)'] = corn['Ethanol (Gallons)']*0.024 #Ethanol in Barrels
# corn['Ethanol (Thousands of Barrels)'] = corn['Ethanol (Barrels)']/1000

# # Sum all counties (to have Iowa Production) for each year - This can be compared with EIA data
# corn_et = corn.groupby(['Year'])['Ethanol (Thousands of Barrels)'].sum()

# """
# Use 2009 and up data (due to expressive change in Ethanol Production 
# Energy Independence and Security Act of 2007 statement was to ‘increase the production of clean renewable fuels’  
# """

# corn_et = corn_et.drop([1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
#              2008])

# # Get EIA Ethanol Production in Thousand Barrels
url = 'https://www.eia.gov/state/seds/sep_prod/xls/prod_phy.xlsx'
# eia = pd.read_excel(url,'Fuel Ethanol', index_col = 0,  header = 2)
# eia = eia.dropna(axis =1)
# eia = eia.transpose()
# eia = eia[['IA']]
# eia = eia.drop([1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971,
#        1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983,
#        1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995,
#        1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
#        2008,2020])

# # Combine both dataframes
# comb = pd.concat([corn_et, eia], 1)
# #comb.plot()
# comb['e'] = comb['Ethanol (Thousands of Barrels)'] - comb['IA']
# comb['sq_e'] = comb['e']*comb['e']


# #Function to minimize
# s = comb['sq_e'].sum()



def IFEWs_Ethanol(c, r):
    
    corn = ifews[['CountyName',"CornGrainAcresHarvested",'CornGrainYield_bupacre' , 'Year']].copy()

    # Prepare data - Fill in NA values based on previous year
    corn["CornGrainAcresHarvested"] = corn["CornGrainAcresHarvested"].fillna(method='ffill')
    corn["CornGrainYield_bupacre"] = corn["CornGrainYield_bupacre"].fillna(method='ffill')
    

    #Calculate Total Bushels per year per County
    corn['Total Bushels'] = corn['CornGrainAcresHarvested']*corn['CornGrainYield_bupacre']
    corn['Year'] = pd.to_datetime(corn['Year'])
    corn['Year'] = corn['Year'].dt.year
    
    # Base equation IFEWs Ethanol Production 
    """
    Total corn in bushels
    Ethanol in Thousand Barrels
    1 bushel of corn (56lbs) = ~2.8 gals = c
    Total corn that goes to ethanol = 50% = r
    1 gal (US), 0.0238095238 bbl (oil)
    42 gal is 1 barrel
    """
    
    corn['Ethanol (Gallons)'] = corn['Total Bushels']*c*r #Ethanol in Gallons
    corn['Ethanol (Barrels)'] = corn['Ethanol (Gallons)']*0.024 #Ethanol in Barrels
    corn['Ethanol (Thousands of Barrels)'] = corn['Ethanol (Barrels)']/1000
    
    # Sum all counties (to have Iowa Production) for each year - This can be compared with EIA data
    corn_et = corn.groupby(['Year'])['Ethanol (Thousands of Barrels)'].sum()
    
    """
    Use 2009 and up data (due to expressive change in Ethanol Production 
    Energy Independence and Security Act of 2007 statement was to ‘increase the production of clean renewable fuels’  
    """
    corn_et = corn_et.drop([1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008])
    #corn_et = corn_et[[2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]]  # Only 2009-2019 data
    
    
    # Get EIA Ethanol Production in Thousand Barrels
    eia = pd.read_excel(url,'Fuel Ethanol', index_col = 0,  header = 2)
    eia = eia.dropna(axis =1)
    eia = eia.transpose()
    eia = eia[['IA']] #only gets Iowa data
    eia = eia.drop([1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971,
        1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983,
       1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995,
        1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
       2008,2020])
    #eia = eia[[2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]] # Only 2009-2019 data
    
    # Combine both dataframes
    comb = pd.concat([corn_et, eia], 1)
    #comb.plot()
    comb['e'] = comb['Ethanol (Thousands of Barrels)'] - comb['IA']
    comb['sq_e'] = comb['e']*comb['e']
    
    
    #Function to minimize
    s = comb['sq_e'].sum()
    
    return s

# define the constraint functions
def r_constraint(s):
    return s[1] - 0.48

def c_constraint(s):
    return 2.7 - s[2]

# define the bounds for r and c
bounds = ((None, None), (0.48, 0.6), (2.7, 2.9))

#define the constraints as a list of dictionaries
constraints = [{'type': 'ineq', 'fun': r_constraint},
               {'type': 'ineq', 'fun': c_constraint}]

#define the initial guess for s
x0 = [0, 2.7, 0.48]

# minimize the objective function subject to the constraints and bounds
result = minimize(IFEWs_Ethanol, x0, method='SLSQP', bounds=bounds, constraints=constraints)

# print the solution
print(result.s)

#results = IFEWs_Ethanol(2.8,0.5)   





