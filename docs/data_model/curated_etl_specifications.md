# Curated ETL Specification

## Engineering Infrastructure Analytics Platform (EIAP)

**Version:** 1.0
**Status:** Approved for Development
**Owner:** Analytics Engineering Team
**Layer:** Curated ETL

---

# 1. Purpose

This document defines the ETL processes responsible for loading the Curated Layer from the Trusted Layer.

The Curated Layer provides the analytical foundation for:

* Executive Dashboards
* Business Intelligence
* KPI Monitoring
* Forecasting
* Machine Learning
* Data Science

---

# 2. ETL Architecture

```text
TRUSTED
    ↓
Business Transformation
    ↓
Surrogate Key Generation
    ↓
Dimension Loading
    ↓
Fact Loading
    ↓
CURATED
```

---

# 3. Curated Loading Sequence

The ETL process must execute in the following order:

```text
STEP 1
Load Dimensions

STEP 2
Load Fact Tables

STEP 3
Run Validation Tests

STEP 4
Generate Audit Logs
```

---

# 4. Dimension Loading Strategy

Dimensions must always be loaded before fact tables.

---

# 4.1 DIM_DATE

Source:

Generated internally

Destination:

```sql
curated.dim_date
```

Loading Type:

```text
Full Load
```

Frequency:

```text
One Time
```

Range:

```text
2020-01-01

2035-12-31
```

---

# 4.2 DIM_PROJECT

Source:

```sql
trusted.project
```

Destination:

```sql
curated.dim_project
```

Loading Type:

```text
Incremental
```

SCD Strategy:

```text
Type 2
```

Business Key:

```text
project_id
```

Surrogate Key:

```text
project_key
```

Change Detection:

```text
project_name

status

budget

project_type
```

History Columns:

```text
effective_date

expiration_date

is_current
```

---

# 4.3 DIM_LOCATION

Source:

```sql
trusted.location
```

Destination:

```sql
curated.dim_location
```

Loading Type:

```text
Incremental
```

Business Key:

```text
location_id
```

Surrogate Key:

```text
location_key
```

---

# 4.4 DIM_VENDOR

Source:

```sql
trusted.vendor
```

Destination:

```sql
curated.dim_vendor
```

Loading Type:

```text
Incremental
```

Business Key:

```text
vendor_id
```

Surrogate Key:

```text
vendor_key
```

SCD:

```text
Type 2
```

Tracked Fields:

```text
vendor_name

category

country
```

---

# 4.5 DIM_EMPLOYEE

Source:

```sql
trusted.employee
```

Destination:

```sql
curated.dim_employee
```

Loading Type:

```text
Incremental
```

Business Key:

```text
employee_id
```

Surrogate Key:

```text
employee_key
```

SCD:

```text
Type 2
```

Tracked Fields:

```text
department

role

salary
```

---

# 4.6 DIM_EQUIPMENT

Source:

```sql
trusted.equipment
```

Destination:

```sql
curated.dim_equipment
```

Loading Type:

```text
Incremental
```

Business Key:

```text
equipment_id
```

Surrogate Key:

```text
equipment_key
```

SCD:

```text
Type 2
```

Tracked Fields:

```text
status

equipment_type

manufacturer
```

---

# 4.7 DIM_RISK

Source:

```sql
trusted.risk
```

Destination:

```sql
curated.dim_risk
```

Loading Type:

```text
Incremental
```

Business Key:

```text
risk_id
```

Surrogate Key:

```text
risk_key
```

---

# 5. Fact Loading Strategy

Fact tables are loaded after all dimensions have been updated.

---

# 5.1 FACT_COST

Source:

```sql
trusted.cost
```

Destination:

```sql
curated.fact_cost
```

Grain:

```text
One transaction

per

Project
+
Vendor
+
Date
```

Dimension Lookups:

```text
project_key

vendor_key

date_key
```

Measures:

```text
planned_cost

actual_cost

cost_variance

earned_value

cpi
```

Transformations:

