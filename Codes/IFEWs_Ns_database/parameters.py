import urllib.parse
import pandas as pd
from c_usda_quick_stats import c_usda_quick_stats

def encode_parameters(params):
    return urllib.parse.urlencode(params)

#Corn Grain Yield Bu/Acre
corng_y=    'source_desc=SURVEY' +  \
                '&sector_desc=CROPS' + \
                '&commodity_desc=CORN' + \
                '&statisticcat_desc=YIELD' + \
                '&util_practice_desc=GRAIN' + \
                '&' + urllib.parse.quote('short_desc=CORN, GRAIN - YIELD, MEASURED IN BU / ACRE') + \
                '&freq_desc=ANNUAL' + \
                '&reference_period_desc=YEAR' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

#Soybean Yield Bu/Acre
soy_y =    'source_desc=SURVEY' +  \
                '&sector_desc=CROPS' + \
                '&commodity_desc=SOYBEANS' + \
                '&statisticcat_desc=YIELD' + \
                '&' + urllib.parse.quote('short_desc=SOYBEANS - YIELD, MEASURED IN BU / ACRE') + \
                '&freq_desc=ANNUAL' + \
                '&reference_period_desc=YEAR' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&format=CSV'

# #Corn Silage Yield Tons/Acre
# parameters3 =    'source_desc=SURVEY' +  \
#                 '&sector_desc=CROPS' + \
#                 '&commodity_desc=CORN' + \
#                 '&statisticcat_desc=YIELD' + \
#                 '&util_practice_desc=SILAGE' + \
#                 '&' + urllib.parse.quote('short_desc=CORN, SILAGE - YIELD, MEASURED IN TONS / ACRE') + \
#                 '&freq_desc=ANNUAL' + \
#                 '&reference_period_desc=YEAR' + \
#                 '&year__GE=1968' + \
#                 '&agg_level_desc=COUNTY' + \
#                 '&state_name=IOWA' + \
#                 '&county_code__LT=998' + \
#                 '&format=CSV'

#Corn Area Planted Acres
corng_pa =    'source_desc=SURVEY' +  \
                '&sector_desc=CROPS' + \
                '&commodity_desc=CORN' + \
                '&statisticcat_desc__LIKE=PLANTED' + \
                '&' + urllib.parse.quote('short_desc=CORN - ACRES PLANTED') + \
                '&unit_desc=ACRES' + \
                '&freq_desc=ANNUAL' + \
                '&reference_period_desc=YEAR' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

#Corn Area Harvested Acres (grain)
corng_ha=    'source_desc=SURVEY' +  \
                '&sector_desc=CROPS' + \
                '&commodity_desc=CORN' + \
                '&util_practice_desc=GRAIN' + \
                '&statisticcat_desc__LIKE=HARVESTED' + \
                '&' + urllib.parse.quote('short_desc=CORN, GRAIN - ACRES HARVESTED') + \
                '&unit_desc=ACRES' + \
                '&freq_desc=ANNUAL' + \
                '&reference_period_desc=YEAR' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

# #Corn Area Harvested Acres (silage)
# parameters6 =    'source_desc=SURVEY' +  \
#                 '&sector_desc=CROPS' + \
#                 '&commodity_desc=CORN' + \
#                 '&util_practice_desc=SILAGE' + \
#                 '&statisticcat_desc__LIKE=HARVESTED' + \
#                 '&' + urllib.parse.quote('short_desc=CORN, SILAGE - ACRES HARVESTED') + \
#                 '&unit_desc=ACRES' + \
#                 '&freq_desc=ANNUAL' + \
#                 '&reference_period_desc=YEAR' + \
#                 '&year__GE=1968' + \
#                 '&agg_level_desc=COUNTY' + \
#                 '&state_name=IOWA' + \
#                 '&county_code__LT=998' + \
#                 '&format=CSV'

