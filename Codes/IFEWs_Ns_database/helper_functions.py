import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
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

def interpolation(ifews_df, method):
    df = ifews_df.copy()
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
        for name in pop_names:
            k = pop_names.copy()
            k.remove(name)

            # Filter the DataFrame for the specific county and population
            county_df = df[(df['CountyName'] == county_name) & (df[name].notna())]

            # Extract x and y values
            x = county_df['Year'].astype(float).to_numpy()
            y = county_df[name].astype(float).to_numpy()

            # Extract xnew values
            xnew = df[(df['CountyName'] == county_name) & (df[name].isna())]['Year'].astype(float).to_numpy()

            f = interp1d(x, y, kind = method, fill_value="extrapolate")
            ynew = f(xnew)

            # Update the DataFrame with interpolated values
            df.loc[(df['CountyName'] == county_name) & (df[name].isna()), name] = np.round(ynew)
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Replace negative values with zero in the entire column
                    df[col] = df[col].apply(lambda x: 0 if x < 0 else x)

    # Forward fill consecutive zeros with the last previous value
    df = df.apply(lambda x: x.mask(x == 0).ffill())   
    return df  

def best_interpol(ifews_df, validation):
    # Assuming you have a DataFrame df_copy with a 'Year' column in datetime format
    kinds = ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic']

    # Create dictionaries to store the results
    in_dfs = {}
    df_sum_dfs = {}
    sse = {}

    # Iterate over each kind and perform interpolation and summation
    for kind in kinds:
        # Run interpolation for the current kind using 'method' parameter
        in_dfs[kind] = interpolation(ifews_df, method=kind)

        # Group by Year and sum the values for each column
        df_sum_dfs[kind] = in_dfs[kind].groupby('Year').sum()
        diff_val = df_sum_dfs[kind]-validation.set_index('Year')
        diff_val.reset_index(inplace=True)
        sse[kind] = (diff_val**2).sum().sum()

    minim_sse = min(sse.values())
    best = [key for key, value in sse.items() if value == minim_sse][0]

    return best  

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
    years = list(range(validation_df['Year'].min(), validation_df['Year'].max()))

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
    new_df = new_df.fillna({'Hogs': np.nan, 'Beef Cattle': np.nan, 'Milk Cattle': np.nan,
                             'Other Cattle': np.nan, "CGY":np.nan,	"SY":np.nan,	"CP":np.nan,
                                 	"CH":np.nan,	"SP":np.nan,	"SH":np.nan})
    
    if 'CGY' in new_df.columns:
        new_df = new_df.drop_duplicates(subset = ['CountyName', 'Year'])

    new_df = new_df[new_df['Year']<2023]        

    return new_df           

# function to calculate ManureN_kg_ha for each row
def calculate_manure_n(row):
    hogs = row['Hogs']
    milk_cows = row['Milk Cattle']
    beef_cows = row['Beef Cattle']
    other_cattle = row['Other Cattle']
    soybeans_acres = row['SP']
    corn_acres = row['CP']
    
    # from Gronberg et al. (2017) 
    manure_n = (hogs * 0.027 * 365 +
                milk_cows * 0.204 * 365 +
                beef_cows * 0.15 * 365 +
                other_cattle * 0.5 * 0.1455 * 365 +
                other_cattle * 0.5 * 0.104 * 170) / (0.404686 * (soybeans_acres + corn_acres))
    
    # # from Andersen, D. S., & Pepple, L. M. (2017) 
    # manure_n = (hogs * 0.036 * 365 +
    #             milk_cows * 0.200 * 365 +
    #             beef_cows * 0.029 * 365 +
    #             other_cattle * 0.5 * 0.1455 * 365 +
    #             other_cattle * 0.5 * 0.104 * 170) / (0.404686 * (soybeans_acres + corn_acres))
    
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