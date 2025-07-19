# gee_image_processing.py
# Author: Michael Adegbenro
# Description: A sample GEE Python API workflow for processing Sentinel-2 imagery
# using filters, masking, and visualization parameters.

import ee

# Initialize the Earth Engine module
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()

# -------------------------------
# PARAMETERS (Adjust as needed)
# -------------------------------

# Area of interest: Replace with your own geometry or use ee.Geometry.Polygon
aoi = ee.Geometry.Rectangle([30.0, 50.0, 31.0, 51.0])  # Example: Kyiv area

# Date range
start_date = '2022-06-01'
end_date = '2022-08-31'

# Cloud probability threshold for filtering
cloud_threshold = 20

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------

def mask_clouds(img):
    """Mask clouds using Sentinel-2 cloud probability layer."""
    cloud_prob = ee.Image(img.get('cloud_mask'))
    cloud_mask = cloud_prob.lt(cloud_threshold)
    return img.updateMask(cloud_mask).copyProperties(img, img.propertyNames())

# -------------------------------
# IMAGE COLLECTION
# -------------------------------

# Load Sentinel-2 surface reflectance data
s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterBounds(aoi) \
    .filterDate(start_date, end_date) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 50))

# Load corresponding cloud probability dataset
s2_clouds = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY') \
    .filterBounds(aoi) \
    .filterDate(start_date, end_date)

# Join cloud probability to reflectance images
def join_collections(img):
    cloud_img = s2_clouds.filter(ee.Filter.eq('system:index', img.get('system:index'))).first()
    return img.set('cloud_mask', cloud_img)

joined = s2.map(join_collections)
cloud_masked = joined.map(mask_clouds)

# -------------------------------
# COMPOSITE CREATION
# -------------------------------

# Create median composite
median_img = cloud_masked.median().clip(aoi)

# -------------------------------
# VISUALIZATION
# -------------------------------

# Visualization parameters
vis_params = {
    'min': 0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2']  # RGB
}

# (OPTIONAL) To export a thumbnail to your Google Drive (uncomment to use)
# from geemap import ee_export_image
# ee_export_image(median_img, filename='sentinel_median', scale=10, region=aoi)

# (OPTIONAL) Visualize in geemap (for Colab or Jupyter)
# import geemap
# Map = geemap.Map(center=[50.5, 30.5], zoom=8)
# Map.addLayer(median_img, vis_params, "Sentinel-2 RGB Median")
# Map.addLayer(aoi, {}, "AOI")
# Map
