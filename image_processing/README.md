# Image Processing with Google Earth Engine

This module uses the Earth Engine Python API to filter, process, and export Landsat 8 imagery over a defined area using a GeoJSON file.

## Features
- Filters imagery by geometry, date, and cloud cover
- Selects RGB bands and scales them for export
- Supports exporting images directly to Google Drive

## Requirements
- [Google Earth Engine Python API](https://developers.google.com/earth-engine/python_install)
- geopandas
- json
- Python 3.8+

## How to Run
Update the `getImage()` function call with the proper file path and year.

```python
getImage("E:/path/to/json", "yourfile.json", 2020)
```

Make sure you authenticate Earth Engine before running.
