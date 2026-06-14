
  
    

  create  table "analytics_db"."curated"."mart_risk_monitoring__dbt_tmp"
  
  
    as
  
  (
    

WITH risk_detail AS (
    SELECT
        fr.date_key,
        dd.year,
        dd.month,
        dd.full_date,
        fr.project_key,
        dp.project_id,
        dp.project_name,
        dp.project_type,
        dp.status AS project_status,
        fr.risk_key,
        dr.risk_id,
        dr.risk_name,
        dr.risk_category,
        fr.probability,
        fr.severity_score,
        fr.impact_cost,
        fr.impact_days,
        fr.risk_score,
        CASE
            WHEN fr.risk_score >= 7 THEN 'Critical'
            WHEN fr.risk_score >= 4 THEN 'High'
            WHEN fr.risk_score >= 2 THEN 'Medium'
            ELSE 'Low'
        END AS risk_level
    FROM "analytics_db"."curated"."stg_risk_fact" fr
    INNER JOIN "analytics_db"."curated"."stg_date" dd ON fr.date_key = dd.date_key
    INNER JOIN "analytics_db"."curated"."stg_project" dp ON fr.project_key = dp.project_key
    INNER JOIN "analytics_db"."curated"."stg_risk" dr ON fr.risk_key = dr.risk_key
),

project_risk_profile AS (
    SELECT
        project_key,
        project_id,
        project_name,
        project_type,
        project_status,
        COUNT(*) AS total_risks,
        SUM(CASE WHEN risk_level = 'Critical' THEN 1 ELSE 0 END) AS critical_risks,
        SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) AS high_risks,
        SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END) AS medium_risks,
        SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) AS low_risks,
        AVG(risk_score) AS avg_risk_score,
        MAX(risk_score) AS max_risk_score,
        SUM(impact_cost) AS total_impact_cost,
        SUM(impact_days) AS total_impact_days
    FROM risk_detail
    GROUP BY project_key, project_id, project_name, project_type, project_status
),

category_risk_summary AS (
    SELECT
        risk_category,
        COUNT(*) AS risk_count,
        AVG(risk_score) AS avg_risk_score,
        AVG(probability) AS avg_probability,
        AVG(severity_score) AS avg_severity,
        SUM(impact_cost) AS total_impact_cost
    FROM risk_detail
    GROUP BY risk_category
),

risk_trend AS (
    SELECT
        year,
        month,
        full_date,
        COUNT(*) AS risk_count,
        AVG(risk_score) AS avg_risk_score,
        SUM(impact_cost) AS total_impact_cost
    FROM risk_detail
    GROUP BY year, month, full_date
)

SELECT
    'project' AS dimension_type,
    prp.project_key AS dimension_key,
    prp.project_id AS dimension_id,
    prp.project_name AS dimension_name,
    prp.project_type AS dimension_category,
    prp.project_status,
    prp.total_risks,
    prp.critical_risks,
    prp.high_risks,
    prp.medium_risks,
    prp.low_risks,
    prp.avg_risk_score,
    prp.max_risk_score,
    prp.total_impact_cost,
    prp.total_impact_days,
    NULL AS risk_category,
    NULL::smallint AS year,
    NULL::smallint AS month
FROM project_risk_profile prp

UNION ALL

SELECT
    'category' AS dimension_type,
    NULL AS dimension_key,
    NULL AS dimension_id,
    crs.risk_category AS dimension_name,
    NULL AS dimension_category,
    NULL AS project_status,
    crs.risk_count AS total_risks,
    NULL AS critical_risks,
    NULL AS high_risks,
    NULL AS medium_risks,
    NULL AS low_risks,
    crs.avg_risk_score,
    NULL AS max_risk_score,
    crs.total_impact_cost,
    NULL AS total_impact_days,
    crs.risk_category,
    NULL::smallint AS year,
    NULL::smallint AS month
FROM category_risk_summary crs

UNION ALL

SELECT
    'trend' AS dimension_type,
    NULL AS dimension_key,
    NULL AS dimension_id,
    NULL AS dimension_name,
    NULL AS dimension_category,
    NULL AS project_status,
    rt.risk_count AS total_risks,
    NULL AS critical_risks,
    NULL AS high_risks,
    NULL AS medium_risks,
    NULL AS low_risks,
    rt.avg_risk_score,
    NULL AS max_risk_score,
    rt.total_impact_cost,
    NULL AS total_impact_days,
    NULL AS risk_category,
    rt.year,
    rt.month
FROM risk_trend rt
  );
  