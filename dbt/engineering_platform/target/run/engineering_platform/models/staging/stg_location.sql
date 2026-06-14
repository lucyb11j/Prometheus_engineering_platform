
  create view "analytics_db"."curated"."stg_location__dbt_tmp"
    
    
  as (
    SELECT
    location_key,
    location_id,
    country,
    region,
    city,
    site_name
FROM "analytics_db"."curated"."dim_location"
  );