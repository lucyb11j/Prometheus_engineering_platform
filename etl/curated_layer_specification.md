# Curated Layer Specification
## Engineering Infrastructure Analytics Platform (EIAP)

**Document Version:** 1.0  
**Status:** Approved  
**Owner:** Analytics Engineering Team  
**Layer:** Curated  
**Architecture:** Enterprise Data Warehouse Star Schema

---

# 1. Purpose

The Curated Layer is the analytical layer of the platform.

Its purpose is to transform validated business data from the Trusted Layer into a dimensional model optimized for:

- Business Intelligence
- Executive Dashboards
- KPI Monitoring
- Data Science
- Machine Learning
- Forecasting
- Self-Service Analytics

---

# 2. Layer Position

```text
Source Systems
      ↓
RAW
      ↓
TRUSTED
      ↓
CURATED
      ↓
DBT Marts
      ↓
Power BI
      ↓
Machine Learning
```

---

# 3. Design Principles

The Curated Layer follows:

- Kimball Methodology
- Star Schema Modeling
- Surrogate Keys
- Slowly Changing Dimensions Type 2
- Business-Oriented Metrics
- Historical Traceability

---

# 4. Curated Schema

```sql
curated
```

---

# 5. Star Schema Overview

```text
                    dim_date
                        |
                        |
dim_location --- fact_cost ---- dim_project
                        |
                        |
                  dim_vendor


                    dim_date
                        |
                        |
dim_project --- fact_schedule
                        |
                        |
                  dim_location


                    dim_date
                        |
                        |
dim_equipment --- fact_maintenance
                        |
                        |
                  dim_project


                    dim_date
                        |
                        |
dim_employee --- fact_workforce
                        |
                        |
                  dim_project


                    dim_date
                        |
                        |
dim_risk ----- fact_risk
                        |
                        |
                  dim_project
```

---

# 6. Dimension Tables

---

# 6.1 DIM_DATE

## Purpose

Calendar dimension.

---

## Source

```text
Generated
```

---

## Table

```sql
curated.dim_date
```

---

## Primary Key

```text
date_key
```

---

## Columns

| Column | Type |
|----------|----------|
| date_key | INTEGER |
| full_date | DATE |
| year | SMALLINT |
| quarter | SMALLINT |
| month | SMALLINT |
| month_name | VARCHAR |
| week | SMALLINT |
| day | SMALLINT |
| day_name | VARCHAR |

---

## Cardinality

```text
4 years (2024-2027)

≈ 1461 rows
```

---

# 6.2 DIM_PROJECT

## Source

```text
trusted.project
```

---

## Table

```sql
curated.dim_project
```

---

## Grain

```text
One row per project
```

---

## Primary Key

```text
project_key
```

---

## Business Key

```text
project_id
```

---

## Columns

| Column |
|----------|
| project_key |
| project_id |
| project_name |
| project_type |
| location_key |
| status |
| start_date |
| planned_end_date |

---

## SCD Type

```text
Type 2
```

---

## Additional Columns

| Column |
|----------|
| effective_date |
| expiration_date |
| is_current |

---

# 6.3 DIM_LOCATION

## Source

```text
trusted.location
```

---

## Grain

```text
One row per location
```

---

## Columns

| Column |
|----------|
| location_key |
| location_id |
| country |
| region |
| city |
| site_name |

---

# 6.4 DIM_VENDOR

## Source

```text
trusted.vendor
```

---

## Grain

```text
One row per vendor
```

---

## Columns

| Column |
|----------|
| vendor_key |
| vendor_id |
| vendor_name |
| category |
| country |

---

# 6.5 DIM_EMPLOYEE

## Source

```text
trusted.employee
```

---

## Grain

```text
One row per employee
```

---

## Columns

| Column |
|----------|
| employee_key |
| employee_id |
| full_name |
| department |
| role |
| hire_date |

---

# 6.6 DIM_EQUIPMENT

## Source

```text
trusted.equipment
```

---

## Grain

```text
One row per equipment
```

---

## Columns

| Column |
|----------|
| equipment_key |
| equipment_id |
| equipment_name |
| equipment_type |
| status |
| manufacturer |
| purchase_date |

---

# 6.7 DIM_RISK

## Source

```text
trusted.risk
```

---

## Grain

```text
One row per risk
```

---

## Columns

| Column |
|----------|
| risk_key |
| risk_id |
| risk_category |
| severity |
| probability |
| risk_score |

---

# 7. Fact Tables

---

# 7.1 FACT_COST

## Purpose

Store project cost transactions.

---

## Source

```text
trusted.cost
```

---

## Table

```sql
curated.fact_cost
```

---

## Grain

```text
One cost transaction
per

Project
+
Vendor
+
Date
```

---

## Foreign Keys

| Column |
|----------|
| date_key |
| project_key |
| risk_key |

---

## Measures

| Measure |
|----------|
| probability |
| severity |
| impact_cost |
| impact_days |
| risk_score |

---

## KPI

### Risk Score

:contentReference[oaicite:4]{index=4}

---

# 8. Surrogate Key Strategy

All dimensions use surrogate keys.

Example:

```text
project_key
```

instead of:

```text
project_id
```

Advantages:

- Historical tracking
- SCD support
- Faster joins
- Stable relationships

---

# 9. Slowly Changing Dimensions

Supported:

```text
SCD Type 2
```

Tracked Dimensions:

```text
dim_project

dim_employee

dim_equipment
```

---

## History Columns

| Column |
|----------|
| effective_date |
| expiration_date |
| is_current |

---

# 10. Aggregation Strategy

Daily:

```text
fact_cost

fact_schedule

fact_maintenance

fact_workforce

fact_risk
```

---

Monthly Aggregates:

```text
project_cost_summary

project_schedule_summary

maintenance_summary

risk_summary
```

---

# 11. Data Quality Requirements

Minimum thresholds:

| KPI | Threshold |
|----------|----------|
| Completeness | 98% |
| Accuracy | 95% |
| Consistency | 95% |
| Referential Integrity | 100% |

---

# 12. Curated Layer Deliverables

Expected Tables:

```text
curated.dim_date
curated.dim_project
curated.dim_location
curated.dim_vendor
curated.dim_employee
curated.dim_equipment
curated.dim_risk

curated.fact_cost
curated.fact_schedule
curated.fact_maintenance
curated.fact_workforce
curated.fact_risk
```

---

# 13. Consumption Layer

Consumers:

```text
Power BI

Apache Superset

Metabase

dbt Marts

Machine Learning Pipelines

Executive Dashboards
```

---

# 14. Future Expansion

Future Dimensions:

```text
dim_contract

dim_material

dim_weather

dim_safety_incident
```

Future Facts:

```text
fact_contract

fact_material_consumption

fact_weather_impact

fact_safety
```

---

# End of Document