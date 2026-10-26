create table if not exists reg_dim(
    longitude float,
    latitude float,
    state text,
    region text,
    country text,
    country_code text,
    constraint pk_reg_dim primary key (longitude, latitude)
);

-- select
--     max(lat) as latitude,
--     max(lon) as longitude,
--     max(town) as town,
--     max(state) as state,
--     max(region) as region,
--     max(country) as country,
--     max(country_code) as country_code
-- from (
--     select read_xml(format('https://nominatim.openstreetmap.org/reverse?lat={}&lon={}', LATITUDE, LONGITUDE))
--     from data_261011
-- );

-- select LATITUDE, LONGITUDE from data_261011 limit 1;

