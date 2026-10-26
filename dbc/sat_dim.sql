create table if not exists sat_dim(
    id utinyint primary key,
    code varchar check(code in ('N', 'N20', 'N21')),
    name varchar(3) generated always as (case
        when code = 'N' then 'SUOMI NPP'
        when code = 'N20' then 'NOAA-20'
        when code = 'N21' then 'NOAA-21'
    end)
);


prepare insert_sats as
    insert into sat_dim(id, code)
    (
        select
            case
                when SATELLITE = 'N' then 0
                when SATELLITE = 'N20' then 1
                when SATELLITE = 'N21' then 2
            end as id,
            SATELLITE as code
        from query_table($1)
    ) on conflict do nothing;

