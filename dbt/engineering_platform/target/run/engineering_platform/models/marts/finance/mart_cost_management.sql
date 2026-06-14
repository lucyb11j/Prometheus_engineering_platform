
  
    

  create  table "analytics_db"."curated"."mart_cost_management__dbt_tmp"
  
  
    as
  
  (
    

WITH cost_detail AS (
    SELECT
        fc.date_key,
        dd.year,
        dd.month,
        dd.month_name,
        fc.project_key,
        dp.project_id,
        dp.project_name,
        dp.project_type,
        fc.vendor_key,
        dv.vendor_name,
        dv.vendor_category,
        fc.planned_cost,
        fc.actual_cost,
        fc.cost_variance,
        fc.forecast_cost
    FROM "analytics_db"."curated"."stg_cost" fc
    INNER JOIN "analytics_db"."curated"."stg_date" dd ON fc.date_key = dd.date_key
    INNER JOIN "analytics_db"."curated"."stg_project" dp ON fc.project_key = dp.project_key
    INNER JOIN "analytics_db"."curated"."stg_vendor" dv ON fc.vendor_key = dv.vendor_key
),

vendor_spend AS (
    SELECT
        vendor_key,
        vendor_name,
        vendor_category,
        year,
        month,
        SUM(actual_cost) AS monthly_spend,
        SUM(planned_cost) AS monthly_planned,
        COUNT(DISTINCT project_key) AS project_count
    FROM cost_detail
    GROUP BY vendor_key, vendor_name, vendor_category, year, month
),

project_cost_trend AS (
    SELECT
        project_key,
        project_id,
        project_name,
        project_type,
        year,
        month,
        SUM(actual_cost) AS monthly_actual,
        SUM(planned_cost) AS monthly_planned,
        SUM(cost_variance) AS monthly_variance
    FROM cost_detail
    GROUP BY project_key, project_id, project_name, project_type, year, month
),

cost_summary AS (
    SELECT
        SUM(actual_cost) AS total_actual_cost,
        SUM(planned_cost) AS total_planned_cost,
        SUM(cost_variance) AS total_cost_variance
    FROM cost_detail
)

SELECT
    CURRENT_DATE AS snapshot_date,
    (SELECT total_actual_cost FROM cost_summary) AS total_actual_cost,
    (SELECT total_planned_cost FROM cost_summary) AS total_planned_cost,
    (SELECT total_cost_variance FROM cost_summary) AS total_cost_variance,
    'vendor' AS dimension_type,
    vs.vendor_key AS dimension_key,
    vs.vendor_name AS dimension_name,
    vs.vendor_category AS dimension_category,
    vs.year,
    vs.month,
    vs.monthly_spend AS fact_value,
    vs.monthly_planned,
    vs.project_count
FROM vendor_spend vs

UNION ALL

SELECT
    CURRENT_DATE,
    (SELECT total_actual_cost FROM cost_summary),
    (SELECT total_planned_cost FROM cost_summary),
    (SELECT total_cost_variance FROM cost_summary),
    'project',
    pct.project_key,
    pct.project_id,
    pct.project_type,
    pct.year,
    pct.month,
    pct.monthly_actual,
    pct.monthly_planned,
    NULL
FROM project_cost_trend pct
  );
  