#Soybean Area Planted Acres
soy_pa =    'source_desc=SURVEY' +  \
                '&sector_desc=CROPS' + \
                '&' + urllib.parse.quote('group_desc=FIELD CROPS') + \
                '&commodity_desc=SOYBEANS' + \
                '&statisticcat_desc__LIKE=PLANTED' + \
                '&' + urllib.parse.quote('short_desc=SOYBEANS - ACRES PLANTED') + \
                '&unit_desc=ACRES' + \
                '&freq_desc=ANNUAL' + \
                '&reference_period_desc=YEAR' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

#Soybean Area Harvested Acres
soy_ha =    'source_desc=SURVEY' +  \
                '&sector_desc=CROPS' + \
                '&' + urllib.parse.quote('group_desc=FIELD CROPS') + \
                '&commodity_desc=SOYBEANS' + \
                '&statisticcat_desc__LIKE=HARVESTED' + \
                '&' + urllib.parse.quote('short_desc=SOYBEANS - ACRES PLANTED') + \
                '&unit_desc=ACRES' + \
                '&freq_desc=ANNUAL' + \
                '&reference_period_desc=YEAR' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'
# -------------------------- Census and Suryey -----------------------------------------
# Hogs
hogs =   urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
                '&group_desc=LIVESTOCK' + \
                '&commodity_desc=HOGS' + \
                '&statisticcat_desc=INVENTORY' + \
                '&domain_desc=TOTAL' + \
                '&' + urllib.parse.quote('domaincat_desc=NOT SPECIFIED') + \
                '&unit_desc=HEAD' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

# Breeding hogs inventory - sows + boars ratio 20:1 and # Hogs sales
hogs_others =  urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
                '&group_desc=LIVESTOCK' + \
                '&commodity_desc=HOGS' + \
                '&' + urllib.parse.quote('util_practice_desc= BREEDING') + \
                '&' + urllib.parse.quote('domaincat_desc=NOT SPECIFIED') + \
                '&unit_desc=HEAD' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

# Beef Cows
beef =    urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
                '&group_desc=LIVESTOCK' + \
                '&commodity_desc=CATTLE' + \
                '&class_desc__LIKE=BEEF' + \
                '&statisticcat_desc=INVENTORY' + \
                '&domain_desc=TOTAL' + \
                '&' + urllib.parse.quote('domaincat_desc=NOT SPECIFIED') + \
                '&unit_desc=HEAD' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'
# Milk
milk =   urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
                '&group_desc=LIVESTOCK' + \
                '&commodity_desc=CATTLE' + \
                '&class_desc__LIKE=MILK' + \
                '&statisticcat_desc=INVENTORY' + \
                '&domain_desc=TOTAL' + \
                '&' + urllib.parse.quote('domaincat_desc=NOT SPECIFIED') + \
                '&unit_desc=HEAD' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'
# All cattle
other_cattle =   urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
                '&group_desc=LIVESTOCK' + \
                '&commodity_desc=CATTLE' + \
                '&' +urllib.parse.quote('class_desc=INCL CALVES') + \
                '&statisticcat_desc=INVENTORY' + \
                '&unit_desc=HEAD' + \
                    '&' +urllib.parse.quote('short_desc=CATTLE, INCL CALVES - INVENTORY') + \
                    '&domain_desc=TOTAL' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

# Cattle on Feed = steers and on feed sales - CATTLE, ON FEED - INVENTORY', 'CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD'
on_feed =   urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
            '&group_desc=LIVESTOCK' + \
            '&commodity_desc=CATTLE' + \
            '&' +urllib.parse.quote('prodn_practice_desc=ON FEED') + \
            '&' +urllib.parse.quote('domain_desc=SALES') + \
            '&unit_desc=HEAD' + \
            '&year__GE=1968' + \
            '&agg_level_desc=COUNTY' + \
            '&state_name=IOWA' + \
            '&county_code__LT=998' + \
            '&format=CSV'

# # Chicken = 'CHICKENS, LAYERS - INVENTORY', 'CHICKENS, BROILERS - INVENTORY',
# chicken =   urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
#             '&group_desc=POULTRY' + \
#             '&commodity_desc=CHICKENS' + \
#             '&unit_desc=HEAD' + \
#             '&year__GE=1968' + \
#             '&agg_level_desc=COUNTY' + \
#             '&state_name=IOWA' + \
#             '&county_code__LT=998' + \
#             '&format=CSV'   

