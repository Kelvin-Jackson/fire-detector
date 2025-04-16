with sensor_satellite_data as (
    select
        sd.sensor_timestamp,
        md.modis_timestamp,
        sd.sensor_value,
        md.fire_lat,
        md.fire_long,
        md.bright_ti4,
        md.confidence,
        md.fire_radiative_power,
        md.daynight,
        row_number() over (partition by sd.sensor_timestamp order by abs(extract(epoch from sd.sensor_timestamp - md.modis_timestamp))) as rn
    from
        sensor_data sd
    left join modis_data md 
        on sd.sensor_timestamp between md.modis_timestamp - interval '2 minute' and md.modis_timestamp + interval '2 minute' -- you can adjust this interval
)
select 
    sensor_timestamp,
    modis_timestamp,
    sensor_value,
    fire_lat,
    fire_long,
    bright_ti4,
    confidence,
    fire_radiative_power,
    daynight,
    -- Creating 'fire_detected' column based on the new condition
    case 
        when fire_radiative_power > 2 or sensor_value > 300 then 1
        else 0
    end as fire_detected
from 
    sensor_satellite_data
where 
    rn = 1;
