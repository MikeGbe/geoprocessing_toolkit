# Google Earth Engine Image Processing Script (Python API)
# This script filters and exports satellite imagery using GEE and a local GeoJSON file

import ee
import geopandas as gpd
import json
import os

ee.Initialize()

def getImage(work, area, year):
    class jsonError(Exception): pass
    class yearError(Exception): pass
    try:
        if area.split(".")[1] != "json":
            raise jsonError
        if year not in range(2013, 2024):
            raise yearError
        gpd_json = gpd.read_file(os.path.join(work, area))
        json_str = gpd_json.to_json()
        jdict = json.loads(json_str)
        json_geo = jdict['features'][0]['geometry']['coordinates']
        garea = ee.Geometry.Polygon(json_geo)
        collection = ee.ImageCollection("LANDSAT/LC08/C02/T1_RT_TOA")
        collection_AOI = collection.filterBounds(garea).filterDate(f"{year}-01-01", f"{year}-12-01")
        least_cloudy = ee.Image(collection_AOI.sort('CLOUD_COVER').first())
        image_rgb = least_cloudy.select(['B4', 'B3', 'B2']).multiply(512).uint8()
        filename = area.split(".")[0] + '_' + str(year)
        task = ee.batch.Export.image.toDrive(image_rgb, folder="GEE", description=filename, dimensions=720, region=garea)
        task.start()
        print(f"Exporting image '{filename}.tif' to Google Drive")
    except jsonError:
        print("Error: Input File must be a JSON File")
    except yearError:
        print("Error: Input Year is Not Valid")

# Example call:
# getImage("E:/GEOG656/Week9", "kyiv.json", 2020)
