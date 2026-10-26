[![Burning Trees](./burning-trees.gif)](#)
# Wildfire ETL Platform
## An ETL Platform to process and store wildfire data.

Source: [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/active_fire/)\
Raw data format:
  + A zipfile containing:
    - .shp (Shapefile): Geomatry file that contains the coordinates of the Fire Spots
    - .dbf (dBase database file): Shapefile attribute format
    - .cpg (Character encoding file): a file format containing a set of characters of text in shapefile in different languages depending on the location.
    - .shx (Shape index format): a file that stores index and offset information from the main Shapefile (.shp).
    - .prj (Projection description): a project file from dBase.

## Architecture
```mermaid
flowchart
    subgraph SRC["Data Source"]
        ZIP[(Zip archive)]
    end
    J0(( ))
    ZIP -- download zip files --> J0
    subgraph O["Object Storage"]
        M@{shape: lin-cyl, label: "MinIO"}
    end
    subgraph E["Extract"]
        E1[VIIRS 375m / NOAA-20]
        E2[VIIRS 375m / NOAA-21]
        J1(( ))
    end
    subgraph T["Transform"]
        T1["Extract Zip contents"]
        T2["Read data from\nthe extracted content"]
        T3["Merge and Write data into\na Parquet file for each\ntable"]
    end
    J0 --> E1 & E2
    E1 & E2  --> J1
    J1 .-> T1
    T1 --> T2 --> T3
    subgraph L["Load"]
        L1["Upload Parquet"]
    end
    T3 --> L1
    L1 -- upload parquet file --> M
    subgraph D[Columnar Database]
        DB@{shape: cyl, label: "DuckDB"}
    end
    M -- integrate data --> DB
    subgraph G[GIS Dashboard]
        Q[QGIS]
    end
    M -- Show the Map --> Q
    subgraph DSB[Dashboard]
        V[Unknown]
    end
    DB -- Visualize Data --> V
```

## Data Model
I used Star Schema Model for the Data Warehouse.
```mermaid
---
    title: Hello
---
erDiagram
    Date_Dim ||--|{ Hotspot_Fct : hi
    Time_Dim ||--|{ Hotspot_Fct : hi
    Hotspot_Fct }|--|| Region_Dim : hi
    Hotspot_Fct }|--|| Satellite_Dim : hi
```

## Tech Stack
![Podman](https://img.shields.io/badge/Podman-%23892CA0.svg?style=for-the-badge&logo=podman&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=fff)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=fff)
![Duckdb](https://img.shields.io/badge/duckdb-%23FFF000.svg?style=for-the-badge&logo=duckdb&logoColor=black)
![MinIO](https://img.shields.io/badge/MinIO-C72E49?logo=minio&logoColor=fff&style=for-the-badge)
<!-- ![Qgis](https://img.shields.io/badge/qgis-%23589632.svg?style=for-the-badge&logo=qgis&logoColor=white) -->
