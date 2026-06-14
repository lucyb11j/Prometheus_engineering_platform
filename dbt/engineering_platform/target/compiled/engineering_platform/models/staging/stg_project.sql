SELECT
    project_key,
    project_id,
    project_name,
    project_type,
    status,
    budget,
    location_key,
    start_date,
    planned_end_date,
    effective_date,
    expiration_date,
    is_current
FROM "analytics_db"."curated"."dim_project"
WHERE is_current = TRUE