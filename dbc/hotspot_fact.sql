create table if not exists hotspot_fact(
    latitude float,
    longitude float,
    scan float,
    track float,
    version string,
    temperature float,
    frp float,
    time_id uint16,
    date_id uint32, 
    sat_id uint8,
    primary key (latitude, longitude, sat_id, date_id, time_id),
    foreign key (time_id) references time_dim (time_id),
    foreign key (date_id) references date_dim (date_id),
    foreign key (sat_id) references sat_dim (id),
    foreign key (longitude, latitude) references reg_dim (longitude, latitude)
);
