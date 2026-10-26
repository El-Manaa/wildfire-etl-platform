create table if not exists date_dim(
    date_id uint32 primary key,
    "date" date not null,
    "day" uint8 generated always as (day("date")),
    "month" uint8 generated always as (month("date")),
    "year" uint16 generated always as (year("date")),
    -- constraint pk_date primary key ("date_id")
);

-- prepare insert_date as 
--     insert into date_dim(date_id, "date")
--     values (strftime(date($1), '%y%m%d')::uint32, date($1));

prepare insert_dates as
    insert into date_dim(date_id, "date")
    (
        select strftime(date("ACQ_DATE"), '%y%m%d')::uint32, date("ACQ_DATE")
        from query_table($1)
    ) on conflict do nothing;
