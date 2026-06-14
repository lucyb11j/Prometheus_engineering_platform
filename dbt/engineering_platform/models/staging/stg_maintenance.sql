SELECT
    date_key,
    equipment_key,
    maintenance_type,
    downtime_hours,
    maintenance_cost
FROM {{ source('curated', 'fact_maintenance') }}
