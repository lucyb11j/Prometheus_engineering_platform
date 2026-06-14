
  
    

  create  table "analytics_db"."curated"."mart_executive_dashboard__dbt_tmp"
  
  
    as
  
  (
    

WITH project_summary AS (
    SELECT
        COUNT(DISTINCT dp.project_id) AS total_projects,
        COUNT(DISTINCT CASE WHEN dp.status = 'Active' THEN dp.project_id END) AS active_projects,
        COUNT(DISTINCT CASE WHEN dp.status = 'Completed' THEN dp.project_id END) AS completed_projects,
        SUM(dp.budget) AS total_budget
    FROM "analytics_db"."curated"."stg_project" dp
),

cost_summary AS (
    SELECT
        SUM(fc.actual_cost) AS total_actual_cost,
        SUM(fc.planned_cost) AS total_planned_cost,
        SUM(fc.cost_variance) AS total_cost_variance
    FROM "analytics_db"."curated"."stg_cost" fc
    INNER JOIN "analytics_db"."curated"."stg_project" dp ON fc.project_key = dp.project_key
),

schedule_summary AS (
    SELECT
        AVG(fs.spi) AS avg_spi,
        SUM(fs.schedule_variance) AS total_schedule_variance
    FROM "analytics_db"."curated"."stg_schedule" fs
    INNER JOIN "analytics_db"."curated"."stg_project" dp ON fs.project_key = dp.project_key
),

risk_summary AS (
    SELECT
        COUNT(DISTINCT fr.project_key) AS projects_with_risks,
        AVG(fr.risk_score) AS avg_risk_score,
        COUNT(CASE WHEN fr.risk_score >= 7 THEN 1 END) AS high_risk_count
    FROM "analytics_db"."curated"."stg_risk_fact" fr
),

workforce_summary AS (
    SELECT
        COUNT(DISTINCT fw.employee_key) AS total_employees,
        SUM(fw.hours_worked) AS total_hours,
        AVG(fw.productivity_score) AS avg_productivity
    FROM "analytics_db"."curated"."stg_workforce" fw
)

SELECT
    CURRENT_DATE AS snapshot_date,
    ps.*,
    cs.total_actual_cost,
    cs.total_planned_cost,
    cs.total_cost_variance,
    ss.avg_spi,
    ss.total_schedule_variance,
    rs.projects_with_risks,
    rs.avg_risk_score,
    rs.high_risk_count,
    ws.total_employees,
    ws.total_hours,
    ws.avg_productivity,
    CASE WHEN cs.total_planned_cost > 0
        THEN (cs.total_planned_cost - cs.total_actual_cost) / cs.total_planned_cost * 100
        ELSE NULL
    END AS budget_health_pct
FROM project_summary ps
CROSS JOIN cost_summary cs
CROSS JOIN schedule_summary ss
CROSS JOIN risk_summary rs
CROSS JOIN workforce_summary ws
  );
  