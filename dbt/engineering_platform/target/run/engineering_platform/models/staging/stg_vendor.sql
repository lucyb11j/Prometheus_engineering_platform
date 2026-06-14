
  create view "analytics_db"."curated"."stg_vendor__dbt_tmp"
    
    
  as (
    SELECT
    vendor_key,
    vendor_id,
    vendor_name,
    category AS vendor_category,
    country
FROM "analytics_db"."curated"."dim_vendor"
  );