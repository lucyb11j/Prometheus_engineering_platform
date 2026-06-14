SELECT
    date_key,
    project_key,
    vendor_key,
    planned_cost,
    actual_cost,
    cost_variance,
    forecast_cost
FROM "analytics_db"."curated"."fact_cost"