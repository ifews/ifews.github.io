import urllib.parse
import pandas as pd

def encode_parameters(params):
    return urllib.parse.urlencode(params)

#Corn Grain Yield Bu/Acre
parameters1 =    'source_desc=SURVEY' +  \
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
parameters2 =    'source_desc=SURVEY' +  \
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

#Corn Silage Yield Tons/Acre
parameters3 =    'source_desc=SURVEY' +  \
                '&sector_desc=CROPS' + \
                '&commodity_desc=CORN' + \
                '&statisticcat_desc=YIELD' + \
                '&util_practice_desc=SILAGE' + \
                '&' + urllib.parse.quote('short_desc=CORN, SILAGE - YIELD, MEASURED IN TONS / ACRE') + \
                '&freq_desc=ANNUAL' + \
                '&reference_period_desc=YEAR' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

#Corn Area Planted Acres
parameters4 =    'source_desc=SURVEY' +  \
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
parameters5 =    'source_desc=SURVEY' +  \
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

#Corn Area Harvested Acres (silage)
parameters6 =    'source_desc=SURVEY' +  \
                '&sector_desc=CROPS' + \
                '&commodity_desc=CORN' + \
                '&util_practice_desc=SILAGE' + \
                '&statisticcat_desc__LIKE=HARVESTED' + \
                '&' + urllib.parse.quote('short_desc=CORN, SILAGE - ACRES HARVESTED') + \
                '&unit_desc=ACRES' + \
                '&freq_desc=ANNUAL' + \
                '&reference_period_desc=YEAR' + \
                '&year__GE=1968' + \
                '&agg_level_desc=COUNTY' + \
                '&state_name=IOWA' + \
                '&county_code__LT=998' + \
                '&format=CSV'

#Soybean Area Planted Acres
parameters7 =    'source_desc=SURVEY' +  \
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
parameters8 =    'source_desc=SURVEY' +  \
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

# Hogs
parameters9c =   'source_desc=CENSUS' +  \
               '&'+ urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
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

# Live Population of Beef Cows
parameters10c =   'source_desc=CENSUS' +  \
               '&' +urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
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
parameters11c =   'source_desc=CENSUS' +  \
                '&' +urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
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
# Cattle but Cows
parameters12c =   'source_desc=CENSUS' +  \
                '&' +urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
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

# Hogs
parameters9s =   'source_desc=SURVEY' +  \
               '&' + urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
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

# Live Population of Beef Cows
parameters10s =   'source_desc=SURVEY' +  \
               '&'+ urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
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
parameters11s =   'source_desc=SURVEY' +  \
                '&' +urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
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
# Cattle but Cows
parameters12s =   'source_desc=SURVEY' +  \
                '&' +urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
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
    #animal population cattle beef validation
    ap_cbval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+COWS%2C+BEEF+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cbval = ap_cbval[ap_cbval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cbval.rename(columns={'Value': 'Beef Cattle'}, inplace=True)
    ap_cmval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+COWS%2C+MILK+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cmval = ap_cmval[ap_cmval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cmval.rename(columns={'Value': 'Milk Cattle'}, inplace=True)
    ap_cicval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CATTLE%2C+INCL+CALVES+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+JAN')
    ap_cicval = ap_cicval[ap_cicval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_cicval.rename(columns={'Value': 'Other Cattle'}, inplace=True)
    ap_hval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=HOGS+-+INVENTORY&year__GE=1968&agg_level_desc=STATE&reference_period_desc=FIRST+OF+DEC')
    ap_hval = ap_hval[ap_hval['state_name'] == 'IOWA'][['Value', 'year']]
    ap_hval.rename(columns={'Value': 'Hogs'}, inplace=True)

    merged_data = pd.merge(ap_cicval, ap_hval, on='year', how='outer')
    merged_data = pd.merge(merged_data, ap_cmval, on='year', how='outer')
    merged_data = pd.merge(merged_data, ap_cbval, on='year', how='outer')

    merged_data = merged_data.replace(',', '', regex=True)
    cols = merged_data.columns.drop('year')
    merged_data[cols] = merged_data [cols].apply(pd.to_numeric, errors='coerce')
    merged_data.rename(columns={'year': 'Year'}, inplace=True)

    merged_data['Other Cattle'] = merged_data['Other Cattle']-(merged_data['Beef Cattle'] + merged_data['Milk Cattle'])
    return merged_data  

def cp(): #crop production
    # crop production corn yield validation
    cp_cyval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN%2C+GRAIN+-+YIELD%2C+MEASURED+IN+BU+%2F+ACRE&year__GE=1968&agg_level_desc=STATE')
    cp_cyval = cp_cyval[cp_cyval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_cyval.rename(columns={'Value': 'CGY'}, inplace=True)
    cp_chval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN%2C+GRAIN+-+ACRES+HARVESTED&year__GE=1968&agg_level_desc=STATE')
    cp_chval = cp_chval[cp_chval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_chval.rename(columns={'Value': 'CH'}, inplace=True)
    cp_cpval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=CORN+-+ACRES+PLANTED&year__GE=1968&agg_level_desc=STATE')
    cp_cpval = cp_cpval[cp_cpval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_cpval.rename(columns={'Value': 'CP'}, inplace=True)
    
    cp_syval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+YIELD%2C+MEASURED+IN+BU+%2F+ACRE&year__GE=1968&agg_level_desc=STATE')
    cp_syval = cp_syval[cp_syval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_syval.rename(columns={'Value': 'SY'}, inplace=True)
    cp_shval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+ACRES+HARVESTED&year__GE=1968&agg_level_desc=STATE')
    cp_shval = cp_shval[cp_shval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_shval.rename(columns={'Value': 'SH'}, inplace=True)
    cp_spval = pd.read_csv('https://api.usda-reports.penguinlabs.net/data.csv?short_desc=SOYBEANS+-+ACRES+PLANTED&year__GE=1968&agg_level_desc=STATE')
    cp_spval = cp_spval[cp_spval['state_name'] == 'IOWA'][['Value', 'year']]
    cp_spval.rename(columns={'Value': 'SP'}, inplace=True)


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