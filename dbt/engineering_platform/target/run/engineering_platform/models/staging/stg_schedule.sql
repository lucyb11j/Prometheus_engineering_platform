
  create view "analytics_db"."curated"."stg_schedule__dbt_tmp"
    
    
  as (
    SELECT
    date_key,
    project_key,
    planned_progress,
    actual_progress,
    schedule_variance,
    spi
FROM "analytics_db"."curated"."fact_schedule"
  );