-- describe select * from read_parquet('s3://firms-processed/*.parquet');
-- create table if not exists data_261011
-- as select * from read_parquet('s3://firms-processed/UNZIP_2026-10-11.parquet');

-- -- DATE DIMENSION
-- select distinct
--     cast(strftime(ACQ_DATE, '%y%m%d') as uint32) AS date_id,
--     date(ACQ_DATE) AS "date",
--     day(ACQ_DATE) AS "day",
--     month(ACQ_DATE) AS "month",
--     year(ACQ_DATE) AS "year"
-- from data_260922
-- order by date_id;

-- -- TIME DIMENSION
-- select distinct
--     CAST(ACQ_TIME AS int) AS time_id,
--     divide(CAST(ACQ_TIME AS int), 100) AS "hour",
--     mod(CAST(ACQ_TIME AS int), 100) AS "minute",
--     strptime(ACQ_TIME, '%H%M')::time AS "time"
-- from data_260922;

-- REGION DIMENSION
select distinct
    LONGITUDE,
    LATITUDE
from data_260922
order by LONGITUDE, LATITUDE;