# # Turkeys 'TURKEYS - INVENTORY'
# turkeys =   urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
#             '&group_desc=POULTRY' + \
#             '&commodity_desc=TURKEYS' + \
#             '&unit_desc=HEAD' + \
#             '&year__GE=1968' + \
#             '&agg_level_desc=COUNTY' + \
#             '&state_name=IOWA' + \
#             '&county_code__LT=998' + \
#             '&format=CSV'     

# # Slaughtered Population Hogs
# parameters13 =    'source_desc=SURVEY' +  \
#                 '&' + urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
#                 '&group_desc=LIVESTOCK' + \
#                 '&commodity_desc=HOGS' + \
#                 '&class_desc__LIKE=ALL' + \
#                 '&util_practice_desc__LIKE=SLAUGHTER'+ \
#                 '&domain_desc=TOTAL' + \
#                 '&reference_period_desc=YEAR' + \
#                 '&year__GE=1968' + \
#                 '&agg_level_desc=STATE' + \
#                 '&state_name=IOWA' + \
#                 '&format=CSV'

# # Slaughtered Population Cattle - NO DIFFERENTIATION BETWEEN BULLS, CALVES, COWS, WEIGHT, HEIFERS AND STEERS - look into this
# parameters14 =    'source_desc=SURVEY' +  \
#                 '&' + urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
#                 '&group_desc=LIVESTOCK' + \
#                 '&commodity_desc=CATTLE' + \
#                 '&util_practice_desc__LIKE=SLAUGHTER'+ \
#                 '&domain_desc=TOTAL' + \
#                 '&reference_period_desc=YEAR' + \
#                 '&year__GE=1968' + \
#                 '&agg_level_desc=STATE' + \
#                 '&state_name=IOWA' + \
#                 '&format=CSV'

# # Slaughtered Population Poultry Slaughtered in LB live basis
# parameters15 =    'source_desc=SURVEY' +  \
#                 '&' + urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
#                 '&group_desc=POULTRY' + \
#                 '&commodity_desc__LIKE=TOTALS' + \
#                 '&statisticcat_desc=SLAUGHTERED'+ \
#                 '&domain_desc=TOTAL' + \
#                 '&reference_period_desc=YEAR' + \
#                 '&year__GE=1968' + \
#                 '&agg_level_desc=NATIONAL' + \
#                 '&format=CSV'



