SELECT
    location_key,
    location_id,
    country,
    region,
    city,
    site_name
FROM {{ source('curated', 'dim_location') }}
