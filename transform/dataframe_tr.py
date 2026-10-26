from polars import Enum
from transform.transformation_functions import (
    satellite_name, satellite_name_id,
    int_to_time, get_country_sh
)
from os import listdir
from pathlib import Path
from glob import glob
from geopandas import read_file as gpd_read_file
from pandas import concat
from polars import (
    LazyFrame, col, UInt8, UInt16, UInt32,
    Time, struct, Struct, String
)

def get_lazyframe(folder: Path) -> LazyFrame:
    return LazyFrame(concat(
        (
            gpd_read_file(
                glob(str(folder/file/"*.shp"))[0]
            ).drop(columns=['geometry'])
            for file in listdir(folder)
        )
    )).drop('__index_level__', 'geom', strict=False).filter(
        col.SATELLITE.is_in(('N20', 'N21'))
    )

def make_date_dim(lf: LazyFrame) -> LazyFrame:
    return lf.select(date=col.ACQ_DATE.dt.date()).with_columns(
        date_id = col.date.dt.strftime("%y%m%d").cast(UInt32),
        day = col.date.dt.day().cast(UInt8),
        month = col.date.dt.month().cast(UInt8),
        year = col.date.dt.year().cast(UInt16)
    )

def make_time_dim(lf: LazyFrame) -> LazyFrame:
    return lf.select(
        time_id = col.ACQ_TIME.cast(UInt16),
        daynight = col.DAYNIGHT
    ).with_columns(
        time = col.time_id.map_elements(int_to_time, return_dtype=Time)
    ).with_columns(
        hour = col.time.dt.hour().cast(UInt8),
        minute = col.time.dt.minute().cast(UInt8)
    )

SAT_ENUM = Enum(("N20", "N21"))

def make_sat_dim(lf: LazyFrame) -> LazyFrame:
    return lf.select(
        code=col.SATELLITE
    ).filter(col.code.is_in(('N20', 'N21'))).unique().with_columns(
        code = col.code.cast(SAT_ENUM),
        name = col.code.map_elements(satellite_name),
        id = col.code.map_elements(satellite_name_id).cast(UInt8)
    )

REG_STRUCT = Struct({
    'state': String,
    'region': String,
    'country': String,
    'country_code': String 
})

def make_reg_dim(lf: LazyFrame) -> LazyFrame:
    return lf.select(
        latitude=col.LATITUDE,
        longitude=col.LONGITUDE
    ).with_columns(
        country = struct(("longitude","latitude"))
            .map_elements(
                get_country_sh,
                return_dtype=REG_STRUCT
            )
    ).unnest("country").with_columns(
        country_code = col.country_code.str.to_uppercase()
    )

def make_hotspot_fact(lf: LazyFrame) -> LazyFrame:
    return lf.select(
        temperature=col.BRIGHT_TI4 - 273.15,
        frp=col.FRP,
        scan=col.SCAN,
        track=col.TRACK,
        version=col.VERSION,
        latitude=col.LATITUDE,
        longitude=col.LONGITUDE,
        time_id=col.ACQ_TIME,
        date_id=col.ACQ_DATE.dt.strftime("%y%m%d").cast(UInt32),
        sat_id=col.SATELLITE.map_elements(satellite_name_id, return_dtype=UInt8)
    )

def prepare_all_tables(lf: LazyFrame):
    for table in (
        'date_dim',
        'time_dim',
        'sat_dim',
        'reg_dim',
        'hotspot_fact'
    ):
        yield (table, eval(f'make_{table}')(lf))
