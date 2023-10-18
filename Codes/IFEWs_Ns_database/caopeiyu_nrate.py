
import os
# Get data
os.chdir(r'C:\Users\jbrittes\Documents\Research\IFEWs_model_v3_1\data')
# Import necessary libraries
import numpy as np
from shapely.geometry import mapping
import rioxarray as rxr
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats
import pandas as pd

# ------------------- Cao Peiyu -----------------------------------------------------
# get original data from Peiyu File - raster to points and aggregate to counties
# path
def nrate_original(parent_dir):
    dir_name1 = parent_dir + "\\N fertilizer maps US from 2022\\"

    files = os.listdir(dir_name1)

    # select only files containing years of interest. And as .tif
    # remove folder N fertilizer data
    files = [x for x in files if "N fertilizer data" not in x]

    # remove unwanted years
    y = [i for i in range(1900,1968,1)]
    y = [str(x) for x in y]
    for i in range(len(y)):
        files = [x for x in files if y[i] not in x]

    # Get boundary data
    file_boundary = os.path.join(parent_dir, "Iowa Counties", 'IowaCounties.shp')

    for idx, file in enumerate(files):
        # Open crop extent (your study area extent boundary)
        iowa = gpd.read_file(file_boundary)
        
        year = 1968 + idx
        f = os.path.join(dir_name1, file)
        # Open rasters
        fertilizer_im = rxr.open_rasterio(f, masked=True).squeeze()
        # Clip data
        nrate_clipped = fertilizer_im.rio.clip(iowa.geometry.apply(mapping),
                                        # This is needed if your GDF is in a diff CRS than the raster data
                                        iowa.crs)
        # export new data
        path_to_tif_file = os.path.join(parent_dir,
                                        "N fertilizer maps US from 2022",'N fertilizer data_Iowa', 
                                        file)

        # Write the data to a new geotiff file
        nrate_clipped.rio.to_raster(path_to_tif_file)
        
        # Convert the raster dataset to a point shapefile using rasterio
        with rasterio.open(path_to_tif_file) as src:
            data = src.read(1, masked=True)
            if not data.mask.all():
                meta = src.meta
                points = np.where(data.mask == False)
                if len(points) == 1:
                    lon, lat = src.xy(points[0], np.zeros_like(points[0]))
                else:
                    lon, lat = src.xy(points[0], points[1])
                df = pd.DataFrame({'Longitude': lon, 'Latitude': lat})
                geometry = gpd.points_from_xy(df.Longitude, df.Latitude)
                crs = src.crs
                point_gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
        
        iowa1 = iowa.to_crs(fertilizer_im.rio.crs)
        # Compute mean values of raster dataset in polygons of Iowa shapefile - shoud output 99 values (one for each county)
        stats = zonal_stats(iowa1, path_to_tif_file, stats='mean', nodata=-999)
        mean_vals = [feature['mean'] for feature in stats]
        iowa['CN_lb/ac'] = mean_vals
        
        # Add year column
        iowa['date'] = year

        # Change CRS to UTM zone 15N
        iowa_utm = iowa.to_crs(epsg=26915)

        #clean shapefiles
        iowa = iowa.drop(['FID', 'PERIMETER', 'DOMCountyI',  'FIPS', 'FIPS_INT', 'SHAPE_Leng', 'SHAPE_Area'], axis=1)

        #iowa['CountyName'] = iowa['CountyName'].replace('Obrien', "O brien")
        #iowa['CountyName'] = iowa['CountyName'].str.upper()
        
        # Save the shapefile
        path_to_shp_file = os.path.join(parent_dir,
                                        "N fertilizer maps US from 2022",'N fertilizer data_Iowa', 
                                        f"Nrate_{year}.shp")
        iowa_utm.to_file(path_to_shp_file)

# --------------- Aggregate Shapefiles in One shapefile (temporal series) ----------------------
# Read in each shapefile as a separate GeoDataFrame and store them in a list:
# path

def nrate_iowa_counties(parent_dir):
    # if more variables available - run nrate_original to update database
    #nrate_original(parent_dir = parent_dir)

    dir_name2 = parent_dir + "\\N fertilizer maps US from 2022\\N fertilizer data_Iowa"
    files = os.listdir(dir_name2)

    # select only shapefiles - remove files that are not shp
    files = [x for x in files if ".shp" in x]

    filepaths = []
    for file in files:
        f = os.path.join(dir_name2, file)
        filepaths.append(f)
        
    gdfs = []
    for filepath in filepaths:
        gdf = gpd.read_file(filepath)
        gdfs.append(gdf)    


    # Concatenate the list of geodata into a single one
    nrate_gdf = pd.concat(gdfs, ignore_index=True)

    # Extract the year from a column in the GeoDataFrame, and create a new column for the year
    nrate_gdf['date'] = pd.to_datetime(nrate_gdf['date'], format='%Y')
    nrate_gdf['Year'] = nrate_gdf['date'].dt.year

    # Drop date column and all unsuaful columns
    nrate_gdf = nrate_gdf.drop(['FID', 'PERIMETER', 'DOMCountyI',  'FIPS', 'FIPS_INT', 'SHAPE_Leng', 'SHAPE_Area', 'date'], axis=1)

    # Makes column names compatible with USDA data
    nrate_gdf.rename(columns={"StateAbbr":"State"}, inplace = True)
    nrate_gdf['CountyName'] = nrate_gdf['CountyName'].replace('Obrien', "O BRIEN")
    nrate_gdf['CountyName'] = nrate_gdf['CountyName'].str.upper()

    return nrate_gdf