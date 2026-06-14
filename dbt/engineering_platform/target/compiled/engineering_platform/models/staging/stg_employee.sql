SELECT
    employee_key,
    employee_id,
    full_name,
    department,
    role,
    salary,
    hire_date,
    effective_date,
    expiration_date,
    is_current
FROM "analytics_db"."curated"."dim_employee"
WHERE is_current = TRUE