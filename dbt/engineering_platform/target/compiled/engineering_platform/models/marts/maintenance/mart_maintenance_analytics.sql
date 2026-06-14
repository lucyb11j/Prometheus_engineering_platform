

WITH maintenance_base AS (
    SELECT
        fm.date_key,
        dd.year,
        dd.month,
        dd.month_name,
        fm.equipment_key,
        de.equipment_id,
        de.equipment_name,
        de.equipment_type,
        de.equipment_status,
        fm.maintenance_type,
        fm.downtime_hours,
        fm.maintenance_cost,
        de.manufacturer
    FROM "analytics_db"."curated"."stg_maintenance" fm
    INNER JOIN "analytics_db"."curated"."stg_date" dd ON fm.date_key = dd.date_key
    INNER JOIN "analytics_db"."curated"."stg_equipment" de ON fm.equipment_key = de.equipment_key
),

equipment_summary AS (
    SELECT
        equipment_key,
        equipment_id,
        equipment_name,
        equipment_type,
        manufacturer,
        COUNT(*) AS maintenance_events,
        SUM(downtime_hours) AS total_downtime,
        AVG(downtime_hours) AS avg_downtime_per_event,
        SUM(maintenance_cost) AS total_maintenance_cost,
        AVG(maintenance_cost) AS avg_cost_per_event,
        SUM(CASE WHEN maintenance_type = 'Emergency' THEN 1 ELSE 0 END) AS emergency_count,
        SUM(CASE WHEN maintenance_type = 'Preventive' THEN 1 ELSE 0 END) AS preventive_count
    FROM maintenance_base
    GROUP BY equipment_key, equipment_id, equipment_name, equipment_type, manufacturer
),

monthly_trend AS (
    SELECT
        year,
        month,
        month_name,
        COUNT(*) AS event_count,
        SUM(downtime_hours) AS total_downtime_hours,
        SUM(maintenance_cost) AS total_cost,
        COUNT(DISTINCT equipment_key) AS equipment_affected
    FROM maintenance_base
    GROUP BY year, month, month_name
),

maintenance_type_summary AS (
    SELECT
        maintenance_type,
        COUNT(*) AS event_count,
        SUM(downtime_hours) AS total_downtime,
        SUM(maintenance_cost) AS total_cost,
        AVG(downtime_hours) AS avg_downtime,
        AVG(maintenance_cost) AS avg_cost
    FROM maintenance_base
    GROUP BY maintenance_type
)

SELECT
    'equipment' AS dimension_type,
    es.equipment_key AS dimension_key,
    es.equipment_id AS dimension_id,
    es.equipment_name AS dimension_name,
    es.equipment_type AS dimension_category,
    es.manufacturer,
    es.maintenance_events,
    es.total_downtime,
    es.avg_downtime_per_event,
    es.total_maintenance_cost,
    es.avg_cost_per_event,
    es.emergency_count,
    es.preventive_count,
    NULL AS year,
    NULL AS month,
    NULL AS month_name
FROM equipment_summary es

UNION ALL

SELECT
    'monthly' AS dimension_type,
    NULL AS dimension_key,
    NULL AS dimension_id,
    NULL AS dimension_name,
    NULL AS dimension_category,
    NULL AS manufacturer,
    mt.event_count AS maintenance_events,
    mt.total_downtime_hours AS total_downtime,
    NULL AS avg_downtime_per_event,
    mt.total_cost AS total_maintenance_cost,
    NULL AS avg_cost_per_event,
    NULL AS emergency_count,
    NULL AS preventive_count,
    mt.year,
    mt.month,
    mt.month_name
FROM monthly_trend mt

UNION ALL

SELECT
    'maintenance_type' AS dimension_type,
    NULL AS dimension_key,
    NULL AS dimension_id,
    mts.maintenance_type AS dimension_name,
    NULL AS dimension_category,
    NULL AS manufacturer,
    mts.event_count AS maintenance_events,
    mts.total_downtime AS total_downtime,
    mts.avg_downtime AS avg_downtime_per_event,
    mts.total_cost AS total_maintenance_cost,
    mts.avg_cost AS avg_cost_per_event,
    NULL AS emergency_count,
    NULL AS preventive_count,
    NULL AS year,
    NULL AS month,
    NULL AS month_name
FROM maintenance_type_summary mts