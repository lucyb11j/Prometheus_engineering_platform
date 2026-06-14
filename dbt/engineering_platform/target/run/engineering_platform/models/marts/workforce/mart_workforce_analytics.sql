
  
    

  create  table "analytics_db"."curated"."mart_workforce_analytics__dbt_tmp"
  
  
    as
  
  (
    

WITH workforce_detail AS (
    SELECT
        fw.date_key,
        dd.year,
        dd.month,
        dd.month_name,
        fw.employee_key,
        de.employee_id,
        de.full_name,
        de.department,
        de.role,
        de.salary,
        fw.project_key,
        dp.project_id,
        dp.project_name,
        dp.project_type,
        dp.status AS project_status,
        fw.hours_worked,
        fw.productivity_score
    FROM "analytics_db"."curated"."stg_workforce" fw
    INNER JOIN "analytics_db"."curated"."stg_date" dd ON fw.date_key = dd.date_key
    INNER JOIN "analytics_db"."curated"."stg_employee" de ON fw.employee_key = de.employee_key
    INNER JOIN "analytics_db"."curated"."stg_project" dp ON fw.project_key = dp.project_key
),

employee_summary AS (
    SELECT
        employee_key,
        employee_id,
        full_name,
        department,
        role,
        salary,
        COUNT(DISTINCT project_key) AS project_count,
        SUM(hours_worked) AS total_hours,
        AVG(hours_worked) AS avg_hours_per_period,
        AVG(productivity_score) AS avg_productivity,
        SUM(hours_worked) * AVG(productivity_score) AS weighted_productivity
    FROM workforce_detail
    GROUP BY employee_key, employee_id, full_name, department, role, salary
),

department_summary AS (
    SELECT
        department,
        COUNT(DISTINCT employee_key) AS employee_count,
        COUNT(DISTINCT project_key) AS project_count,
        SUM(hours_worked) AS total_hours,
        AVG(productivity_score) AS avg_productivity,
        AVG(salary) AS avg_salary
    FROM workforce_detail
    GROUP BY department
),

project_workforce AS (
    SELECT
        project_key,
        project_id,
        project_name,
        project_type,
        project_status,
        COUNT(DISTINCT employee_key) AS assigned_employees,
        SUM(hours_worked) AS total_hours,
        AVG(productivity_score) AS avg_productivity
    FROM workforce_detail
    GROUP BY project_key, project_id, project_name, project_type, project_status
),

monthly_workforce AS (
    SELECT
        year,
        month,
        month_name,
        COUNT(DISTINCT employee_key) AS active_employees,
        COUNT(DISTINCT project_key) AS active_projects,
        SUM(hours_worked) AS total_hours,
        AVG(productivity_score) AS avg_productivity
    FROM workforce_detail
    GROUP BY year, month, month_name
)

SELECT
    'employee' AS dimension_type,
    es.employee_key AS dimension_key,
    es.employee_id AS dimension_id,
    es.full_name AS dimension_name,
    es.department,
    es.role,
    es.salary,
    es.project_count,
    es.total_hours,
    es.avg_hours_per_period,
    es.avg_productivity,
    es.weighted_productivity,
    NULL::smallint AS year,
    NULL::smallint AS month,
    NULL AS month_name
FROM employee_summary es

UNION ALL

SELECT
    'department' AS dimension_type,
    NULL AS dimension_key,
    NULL AS dimension_id,
    ds.department AS dimension_name,
    ds.department,
    NULL AS role,
    ds.avg_salary AS salary,
    ds.project_count,
    ds.total_hours,
    NULL AS avg_hours_per_period,
    ds.avg_productivity,
    NULL AS weighted_productivity,
    NULL::smallint AS year,
    NULL::smallint AS month,
    NULL AS month_name
FROM department_summary ds

UNION ALL

SELECT
    'project' AS dimension_type,
    pw.project_key AS dimension_key,
    pw.project_id AS dimension_id,
    pw.project_name AS dimension_name,
    NULL AS department,
    NULL AS role,
    NULL AS salary,
    pw.assigned_employees AS project_count,
    pw.total_hours,
    NULL AS avg_hours_per_period,
    pw.avg_productivity,
    NULL AS weighted_productivity,
    NULL::smallint AS year,
    NULL::smallint AS month,
    NULL AS month_name
FROM project_workforce pw

UNION ALL

SELECT
    'monthly' AS dimension_type,
    NULL AS dimension_key,
    NULL AS dimension_id,
    NULL AS dimension_name,
    NULL AS department,
    NULL AS role,
    NULL AS salary,
    mw.active_projects AS project_count,
    mw.total_hours,
    NULL AS avg_hours_per_period,
    mw.avg_productivity,
    NULL AS weighted_productivity,
    mw.year,
    mw.month,
    mw.month_name
FROM monthly_workforce mw
  );
  