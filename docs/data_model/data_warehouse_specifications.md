# Data Warehouse Specification

## Prometheus Analytics Platform

**Version:** 1.0
**Status:** Approved for Development
**Owner:** Analytics Engineering Team

---

# 1. Purpose

This document defines the implementation standards, loading strategies, historical management policies, data quality controls, and analytical modeling rules governing the Prometheus Analytics Platform Data Warehouse.

This specification serves as the operational blueprint for:

* Data Engineers
* Analytics Engineers
* BI Developers
* Data Scientists
* Platform Administrators

---

# 2. Data Warehouse Architecture

The platform follows a Medallion Architecture.

```text
SOURCE SYSTEMS
      │
      ▼
RAW
      │
      ▼
TRUSTED
      │
      ▼
CURATED
      │
      ▼
CONSUMPTION
```

---

# 3. Layer Definitions

## 3.1 RAW Layer

Purpose:

Store source data exactly as received.

Characteristics:

* Immutable
* Append Only
* No transformations
* Full traceability

Schema:

```sql
raw
```

Retention:

```text
5 years
```

---

## 3.2 TRUSTED Layer

Purpose:

Store validated enterprise data.

Characteristics:

* Cleaned data
* Standardized values
* Duplicate removal
* Quality validated

Schema:

```sql
trusted
```

Retention:

```text
10 years
```

---

## 3.3 CURATED Layer

Purpose:

Serve analytics workloads.

Characteristics:

* Star Schema
* KPI Calculation
* Dashboard Consumption
* Machine Learning Features

Schema:

```sql
curated
```

Retention:

```text
Permanent
```

---

# 4. Historical Data Strategy

The platform supports historical preservation using Slowly Changing Dimensions (SCD).

---

## 4.1 SCD Type 1

Overwrite old values.

Used when history is not required.

Examples:

```text
Corrected spelling
Phone number updates
Data quality fixes
```

Applicable Dimensions:

```text
dim_vendor
dim_location
```

---

## 4.2 SCD Type 2

Preserve historical versions.

Additional fields:

```text
effective_date
expiration_date
is_current
```

Applicable Dimensions:

```text
dim_project
dim_employee
dim_equipment
```

Example:

| project_id | status  | effective_date |
| ---------- | ------- | -------------- |
| P001       | Active  | 2025-01-01     |
| P001       | Delayed | 2025-03-01     |

---

# 5. Loading Strategy

---

## Full Load

Used during:

```text
Initial deployment
Historical migrations
```

Frequency:

```text
On demand
```

---

## Incremental Load

Used during:

```text
Daily operations
```

Strategy:

```text
Insert new records

Update modified records

Preserve historical records
```

Method:

```sql
MERGE
UPSERT
INSERT ON CONFLICT
```

---

# 6. Data Refresh Frequency

| Dataset     | Frequency |
| ----------- | --------- |
| Projects    | Daily     |
| Costs       | Daily     |
| Schedule    | Daily     |
| Equipment   | Daily     |
| Maintenance | Hourly    |
| Workforce   | Daily     |
| Risk Events | Daily     |

---

# 7. Fact Table Granularity

---

## fact_cost

Granularity:

```text
One project cost transaction per day
```

---

## fact_schedule

Granularity:

```text
One project progress record per reporting date
```

---

## fact_maintenance

Granularity:

```text
One maintenance event
```

---

## fact_workforce

Granularity:

```text
One employee activity per day
```

---

## fact_risk

Granularity:

```text
One risk occurrence event
```

---

# 8. Partitioning Strategy

Large Fact Tables:

```text
fact_cost
fact_schedule
fact_maintenance
fact_workforce
fact_risk
```

Partition Key:

```text
date_key
```

Partition Type:

```sql
PARTITION BY RANGE(date_key)
```

Example:

```text
fact_cost_2025
fact_cost_2026
fact_cost_2027
```

---

# 9. Indexing Standards

---

## Dimension Tables

Indexes:

```text
Business Keys
Foreign Keys
```

Example:

```sql
CREATE INDEX idx_project_id
ON curated.dim_project(project_id);
```

---

## Fact Tables

Indexes:

```sql
date_key
project_key
equipment_key
employee_key
risk_key
```

---

# 10. Data Quality Framework

All datasets must pass validation before entering the Trusted Layer.

---

## Completeness Checks

Example:

```text
project_id cannot be null
```

---

## Uniqueness Checks

Example:

```text
project_id must be unique
```

---

## Valid Range Checks

Example:

```text
0 <= probability <= 1
```

---

## Referential Integrity

Example:

```text
project_key must exist in dim_project
```

---

# 11. Data Quality Rules

| Rule ID | Description                 |
| ------- | --------------------------- |
| DQ-001  | Project ID mandatory        |
| DQ-002  | Vendor ID mandatory         |
| DQ-003  | Cost values >= 0            |
| DQ-004  | Progress between 0 and 100  |
| DQ-005  | Downtime >= 0               |
| DQ-006  | Probability between 0 and 1 |
| DQ-007  | No duplicate business keys  |

---

# 12. KPI Layer

KPIs are generated exclusively from Curated Layer data.

---

## Financial KPIs

```text
Budget Variance

Cost Variance

Cost Performance Index (CPI)

Forecast Cost
```

---

## Project KPIs

```text
Schedule Variance

Schedule Performance Index (SPI)

Project Completion Forecast
```

---

## Equipment KPIs

```text
MTBF

MTTR

Equipment Availability

Equipment Utilization
```

---

## Workforce KPIs

```text
Productivity Score

Labor Utilization

Hours Worked
```

---

## Risk KPIs

```text
Risk Exposure Score

Expected Monetary Value

Risk Heat Map
```

---

# 13. dbt Modeling Standards

Model Layers:

```text
staging
intermediate
mart
```

Example:

```text
stg_projects

int_project_metrics

mart_project_performance
```

Naming Convention:

```text
stg_
int_
mart_
```

---

# 14. Audit Framework

Schema:

```sql
audit
```

Table:

```text
etl_execution_log
```

Stores:

* Execution time
* Pipeline status
* Processed rows
* Failed rows
* Error details

---

# 15. Machine Learning Readiness

The Curated Layer must expose:

Features:

```text
Cost trends

Equipment failures

Maintenance history

Schedule delays

Workforce productivity

Risk scores
```

Used by:

```text
Forecasting Models

Predictive Maintenance

Delay Prediction

Risk Prediction
```

---

# 16. Security Model

Role-Based Access Control (RBAC)

Roles:

```text
analytics_admin

data_engineer

analytics_engineer

data_analyst

executive_user
```

Principle:

```text
Least Privilege
```

---

# 17. Backup Strategy

Frequency:

```text
Daily Incremental

Weekly Full Backup
```

Retention:

```text
90 Days
```

Recovery Objective:

```text
RPO: 1 Hour

RTO: 4 Hours
```

---

# 18. Future Extensions

Future Dimensions:

```text
dim_material

dim_contract

dim_weather

dim_sensor

dim_customer
```

Future Facts:

```text
fact_quality

fact_safety

fact_environment

fact_energy

fact_iot_sensor
```

---

# End of Document