```text
cost_variance = actual_cost - planned_cost

cpi = earned_value / actual_cost
```

---

# 5.2 FACT_SCHEDULE

Source:

```sql
trusted.schedule
```

Destination:

```sql
curated.fact_schedule
```

Grain:

```text
One project report
per reporting date
```

Dimension Lookups:

```text
project_key

date_key
```

Measures:

```text
planned_progress

actual_progress

schedule_variance

spi
```

Transformations:

```text
schedule_variance =
actual_progress - planned_progress

spi =
actual_progress / planned_progress
```

---

# 5.3 FACT_MAINTENANCE

Source:

```sql
trusted.maintenance
```

Destination:

```sql
curated.fact_maintenance
```

Dimension Lookups:

```text
equipment_key

project_key

date_key
```

Measures:

```text
downtime_hours

maintenance_cost

repair_duration_hours
```

---

# 5.4 FACT_WORKFORCE

Source:

```sql
trusted.employee_productivity
```

Destination:

```sql
curated.fact_workforce
```

Dimension Lookups:

```text
employee_key

project_key

date_key
```

Measures:

```text
hours_worked

overtime_hours

labor_cost

productivity_score
```

---

# 5.5 FACT_RISK

Source:

```sql
trusted.risk
```

Destination:

```sql
curated.fact_risk
```

Dimension Lookups:

```text
risk_key

project_key

date_key
```

Measures:

```text
probability

severity

impact_cost

impact_days

risk_score
```

Transformation:

```text
risk_score =
probability × severity
```

---

# 6. Surrogate Key Resolution

Before loading facts:

```text
project_id
→
project_key

vendor_id
→
vendor_key

employee_id
→
employee_key

equipment_id
→
equipment_key

risk_id
→
risk_key
```

Rules:

```text
No fact record may be loaded
without valid surrogate keys.
```

Invalid records:

```text
audit.rejected_records
```

---

# 7. Incremental Loading Strategy

Load Type:

```text
CDC Inspired Incremental Load
```

Method:

```text
Load only new or modified records
```

Detection Fields:

```text
created_at

updated_at

load_timestamp
```

---

# 8. Data Quality Validation

Before Curated Load:

```text
No Null Business Keys

No Duplicate Business Keys

Referential Integrity Valid

Numeric Fields Valid

Date Fields Valid
```

---

# 9. Audit Logging

Audit Table:

```sql
audit.etl_execution_log
```

Captured Metrics:

```text
Pipeline Name

Start Time

End Time

Rows Read

Rows Inserted

Rows Updated

Rows Rejected

Execution Status
```

---

# 10. Rejected Records

Destination:

```sql
audit.rejected_records
```

Columns:

```text
rejection_id

pipeline_name

source_table

record_identifier

rejection_reason

rejected_at
```

---

# 11. ETL Execution Order

```text
Load DIM_DATE

Load DIM_LOCATION

Load DIM_PROJECT

Load DIM_VENDOR

Load DIM_EMPLOYEE

Load DIM_EQUIPMENT

Load DIM_RISK

Load FACT_COST

Load FACT_SCHEDULE

Load FACT_MAINTENANCE

Load FACT_WORKFORCE

Load FACT_RISK
```

---

# 12. Expected Outputs

Dimensions:

```text
curated.dim_date
curated.dim_project
curated.dim_location
curated.dim_vendor
curated.dim_employee
curated.dim_equipment
curated.dim_risk
```

Facts:

```text
curated.fact_cost
curated.fact_schedule
curated.fact_maintenance
curated.fact_workforce
curated.fact_risk
```

---

# 13. Acceptance Criteria

The Curated Layer is considered complete when:

```text
All dimensions populated

All facts populated

Foreign Keys resolved

Data Quality > 95%

Audit Logs generated

Validation Tests passed
```

---

# 14. Future Enhancements

Future ETL Capabilities:

```text
Apache Airflow

dbt Incremental Models

Data Observability

Great Expectations

Real-Time Streaming

Kafka Integration
```

---

# End of Document