def ap(): #animal population
    # Cattle
    ap_cbval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+COWS%2C+BEEF+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cbval = ap_cbval[ap_cbval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cbval.rename(columns={'Value': 'beef'}, inplace=True)
    ap_cmval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+COWS%2C+MILK+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cmval = ap_cmval[ap_cmval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cmval.rename(columns={'Value': 'milk'}, inplace=True)
    ap_cicval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+INCL+CALVES+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cicval = ap_cicval[ap_cicval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cicval.rename(columns={'Value': 'cattle'}, inplace=True)
    #on feed
    on_feed_s =   urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
            '&group_desc=LIVESTOCK' + \
            '&commodity_desc=CATTLE' + \
            '&' +urllib.parse.quote('prodn_practice_desc=ON FEED') + \
            '&' +urllib.parse.quote('domain_desc=SALES') + \
            '&unit_desc=HEAD' + \
            '&year__GE=1968' + \
            '&agg_level_desc=STATE' + \
            '&state_name=IOWA' + \
            '&format=CSV'
    
    stats = c_usda_quick_stats()
    df = stats.get_data(on_feed_s)
    # cattle steers
    ap_csval = df[(df['short_desc'] == 'CATTLE, ON FEED - INVENTORY') & (df['domain_desc'] == 'TOTAL')][['Value', 'year']]
    ap_csval.rename(columns={'Value': 'steers'}, inplace=True)
    # cattle for sale
    ap_sval = df[(df['short_desc'] == 'CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD') & (df['domain_desc'] == 'TOTAL')][['Value', 'year']]
    ap_sval.rename(columns={'Value': 'onfeed_sold'}, inplace=True)
    
    # Hogs
    ap_hval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=HOGS+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+DEC')
    ap_hval = ap_hval[ap_hval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_hval.rename(columns={'Value': 'hogs'}, inplace=True)
    ap_hbval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=HOGS,+BREEDING+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+DEC')
    ap_hbval = ap_hbval[ap_hbval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_hbval.rename(columns={'Value': 'hogs_breeding'}, inplace=True)
    ap_hsval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=HOGS+-+SALES,+MEASURED+IN+HEAD&year__GE=1968&agg_level_desc=STATE&reference_period_desc=YEAR')
    ap_hsval = ap_hsval[ap_hsval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_hsval.rename(columns={'Value': 'hogs_sales'}, inplace=True)

    merged_data= ap_cbval.merge(ap_cmval, on='year', how='outer')\
                    .merge(ap_cicval, on='year', how='outer')\
                    .merge(ap_csval, on='year', how='outer')\
                    .merge(ap_sval, on='year', how='outer')\
                    .merge(ap_hval, on='year', how='outer')\
                    .merge(ap_hbval, on='year', how='outer')\
                    .merge(ap_hsval, on='year', how='outer')

    merged_data = merged_data.replace(',', '', regex=True)
    cols = merged_data.columns.drop('year')
    merged_data[cols] = merged_data [cols].apply(pd.to_numeric, errors='coerce')
    merged_data.rename(columns={'year': 'Year'}, inplace=True)

    #merged_data['Other Cattle'] = merged_data['Other Cattle']-(merged_data['Beef Cattle'] + merged_data['Milk Cattle'])
    return merged_data  

def cp(): #crop production
    # crop production corn yield validation
    cp_cyval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN%2C+GRAIN+-+YIELD%2C+MEASURED+IN+BU+%2F+ACRE&year__GE=1968&agg_level_desc=STATE')
    cp_cyval = cp_cyval[cp_cyval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_cyval.rename(columns={'Value': 'corng_y'}, inplace=True)
    cp_chval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN%2C+GRAIN+-+ACRES+HARVESTED&year__GE=1968&agg_level_desc=STATE')
    cp_chval = cp_chval[cp_chval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_chval.rename(columns={'Value': 'corng_ha'}, inplace=True)
    cp_cpval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN+-+ACRES+PLANTED&year__GE=1968&agg_level_desc=STATE')
    cp_cpval = cp_cpval[cp_cpval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_cpval.rename(columns={'Value': 'corng_pa'}, inplace=True)
    
    cp_syval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+YIELD%2C+MEASURED+IN+BU+%2F+ACRE&year__GE=1968&agg_level_desc=STATE')
    cp_syval = cp_syval[cp_syval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_syval.rename(columns={'Value': 'soy_y'}, inplace=True)
    cp_shval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+ACRES+HARVESTED&year__GE=1968&agg_level_desc=STATE')
    cp_shval = cp_shval[cp_shval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_shval.rename(columns={'Value': 'soy_ha'}, inplace=True)
    cp_spval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+ACRES+PLANTED&year__GE=1968&agg_level_desc=STATE')
    cp_spval = cp_spval[cp_spval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_spval.rename(columns={'Value': 'soy_pa'}, inplace=True)


    merged_data = pd.merge(cp_cyval, cp_chval, on='year', how='outer')
    merged_data = pd.merge(merged_data, cp_cpval, on='year', how='outer')
    merged_data = pd.merge(merged_data, cp_syval, on='year', how='outer')
    merged_data = pd.merge(merged_data, cp_shval, on='year', how='outer')
    merged_data = pd.merge(merged_data, cp_spval, on='year', how='outer')

    merged_data = merged_data.replace(',', '', regex=True)
    cols = merged_data.columns.drop('year')
    merged_data[cols] = merged_data[cols].apply(pd.to_numeric, errors='coerce')
    merged_data.rename(columns={'year': 'Year'}, inplace=True)

    return merged_data  