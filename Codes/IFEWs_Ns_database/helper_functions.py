import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from c_usda_quick_stats import c_usda_quick_stats

# instance of c_usda_quick_stats
stats = c_usda_quick_stats()

# function to fetch and process data
def process_data_crop(parameters):
    dataframes = []
    for param in parameters:
        df = stats.get_data(param)         

        if 'CORN' in param and 'YIELD' in param:
            name =  "corng_y"
        elif 'CORN' in param and 'PLANTED' in param:
            name =  "corng_pa"  
        elif 'CORN' in param and 'HARVESTED' in param:
            name =  "corng_ha"  
        elif 'SOYBEANS' in param and 'YIELD' in param:
            name =  "soy_y"
        elif 'SOYBEANS' in param and 'HARVESTED' in param:
            name =  "soy_ha"
        else:
            name =  "soy_pa"
        # pivot table with county_name and year as indices and Value as the data column
        df = df.pivot_table(index=['county_name', 'year'], 
                                values='Value', 
                                aggfunc='first').reset_index()

        # Rename the columns
        df.columns = ['county_name', 'year', name]

        dataframes.append(df)

    df = dataframes[0] 
    for dfs in dataframes[1:]:  # Loop through remaining dataframes
        df = pd.merge(df, dfs, on=['county_name', 'year'], how='outer')
    
    df = df.replace(',', '', regex=True)
    df = df.replace(' (D)', np.nan)
    
    return df

def process_data_animal(parameters):
    dataframes = []
    for param in parameters:
        df = stats.get_data(param)
        
        if 'CALVES' in param:
            df = df[df['class_desc'] == 'INCL CALVES']
            # pivot table with county_name and year as indices and Value as the data column
            df = df.pivot_table(index=['county_name', 'year'], 
                                    values='Value', 
                                    aggfunc='first').reset_index()

            df.columns = ['county_name', 'year', 'cattle']

        if 'HOGS' in param and 'BREEDING' not in param:
            df = df[df['short_desc'] == 'HOGS - INVENTORY']  

            # pivot table with county_name and year as indices and Value as the data column
            df = df.pivot_table(index=['county_name', 'year'], 
                                    values='Value', 
                                    aggfunc='first').reset_index()

            df.columns = ['county_name', 'year', 'hogs']

        if 'BREEDING' in param:  
            df = df[
                ((df['short_desc'] == 'HOGS, BREEDING - INVENTORY') | 
                (df['short_desc'] == 'HOGS - SALES, MEASURED IN HEAD')) & 
                (df['domain_desc'] == 'TOTAL')
            ][['county_name', 'year', 'short_desc', 'Value']]

            # Use pivot_table to reshape the data
            df = df.pivot_table(
                index=['county_name', 'year'], 
                columns='short_desc', 
                values='Value', 
                aggfunc='first'
            ).reset_index()

            df.columns.name = None  # remove the columns' name
            df.rename(columns={
                'HOGS, BREEDING - INVENTORY': 'hogs_breeding', 
                'HOGS - SALES, MEASURED IN HEAD': 'hogs_sales'
            }, inplace=True)
            
        if 'SALES' in param:
            df = df[
                ((df['short_desc'] == 'CATTLE, ON FEED - INVENTORY') | 
                (df['short_desc'] == 'CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD')) & 
                (df['domain_desc'] == 'TOTAL')
            ][['county_name', 'year', 'short_desc', 'Value']]

            df = df.pivot_table(
                index=['county_name', 'year'], 
                columns='short_desc', 
                values='Value', 
                aggfunc='first'
            ).reset_index()

            df.columns.name = None
            df.rename(columns={
                'CATTLE, ON FEED - INVENTORY': 'steers', 
                'CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD': 'onfeed_sold'
            }, inplace=True)
            
        # if 'CHICKENS' in param:
        #     df = df[
        #         ((df['short_desc'] == 'CHICKENS, BROILERS - INVENTORY') | 
        #         (df['short_desc'] == 'CHICKENS, LAYERS - INVENTORY')) & 
        #         (df['domain_desc'] == 'TOTAL')
        #     ][['county_name', 'year', 'short_desc', 'Value']]

        #     df = df.pivot_table(
        #         index=['county_name', 'year'], 
        #         columns='short_desc', 
        #         values='Value', 
        #         aggfunc='first'
        #     ).reset_index()

        #     df.columns.name = None 
        #     df.rename(columns={
        #         'CHICKENS, BROILERS - INVENTORY': 'broilers', 
        #         'CHICKENS, LAYERS - INVENTORY': 'layers'
        #     }, inplace=True)
        
        if not any(x in param for x in ['CHICKENS', 'SALES', 'BREEDING', 'HOGS', 'CALVES']):
            if 'BEEF' in param:
                name =  "beef"
            elif 'MILK' in param:
                name = "milk"
            # elif 'TURKEYS' in param:
            #     name = 'turkeys'

            # pivot table with county_name and year as indices and Value as the data column
            df = df.pivot_table(index=['county_name', 'year'], 
                                    values='Value', 
                                    aggfunc='first').reset_index()

            df.columns = ['county_name', 'year', name]

        dataframes.append(df)

    df = dataframes[0] 
    for dfs in dataframes[1:]: 
        df = pd.merge(df, dfs, on=['county_name', 'year'], how='outer')
    
    df = df.replace(',', '', regex=True)
    df = df.replace(' (D)', np.nan)
    
    return df

