"""
lidar_dem_workflow.py
Author: Michael Adegbenro
Python: 3.8
Date: June 30th, 2023

Description:
Lidar-based terrain modeling workflow using ArcPy.
Generates DTM, DSM, CHM, performs DEM differencing (DoD),
and extracts max tree height using zonal statistics.

Note:
Requires Spatial Analyst Extension and a valid LAS dataset.
"""

import arcpy
import os

# --- CONFIGURATION ---
workspace = r"E:/GEOG656/Week5/Ex5.gdb"
las_directory = r"E:/GEOG656/Week5/"
las_dataset = "Drone Lidar March 2019.lasd"
cell_size = 0.1
year = 2019

# --- FUNCTION: Create DTM, DSM, CHM ---
def dtmdsmchm(workspace, las_dataset, cell_size, year):
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    arcpy.CheckOutExtension("spatial")
    
    print("*** Setup Complete ***")
    lasd = os.path.join(las_directory, las_dataset)

    # ---- DTM (Ground: class 1,2) ----
    laslyr = "laslayer_dtm"
    arcpy.MakeLasDatasetLayer_management(lasd, laslyr, "1;2")
    out_dtm = f"dtm_{year}"
    arcpy.LasDatasetToRaster_conversion(laslyr, out_dtm, "", "BINNING MINIMUM LINEAR", "", "", cell_size)
    dtm_raster = arcpy.sa.Raster(out_dtm)
    print(f"*** RASTER '{out_dtm}' CREATED ***")

    # ---- DSM (Vegetation: class 5) ----
    laslyr = "laslayer_dsm"
    arcpy.MakeLasDatasetLayer_management(lasd, laslyr, "5")
    out_dsm = f"dsm_{year}"
    arcpy.LasDatasetToRaster_conversion(laslyr, out_dsm, "", "BINNING MAXIMUM NONE", "", "", cell_size)
    dsm_raster = arcpy.sa.Raster(out_dsm)
    print(f"*** RASTER '{out_dsm}' CREATED ***")

    # ---- CHM (DSM - DTM) ----
    chm_raster = dsm_raster - dtm_raster
    chm_filled = arcpy.sa.Con(arcpy.sa.IsNull(chm_raster), 0, chm_raster)
    out_chm = f"chm_{year}"
    chm_filled.save(out_chm)
    print(f"*** RASTER '{out_chm}' CREATED ***")

# Example usage:
# dtmdsmchm(workspace, las_dataset, cell_size, 2019)

# --- FUNCTION: DEM of Difference ---
def calcDoDMeanChange(workspace, chm_old, chm_new, dod_name):
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    old = arcpy.sa.Raster(chm_old)
    new = arcpy.sa.Raster(chm_new)
    dod_raster = new - old
    dod_raster.save(dod_name)
    print(f"*** RASTER '{dod_name}' CREATED ***")

    mean_result = arcpy.management.GetRasterProperties(dod_name, "MEAN")
    mean_val = float(mean_result.getOutput(0))
    print(f"Mean Change ({chm_old} → {chm_new}) = {mean_val:.3f} meters")
    return mean_val

# Example:
# calcDoDMeanChange(workspace, "chm_2018", "chm_2019", "dod_1819")

# --- FUNCTION: Max Tree Height using CHM and Buffers ---
def maxTreeHeight(workspace, chm, tree_points, buffer_meters):
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    buffer_fc = "tree_buffer"
    output_table = f"{chm}_trees"

    arcpy.analysis.Buffer(tree_points, buffer_fc, buffer_meters)
    arcpy.sa.ZonalStatisticsAsTable(buffer_fc, "Id", chm, output_table, "NODATA", "MAXIMUM")
    print(f"*** TABLE '{output_table}' CREATED ***")

# Example:
# maxTreeHeight(workspace, "chm_2019", "tree_locations", 0.5)

# --- FUNCTION: Summary Tree Heights by Year ---
def getTreeStats(workspace):
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    print("\n*** MAXIMUM TREE HEIGHT (METERS) PER YEAR ***")
    print("YEAR  TREE 1  TREE 2  TREE 3  TREE 4")

    tables = [t for t in arcpy.ListTables() if "trees" in t]
    for table in sorted(tables):
        year = table.split("_")[1]
        heights = [row[0] for row in arcpy.da.SearchCursor(table, ["MAX"])]
        if len(heights) == 4:
            print(f"{year}  {heights[0]:.2f}   {heights[1]:.2f}   {heights[2]:.2f}   {heights[3]:.2f}")
        else:
            print(f"{year}  <Incomplete data>")

# Example:
# getTreeStats(workspace)
