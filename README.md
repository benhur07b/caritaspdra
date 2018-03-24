
# Caritas PDRA Analysis tool
The Caritas Participatory Disaster Risk Assessment (PDRA) Analysis Tool is a QGIS plugin that performs different analysis using Caritas Philippines PDRA data.

## Versions
The tool has 2 working versions: the *shp-version* and the *gpkg-version*. Both versions work in exactly the same way but vary on the type of input they are optimized for.

### gpkg-version
- optimized for handling PDRA data in GeoPackage (.gpkg) format where the **FIELDNAMES** are the **INDICATOR_NAMES** provided in the PDRA Indicator List CSV

### shp-version
- optimized for handling PDRA data in Shapefile (.shp) format where the **FIELDNAMES** are the **INDICATOR_CODES** provided in the PDRA Indicator List CSV

## PDRA Indicators CSV
Comma-separated value (CSV) files containing the PDRA indicators used in the analysis can be found insed the **indicators** folder.

### PDRA Household Indicators
- **FILE** : _pdra-household-indicators.csv_
- **COLUMNS**
	- INDICATOR_CODE - used as FIELDNAME for the shp-version
    - INDICATOR_NAME - used as FIELDNAME in the gpkg-version
    - CATEGORY - Indicator category (e.g. Hazard, Vulnerability, Capacity, Risk)
    - VALUE - Value of the Indicator in computing for the household's level of Hazard, Vulnerability, and Capacity. A value of 1 means that the household's level (of Hazard, Vulnerability, or Capacity depending on the indicator category) is increased when the indicator is present.

## Installing the Plugin
1. Choose which version to download:
	-	_gpkg-version_ - [https://github.com/benhur07b/caritaspdra/tree/shp-version](https://github.com/benhur07b/caritaspdra/tree/gpkg-version)
	-	_shp-version_ - [https://github.com/benhur07b/caritaspdra/tree/shp-version](https://github.com/benhur07b/caritaspdra/tree/shp-version)
2. Go to **Clone or Download** and Click **Download ZIP**.
3. Unzip the zipped file to your QGIS3 profile's plugins folder.
	-	Here are the "standard" locations for Linux, Mac, and Windows, as found under your HOME directory (Thanks to Mr. Gary Sherman for [this](http://spatialgalaxy.net/2018/03/12/where-is-my-.qgis3-folder/):
		-	Linux: ```.local/share/QGIS/QGIS3/profiles/default```
		-   Mac OS X: ```Library/Application Support/QGIS/QGIS3/profiles/default```
		-   Windows: ```AppData\Roaming\QGIS\QGIS3\profiles\default```
4. Open the **Manage and Install Plugins** Dialog in QGIS via ```Plugins -> Manage and Install Plugins```
5. Activate Caritas PDRA Analysis Tool