def refine_animal_data(animal_df, animal_val):
    animal_nloss = animal_df.copy()
    animal_val_nloss = animal_val.copy()

    # Function to distribute population among all counties proportionally
    def distribute_population_proportionally(remaining_population, counties_population):
        if not counties_population:  # Check if counties_population is empty
            return []
        
        total_known_population = sum(counties_population)
        if total_known_population == 0:
            equal_distribution = remaining_population / len(counties_population)
            return [round(equal_distribution)] * len(counties_population)
        else:
            proportions = [pop / total_known_population for pop in counties_population]
            distributed_population = [remaining_population * proportion for proportion in proportions]
            return [round(pop) for pop in distributed_population]
    
    # Function to correct values in animal population data
    def correct_values(animal_type, df, val_df, interpolated_indices):
        for year in df['Year'].unique():
            interpolated_population = df.loc[(df['Year'] == year) & df.index.isin(interpolated_indices), animal_type].tolist()
            total_interpolated_population = sum(interpolated_population)
            state_population = val_df.loc[val_df['Year'] == year, animal_type].values[0]
            total_known_population = df.loc[df['Year'] == year, animal_type].sum()

            if not np.isnan(state_population):
                remaining_population = max(0, state_population - (total_known_population - total_interpolated_population))
                corrected_population = distribute_population_proportionally(remaining_population, interpolated_population)
                df.loc[(df['Year'] == year) & df.index.isin(interpolated_indices), animal_type] = corrected_population
    
    # Function to apply linear interpolation to specific columns
    def apply_interpolation(df, columns):
        interpolated_indices = {}
        for column in columns:
            # Record indices of NaN values before interpolation
            interpolated_indices[column] = df[df[column].isna()].index.tolist()
            
            df[column] = df.groupby('CountyName')[column].transform(lambda x: x.interpolate().round())
            df[column].fillna(method='ffill', inplace=True)
            df[column].fillna(method='bfill', inplace=True)
        return interpolated_indices

    common_animal_types = set(animal_nloss.columns) & set(animal_val_nloss.columns) - {'Year', 'CountyName'}

    # Apply linear interpolation first
    interpolated_indices = apply_interpolation(animal_nloss, common_animal_types)

    # Correct only interpolated values with proportional allocation
    for animal_type in common_animal_types:
        correct_values(animal_type, animal_nloss, animal_val_nloss, interpolated_indices[animal_type])

    #cattle
    animal_nloss['bulls'] = round(animal_nloss['beef']*0.05)
    animal_nloss['calves'] = round(animal_nloss['cattle'] - (animal_nloss['beef'] + animal_nloss['milk'] + animal_nloss['bulls'] + animal_nloss['steers']))
    animal_nloss['beef_heifers'] = round(animal_nloss['calves']*animal_nloss['beef']/(animal_nloss['beef']+animal_nloss['milk']))
    animal_nloss['dairy_150'] = round((1/2)*animal_nloss['calves']*animal_nloss['milk']/(animal_nloss['beef']+animal_nloss['milk']))
    animal_nloss['dairy_400'] = round((1/2)*animal_nloss['calves']*animal_nloss['milk']/(animal_nloss['beef']+animal_nloss['milk']))
    animal_nloss['fin_cattle'] = round((animal_nloss['steers'] + animal_nloss['onfeed_sold'])/3)
    #hogs
    animal_nloss['hogs_fin'] = round((animal_nloss['hogs'] + animal_nloss['hogs_sales'])/3)
    animal_nloss['hogs_sow'] = round(animal_nloss['hogs_breeding']/21)
    animal_nloss['hogs_boars'] = round(animal_nloss['hogs_breeding'] - animal_nloss['hogs_sow'])


    return animal_nloss

