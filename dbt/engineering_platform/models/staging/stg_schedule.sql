SELECT
    date_key,
    project_key,
    planned_progress,
    actual_progress,
    schedule_variance,
    spi
FROM {{ source('curated', 'fact_schedule') }}
