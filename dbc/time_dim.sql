create table if not exists time_dim (
    time_id uint16 primary key,
    time time generated always as (make_time("hour", "minute", 0)),
    hour uint8 generated always as (divide(cast("time_id" as uint16), 100)),
    minute uint8 generated always as (mod(cast("time_id" as uint16), 100))
);

-- prepare insert_time as
--     insert into time_dim(time_id) values ($1::uint16);

prepare insert_times as
    insert into time_dim("time_id")
    (select "ACQ_TIME"::uint16 from query_table($1))
    on conflict do nothing;