def interpolation(ifews_df):
    df = ifews_df.copy()
    county_names = df['CountyName'].unique()
    pop_names = ["corng_y",	"corng_pa",	"corng_ha",	"soy_y","soy_pa","soy_ha"]
        
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

            f = interp1d(x, y, kind = 'linear', fill_value="extrapolate")
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
    new_df = new_df.fillna({'hogs': np.nan, 'hogs_sales': np.nan, 'hogs_breeding':np.nan, 'beef': np.nan, 'milk': np.nan,
                             'cattle': np.nan, 'steers': np.nan, 'onfeed_sold':np.nan, 
                                 "corng_y":np.nan,	"corng_pa":np.nan,	"corng_ha":np.nan, "soy_y":np.nan,
                                 'soy_pa':np.nan, 'soy_ha':np.nan})
                                 #'broilers': np.nan, 'layers': np.nan, 'turkeys':np.nan,
    
    if 'corng_y' in new_df.columns:
        new_df = new_df.drop_duplicates(subset = ['CountyName', 'Year'])

    new_df = new_df[new_df['Year']<2023]        

    return new_df           

# function to calculate ManureN_kg_ha for each row
def calculate_manure_n(row):
    hogs_sows = row['hogs_sow']
    hogs_boars = row['hogs_boars']
    hogs_fin = row['hogs_fin']
    milk_cows = row['milk']
    beef_cows = row['beef']
    milk_cows_150 = row['dairy_150']
    milk_cows_440 = row['dairy_400']
    beef_bulls = row['bulls']
    calf = row['steers']
    cattle_fin = row['fin_cattle']
    soybeans_acres = row['soy_pa']
    corn_acres = row['corng_pa']
    
    # from Gronberg et al. (2017) and looking into nloss from Andersen, D. S., & Pepple, L. M. (2017) 
    manure_n = (hogs_sows * 0.036 * 365 +
                hogs_boars * 0.022 * 365 +
                hogs_fin * 0.028 * 365 +
                milk_cows * 0.2 * 365 +
                beef_cows * 0.029 * 365 +
                milk_cows_150 * 0.031 * 365 +
                milk_cows_440 * 0.060 * 365 +
                beef_bulls * 0.029 * 365 +
                calf * 0.019 * 365 +
                cattle_fin * 0.089 * 365) / (0.404686 * (soybeans_acres + corn_acres))
        
    return round(manure_n, 1)

# function for calculating fixation n
# soybeans bushels consider 1 metric ton/hectare = 14.87 (15) bushels/acre from https://www.extension.iastate.edu/agdm/wholefarm/pdf/c6-80.pdf
def calculate_fix_n(row):
    soybeans_yield = row['soy_y']
    soybeans_acres = row['soy_pa']
    corn_acres = row['corng_pa']
    
    fix_n = ((soybeans_yield/15)*81.1-98.5)*(soybeans_acres/(soybeans_acres+corn_acres))
    
    return round(fix_n, 1)

# function for calculation grain nitrogen
def calculate_grain_n(row):
    soybeans_yield = row['soy_y']
    corn_yield = row['corng_y']
    soybeans_acres_h = row['soy_ha']
    corn_acres_h = row['corng_ha']
    
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