
  
    

  create  table "analytics_db"."curated"."mart_project_performance__dbt_tmp"
  
  
    as
  
  (
    

WITH project_base AS (
    SELECT
        dp.project_key,
        dp.project_id,
        dp.project_name,
        dp.project_type,
        dp.status,
        dp.budget,
        dl.city AS location_city,
        dl.country AS location_country
    FROM "analytics_db"."curated"."stg_project" dp
    LEFT JOIN "analytics_db"."curated"."stg_location" dl ON dp.location_key = dl.location_key
),

cost_agg AS (
    SELECT
        project_key,
        SUM(planned_cost) AS total_planned_cost,
        SUM(actual_cost) AS total_actual_cost,
        SUM(cost_variance) AS total_cost_variance,
        MAX(forecast_cost) AS latest_forecast_cost
    FROM "analytics_db"."curated"."stg_cost"
    GROUP BY project_key
),

schedule_agg AS (
    SELECT
        project_key,
        AVG(spi) AS avg_spi,
        MIN(spi) AS min_spi,
        SUM(schedule_variance) AS total_schedule_variance,
        MAX(actual_progress) AS latest_actual_progress,
        MAX(planned_progress) AS latest_planned_progress
    FROM "analytics_db"."curated"."stg_schedule"
    GROUP BY project_key
),

risk_agg AS (
    SELECT
        project_key,
        COUNT(*) AS risk_count,
        MAX(risk_score) AS max_risk_score,
        AVG(risk_score) AS avg_risk_score,
        SUM(impact_cost) AS total_risk_impact_cost
    FROM "analytics_db"."curated"."stg_risk_fact"
    GROUP BY project_key
),

workforce_agg AS (
    SELECT
        project_key,
        COUNT(DISTINCT employee_key) AS employee_count,
        SUM(hours_worked) AS total_hours_worked,
        AVG(productivity_score) AS avg_productivity
    FROM "analytics_db"."curated"."stg_workforce"
    GROUP BY project_key
)

SELECT
    pb.*,
    COALESCE(ca.total_planned_cost, 0) AS total_planned_cost,
    COALESCE(ca.total_actual_cost, 0) AS total_actual_cost,
    COALESCE(ca.total_cost_variance, 0) AS total_cost_variance,
    ca.latest_forecast_cost,
    COALESCE(sa.avg_spi, 1) AS avg_spi,
    COALESCE(sa.min_spi, 1) AS min_spi,
    COALESCE(sa.total_schedule_variance, 0) AS total_schedule_variance,
    sa.latest_actual_progress,
    sa.latest_planned_progress,
    COALESCE(ra.risk_count, 0) AS risk_count,
    ra.max_risk_score,
    ra.avg_risk_score,
    COALESCE(ra.total_risk_impact_cost, 0) AS total_risk_impact_cost,
    COALESCE(wa.employee_count, 0) AS employee_count,
    COALESCE(wa.total_hours_worked, 0) AS total_hours_worked,
    wa.avg_productivity,
    CASE WHEN pb.budget > 0
        THEN (pb.budget - COALESCE(ca.total_actual_cost, 0)) / pb.budget * 100
        ELSE NULL
    END AS budget_remaining_pct,
    CASE WHEN ca.total_planned_cost > 0
        THEN (ca.total_actual_cost / ca.total_planned_cost) * 100
        ELSE NULL
    END AS cost_overrun_pct
FROM project_base pb
LEFT JOIN cost_agg ca ON pb.project_key = ca.project_key
LEFT JOIN schedule_agg sa ON pb.project_key = sa.project_key
LEFT JOIN risk_agg ra ON pb.project_key = ra.project_key
LEFT JOIN workforce_agg wa ON pb.project_key = wa.project_key
  );
  