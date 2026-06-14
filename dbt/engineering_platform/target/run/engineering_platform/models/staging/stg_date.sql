
  create view "analytics_db"."curated"."stg_date__dbt_tmp"
    
    
  as (
    SELECT
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    week,
    day,
    day_name
FROM "analytics_db"."curated"."dim_date"
  );