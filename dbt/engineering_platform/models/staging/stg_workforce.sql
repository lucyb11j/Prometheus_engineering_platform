SELECT
    date_key,
    employee_key,
    project_key,
    hours_worked,
    productivity_score
FROM {{ source('curated', 'fact_workforce') }}
