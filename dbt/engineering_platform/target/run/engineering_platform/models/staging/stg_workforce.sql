
  create view "analytics_db"."curated"."stg_workforce__dbt_tmp"
    
    
  as (
    SELECT
    date_key,
    employee_key,
    project_key,
    hours_worked,
    productivity_score
FROM "analytics_db"."curated"."fact_workforce"
  );