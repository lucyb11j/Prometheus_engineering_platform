
  create view "analytics_db"."curated"."stg_equipment__dbt_tmp"
    
    
  as (
    SELECT
    equipment_key,
    equipment_id,
    equipment_name,
    equipment_type,
    status AS equipment_status,
    manufacturer,
    effective_date,
    expiration_date,
    is_current
FROM "analytics_db"."curated"."dim_equipment"
WHERE is_current = TRUE
  );