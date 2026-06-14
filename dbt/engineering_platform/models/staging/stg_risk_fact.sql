SELECT
    date_key,
    project_key,
    risk_key,
    probability,
    severity_score,
    impact_cost,
    impact_days,
    risk_score
FROM {{ source('curated', 'fact_risk') }}
