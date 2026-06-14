
  create view "analytics_db"."curated"."stg_risk__dbt_tmp"
    
    
  as (
    SELECT
    risk_key,
    risk_id,
    risk_name,
    risk_category
FROM "analytics_db"."curated"."dim_risk"
  );