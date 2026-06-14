SELECT
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    week,
    day,
    day_name
FROM {{ source('curated', 'dim_date') }}
