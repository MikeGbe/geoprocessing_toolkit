
## Raster Processing Raster Processing Scripts
[Includes elevation models, land use rasters, binary rasters, reclassification, map algebra, zonal stats]

## LiDAR Raster Processing Scripts

This module provides a workflow for processing raw LAS datasets into Digital Terrain Models (DTMs), Digital Surface Models (DSMs), and Canopy Height Models (CHMs) using ArcPy. It includes:

- `dtmdsmchm()`: Generates DTM, DSM, CHM
- `calcDoDMeanChange()`: Calculates change over time between CHMs
- `maxTreeHeight()`: Buffers tree points and calculates max height using zonal statistics
- `getTreeStats()`: Summarizes tree height change across years

### Requirements
- ArcGIS Pro with Spatial Analyst
- LAS Dataset input
- CHM rasters and tree point layers for analysis

### Example Use
```python
dtmdsmchm(workspace, las_dataset, 0.1, 2019)
calcDoDMeanChange(workspace, "chm_2017", "chm_2019", "dod_1719")
maxTreeHeight(workspace, "chm_2019", "tree_locations", 0.5)
getTreeStats(workspace)
