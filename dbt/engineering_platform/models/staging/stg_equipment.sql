SELECT
    equipment_key,
    equipment_id,
    equipment_name,
    equipment_type,
    status AS equipment_status,
    manufacturer,
    effective_date,
    expiration_date,
    is_current
FROM {{ source('curated', 'dim_equipment') }}
WHERE is_current = TRUE
