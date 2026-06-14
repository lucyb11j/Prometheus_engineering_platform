SELECT
    vendor_key,
    vendor_id,
    vendor_name,
    category AS vendor_category,
    country
FROM {{ source('curated', 'dim_vendor') }}
