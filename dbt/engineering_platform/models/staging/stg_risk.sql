SELECT
    risk_key,
    risk_id,
    risk_name,
    risk_category
FROM {{ source('curated', 'dim_risk') }}
