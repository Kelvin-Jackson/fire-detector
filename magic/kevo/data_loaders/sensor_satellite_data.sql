with sensor_satellite_data as (
    select
        sd.timestamp,
        md.modis_timestamp,
        sd.smoke_value,
        md.fire_lat,
        md.fire_long,
        md.bright_ti4,
        md.confidence,
        md.fire_radiative_power,
        md.daynight,
        row_number() over (partition by sd.timestamp order by abs(extract(epoch from sd.timestamp - md.modis_timestamp))) as rn
    from
        smoke_data_new sd
    left join modis_data md 
        on sd.timestamp between md.modis_timestamp - interval '2 minute' and md.modis_timestamp + interval '2 minute' -- you can adjust this interval
)
select 
    timestamp,
    modis_timestamp,
    smoke_value,
    fire_lat,
    fire_long,
    bright_ti4,
    confidence,
    fire_radiative_power,
    daynight,
    -- Creating 'fire_detected' column based on the new condition
    case 
        when fire_radiative_power > 2 or smoke_value > 300 then 1
        else 0
    end as fire_detected
from 
    sensor_satellite_data
where 
    rn = 1;
