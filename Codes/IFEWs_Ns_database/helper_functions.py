import numpy as np
import pandas as pd
from c_usda_quick_stats import c_usda_quick_stats

# Create an instance of c_usda_quick_stats
stats = c_usda_quick_stats()

# Define a function to fetch and process data
def process_data(parameters, names, wanted):
    dataframes = []
    for i, param in enumerate(parameters):
        df = stats.get_data(param)
        if 'CALVES' in param:
            df = df[df['class_desc'] == 'INCL CALVES']
        if 'HOGS' in param:
            df = df[df['short_desc'] == 'HOGS - INVENTORY']            
        df.columns = [col + '_' + names[i] if col not in ['year', 'county_name'] else col for col in df.columns]
        dataframes.append(df)
    merged_df = dataframes[0]
    
    for i in range(1, len(dataframes)):
        merged_df = pd.merge(merged_df, dataframes[i], on=['county_name', 'year'], how='outer')
    merged_df = merged_df.drop(merged_df[[item for item in list(merged_df.columns.values) if item not in wanted]], axis=1)          
    
    merged_df = merged_df.replace(',', '', regex=True)
    merged_df = merged_df.replace(' (D)', np.nan)
    cols = merged_df.columns.drop('county_name', 'year')
    merged_df[cols] = merged_df[cols].apply(pd.to_numeric, errors='coerce')

    if 'Value_other' in merged_df.columns:
        merged_df['Value_other'] = merged_df['Value_other'] - (merged_df['Value_beef'] + merged_df['Value_milk'])
    
    return merged_df

def interpolation(df, method):
    county_names = df['CountyName'].unique()
    animal_names = ['Beef Cattle','Hogs', 'Milk Cattle', 'Other Cattle']
    crop_names = ['CP', 'CH', 'CGY', 'SH', 'SP', 'SY']
    if all(col_name in df.columns for col_name in animal_names):
        # for each population
        pop_names = animal_names
    elif all(col_name in df.columns for col_name in crop_names):
        pop_names = crop_names
        
    # Loop through county names and populate data
    for county_name in county_names:

        # For each population
        for name in pop_names:
            k = pop_names.copy()
            k.remove(name)

            df_current = df[df['CountyName'] == county_name].drop(k, axis=1)
            years_to_pop = df_current[df_current[name].isna()]
            interpolated = df_current.interpolate(method)
            
            for year in years_to_pop['Year']:
                df.loc[(df['Year'] == year) & (df['CountyName']== county_name),name] = round(interpolated.loc[(interpolated['Year'] == year) & (interpolated['CountyName'] == county_name),name])
        
    return df  

# Define a function to calculate SSE
def calculate_sse(df_animal, df_valid):
    squared_errors = (df_animal - df_valid) ** 2
    sse = squared_errors.sum().sum()
    return sse

def best_interpol(df, df_valid):
    # List of interpolation methods
    kinds = ['linear', 'values', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic', 'from_derivatives', 'piecewise_polynomial', 'pchip', 'akima', 'cubicspline']

    # Initialize variables to keep track of the best method and SSE
    best_sse = float('inf')
    best_method = None

    # Iterate through interpolation methods
    for method in kinds:
        # Make a copy of animal_df to avoid modifying the original
        df_copy = df.copy()

        # Run animal_interpol for the current method
        interpolated_df = interpolation(df_copy, method)

        # Group by Year and sum the values for each column
        df_sum = interpolated_df.groupby('Year').sum()

        # Calculate SSE for the current method
        sse = calculate_sse(df_sum, df_valid)

        # Check if the current SSE is the smallest so far
        if sse < best_sse:
            best_sse = sse
            best_method = method
    return best_method   

def join_census_survey(df_survey, df_census):
    # Iterate through survey and update values based on conditions
    for index, row in df_survey.iterrows():
        county = row['CountyName']
        year = row['Year']
        
        # Find the corresponding row in census
        census_row = df_census[(df_census['CountyName'] == county) & (df_census['Year'] == year)]
        
        # Check if there is a matching census row
        if not census_row.empty:
            # Update non-NaN values from census_row to survey_row
            for column in ['Hogs', 'Beef Cattle', 'Milk Cattle', 'Other Cattle']:
                if np.isnan(row[column]):
                    df_survey.at[index, column] = census_row.iloc[0][column]    

    return df_survey               

def expand_df(df, validation_df):
    # Create a list of unique counties
    counties = df['CountyName'].unique()

    # Create a list of years from 1968 to 2023
    years = list(range(validation_df['Year'].min(), validation_df['Year'].max()+1))

    # Create an empty DataFrame to store the expanded data
    expanded_df = pd.DataFrame(columns=df.columns)

    # Iterate through each county and year, and add rows to the expanded DataFrame
    for county in counties:
        for year in years:
            # Check if the county and year combination already exists in the original DataFrame
            if not ((df['CountyName'] == county) & (df['Year'] == year)).any():
                # Create a new row with NaN values for all columns
                new_row = pd.DataFrame([[county, year] + [pd.NA] * (len(df.columns) - 2)], columns=df.columns)
                # Append the new row to the expanded DataFrame
                expanded_df = pd.concat([expanded_df, new_row], ignore_index=True)

    # Concatenate the original DataFrame and the expanded DataFrame
    new_df = pd.concat([df, expanded_df], ignore_index=True)

    # Sort the DataFrame by CountyName and Year
    new_df = new_df.sort_values(['CountyName', 'Year']).reset_index(drop=True)

    # Fill any remaining NaN values with appropriate default values
    new_df = new_df.fillna({'Hogs': np.nan, 'Beef Cattle': np.nan, 'Milk Cattle': np.nan, 'Other Cattle': np.nan})

    return new_df           

# function to calculate ManureN_kg_ha for each row
def calculate_manure_n(row):
    hogs = row['Hogs']
    milk_cows = row['Milk Cattle']
    beef_cows = row['Beef Cattle']
    other_cattle = row['Other Cattle']
    soybeans_acres = row['SP']
    corn_acres = row['CP']
    
    manure_n = (hogs * 0.027 * 365 + milk_cows * 0.204 * 365 + beef_cows * 0.15 * 365 + other_cattle * 0.5 * 0.1455 * 365 + other_cattle * 0.5 * 0.104 * 170) / (0.404686 * (soybeans_acres + corn_acres))
    
    return round(manure_n, 1)

# function for calculating fixation n
# soybeans bushels consider 1 metric ton/hectare = 14.87 (15) bushels/acre from https://www.extension.iastate.edu/agdm/wholefarm/pdf/c6-80.pdf
def calculate_fix_n(row):
    soybeans_yield = row['SY']
    soybeans_acres = row['SP']
    corn_acres = row['CP']
    
    fix_n = ((soybeans_yield/15)*81.1-98.5)*(soybeans_acres/(soybeans_acres+corn_acres))
    
    return round(fix_n, 1)

# function for calculation grain nitrogen
def calculate_grain_n(row):
    soybeans_yield = row['SY']
    corn_yield = row['CGY']
    soybeans_acres_h = row['SH']
    corn_acres_h = row['CH']
    
    grain_n = ((soybeans_yield*67.25)*(6.4/100)*(soybeans_acres_h*0.404686)+(corn_yield*62.77)*(1.18/100)*corn_acres_h*0.404686)/(0.404686*(soybeans_acres_h+corn_acres_h))
    
    return round(grain_n, 1)

# function for calculating nitrogen surplus 
def calculate_ns(row):
    commercial = row['CN']
    manure = row['MN']
    grain = row['GN']
    fix = row['FN']
    
    ns = commercial + manure + fix - grain
    
    return round(ns, 1)