# Curated Validation Plan

## Engineering Infrastructure Analytics Platform (EIAP)

**Version:** 1.0
**Status:** Approved
**Owner:** Analytics Engineering Team
**Environment:** PostgreSQL Data Warehouse
**Layer:** Curated

---

# 1. Purpose

This document defines the validation strategy for the Curated Layer.

The purpose is to ensure:

* Data completeness
* Data accuracy
* Referential integrity
* Business rule compliance
* SCD Type 2 functionality
* KPI calculation correctness
* Readiness for Analytics and Reporting

---

# 2. Validation Scope

The following objects are included:

## Dimensions

```text
curated.dim_date

curated.dim_project

curated.dim_location

curated.dim_vendor

curated.dim_employee

curated.dim_equipment

curated.dim_risk
```

---

## Fact Tables

```text
curated.fact_cost

curated.fact_schedule

curated.fact_maintenance

curated.fact_workforce

curated.fact_risk
```

---

# 3. Validation Categories

The validation framework includes:

```text
Structure Validation

Data Quality Validation

Referential Integrity Validation

Business Rule Validation
```
# 4. Dimension Validation

---

# 4.1 DIM_DATE Validation

Table:

```sql
curated.dim_date
```

Validation Objectives:

* Verify date range completeness
* Verify surrogate key uniqueness
* Verify calendar attributes consistency

---

## DV-DATE-001

Validate row count.

Expected:

```text
2020-01-01
through
2035-12-31
```

SQL:

```sql
SELECT COUNT(*)
FROM curated.dim_date;
```

Expected Result:

```text
>= 5844 rows
```

---

## DV-DATE-002

Validate unique date_key.

SQL:

```sql
SELECT date_key,
       COUNT(*)
FROM curated.dim_date
GROUP BY date_key
HAVING COUNT(*) > 1;
```

Expected:

```text
0 rows
```

---

## DV-DATE-003

Validate date uniqueness.

SQL:

```sql
SELECT full_date,
       COUNT(*)
FROM curated.dim_date
GROUP BY full_date
HAVING COUNT(*) > 1;
```

Expected:

```text
0 rows
```

---

# 4.2 DIM_PROJECT Validation

Table:

```sql
curated.dim_project
```

---

## DV-PROJ-001

Validate surrogate key uniqueness.

SQL:

```sql
SELECT project_key,
       COUNT(*)
FROM curated.dim_project
GROUP BY project_key
HAVING COUNT(*) > 1;
```

Expected:

```text
0 rows
```

---

## DV-PROJ-002

Validate business key existence.

SQL:

```sql
SELECT *
FROM curated.dim_project
WHERE project_id IS NULL;
```

Expected:

```text
0 rows
```

---

## DV-PROJ-003

Validate SCD current record.

SQL:

```sql
SELECT project_id
FROM curated.dim_project
WHERE is_current = TRUE
GROUP BY project_id
HAVING COUNT(*) > 1;
```

Expected:

```text
0 rows
```

---

## DV-PROJ-004

Validate budget.

SQL:

```sql
SELECT *
FROM curated.dim_project
WHERE budget <= 0;
```

Expected:

```text
0 rows
```

---

# 4.3 DIM_VENDOR Validation

Table:

```sql
curated.dim_vendor
```

Validation Rules:

```text
Unique surrogate keys

Non-null vendor_id

Valid category

SCD Type 2 integrity
```

SQL:

```sql
SELECT *
FROM curated.dim_vendor
WHERE vendor_id IS NULL;
```

Expected:

```text
0 rows
```

---

# 4.4 DIM_EMPLOYEE Validation

Table:

```sql
curated.dim_employee
```

---

## DV-EMP-001

SQL:

```sql
SELECT *
FROM curated.dim_employee
WHERE employee_id IS NULL;
```

Expected:

```text
0 rows
```

---

## DV-EMP-002

SQL:

```sql
SELECT *
FROM curated.dim_employee
WHERE salary <= 0;
```

Expected:

```text
0 rows
```

---

# 4.5 DIM_EQUIPMENT Validation

Table:

```sql
curated.dim_equipment
```

Validation:

```text
equipment_id not null

purchase_date valid

status valid
```

SQL:

```sql
SELECT *
FROM curated.dim_equipment
WHERE equipment_id IS NULL;
```

Expected:

```text
0 rows
```

---

# 4.6 DIM_LOCATION Validation

Table:

```sql
curated.dim_location
```

Validation:

```text
location_id not null

country populated

city populated
```

SQL:

```sql
SELECT *
FROM curated.dim_location
WHERE location_id IS NULL;
```

Expected:

```text
0 rows
```

---

# 4.7 DIM_RISK Validation

Table:

```sql
curated.dim_risk
```

Validation:

```text
risk_score >= 0

severity between 1 and 10
```

SQL:

```sql
SELECT *
FROM curated.dim_risk
WHERE severity NOT BETWEEN 1 AND 10;
```

Expected:

```text
0 rows
```

---

# 5. Fact Table Validation

---

# 5.1 FACT_COST Validation

Table:

```sql
curated.fact_cost
```

---

## FV-COST-001

Validate measures.

SQL:

```sql
SELECT *
FROM curated.fact_cost
WHERE planned_cost < 0;
```

Expected:

```text
0 rows
```

---

## FV-COST-002

Validate variance calculation.

SQL:

```sql
SELECT *
FROM curated.fact_cost
WHERE cost_variance <>
      actual_cost - planned_cost;
```

Expected:

```text
0 rows
```

---

## FV-COST-003

Validate CPI.

SQL:

```sql
SELECT *
FROM curated.fact_cost
WHERE cpi < 0;
```

Expected:

```text
0 rows
```

---

# 5.2 FACT_SCHEDULE Validation

Table:

```sql
curated.fact_schedule
```

Validation:

```text
planned_progress

actual_progress

schedule_variance

spi
```

SQL:

```sql
SELECT *
FROM curated.fact_schedule
WHERE planned_progress NOT BETWEEN 0 AND 100;
```

Expected:

```text
0 rows
```

---

# 5.3 FACT_MAINTENANCE Validation

SQL:

```sql
SELECT *
FROM curated.fact_maintenance
WHERE downtime_hours < 0;
```

Expected:

```text
0 rows
```

---

# 5.4 FACT_WORKFORCE Validation

SQL:

```sql
SELECT *
FROM curated.fact_workforce
WHERE hours_worked < 0;
```

Expected:

```text
0 rows
```

---

# 5.5 FACT_RISK Validation

SQL:

```sql
SELECT *
FROM curated.fact_risk
WHERE risk_score < 0;
```

Expected:

```text
0 rows
```

# 6. Referential Integrity Validation

---

# Objective

Ensure all fact tables reference valid dimension records.

No orphan records are allowed.

---

# RI-001 FACT_COST → DIM_PROJECT

SQL:

```sql
SELECT COUNT(*)
FROM curated.fact_cost f
LEFT JOIN curated.dim_project d
ON f.project_key = d.project_key
WHERE d.project_key IS NULL;
```

Expected:

```text
0
```

---

# RI-002 FACT_COST → DIM_VENDOR

SQL:

```sql
SELECT COUNT(*)
FROM curated.fact_cost f
LEFT JOIN curated.dim_vendor d
ON f.vendor_key = d.vendor_key
WHERE d.vendor_key IS NULL;
```

Expected:

```text
0
```

---

# RI-003 FACT_SCHEDULE → DIM_PROJECT

SQL:

```sql
SELECT COUNT(*)
FROM curated.fact_schedule f
LEFT JOIN curated.dim_project d
ON f.project_key = d.project_key
WHERE d.project_key IS NULL;
```

Expected:

```text
0
```

---

# RI-004 FACT_MAINTENANCE → DIM_EQUIPMENT

SQL:

```sql
SELECT COUNT(*)
FROM curated.fact_maintenance f
LEFT JOIN curated.dim_equipment d
ON f.equipment_key = d.equipment_key
WHERE d.equipment_key IS NULL;
```

Expected:

```text
0
```

---

# RI-005 FACT_WORKFORCE → DIM_EMPLOYEE

SQL:

```sql
SELECT COUNT(*)
FROM curated.fact_workforce f
LEFT JOIN curated.dim_employee d
ON f.employee_key = d.employee_key
WHERE d.employee_key IS NULL;
```

Expected:

```text
0
```

---

# RI-006 FACT_RISK → DIM_RISK

SQL:

```sql
SELECT COUNT(*)
FROM curated.fact_risk f
LEFT JOIN curated.dim_risk d
ON f.risk_key = d.risk_key
WHERE d.risk_key IS NULL;
```

Expected:

```text
0
```

---

# 7. SCD Type 2 Validation

---

# Objective

Verify historical tracking works correctly.

Applicable Dimensions:

```text
dim_project

dim_vendor

dim_employee

dim_equipment
```

---

# SCD-001

Validate single current record.

SQL:

```sql
SELECT project_id
FROM curated.dim_project
WHERE is_current = TRUE
GROUP BY project_id
HAVING COUNT(*) > 1;
```

Expected:

```text
0 rows
```

---

# SCD-002

Validate historical versioning.

SQL:

```sql
SELECT project_id,
       COUNT(*)
FROM curated.dim_project
GROUP BY project_id
HAVING COUNT(*) > 1;
```

Expected:

```text
Historical records may exist
```

---

# SCD-003

Validate expiration dates.

SQL:

```sql
SELECT *
FROM curated.dim_project
WHERE is_current = FALSE
AND expiration_date IS NULL;
```

Expected:

```text
0 rows
```

---

# SCD-004

Validate current rows.

SQL:

```sql
SELECT *
FROM curated.dim_project
WHERE is_current = TRUE
AND expiration_date IS NOT NULL;
```

Expected:

```text
0 rows
```

---

# 8. KPI Validation

---

# KPI-001 Cost Variance

Rule:

```text
cost_variance =
actual_cost - planned_cost
```

SQL:

```sql
SELECT *
FROM curated.fact_cost
WHERE cost_variance <>
(actual_cost - planned_cost);
```

Expected:

```text
0 rows
```

---

# KPI-002 CPI

Rule:

```text
CPI = earned_value / actual_cost
```

SQL:

```sql
SELECT *
FROM curated.fact_cost
WHERE cpi < 0;
```

Expected:

```text
0 rows
```

---

# KPI-003 Schedule Variance

Rule:

```text
schedule_variance =
actual_progress - planned_progress
```

SQL:

```sql
SELECT *
FROM curated.fact_schedule
WHERE schedule_variance <>
(actual_progress - planned_progress);
```

Expected:

```text
0 rows
```

---

# KPI-004 SPI

Rule:

```text
SPI > 0
```

SQL:

```sql
SELECT *
FROM curated.fact_schedule
WHERE spi < 0;
```

Expected:

```text
0 rows
```

---

# KPI-005 Risk Score

Rule:

```text
risk_score =
probability × severity
```

SQL:

```sql
SELECT *
FROM curated.fact_risk
WHERE risk_score <>
(probability * severity);
```

Expected:

```text
0 rows
```

---

# 9. Data Quality Validation

---

# DQ-001 Completeness

SQL:

```sql
SELECT
COUNT(*) AS total_rows,
COUNT(project_id) AS populated_rows
FROM curated.dim_project;
```

Target:

```text
≥ 98%
```

---

# DQ-002 Duplicate Rate

SQL:

```sql
SELECT project_id,
COUNT(*)
FROM curated.dim_project
GROUP BY project_id
HAVING COUNT(*) > 1;
```

Expected:

```text
Only valid SCD history
```

---

# DQ-003 Accuracy

Validation:

```text
Business Rules
must match specification
```

Target:

```text
95%
```

---

# DQ-004 Referential Integrity

Target:

```text
100%
```

---

# DQ-005 Freshness

Validation:

```sql
SELECT MAX(load_timestamp)
FROM curated.fact_cost;
```

Target:

```text
Within SLA
```

# 10. ETL Validation

---

# ETL-001 Pipeline Execution

Objective:

Verify successful execution of all ETL stages.

Expected Flow:

```text
RAW
 ↓
TRUSTED
 ↓
CURATED
```

Validation:

```text
No ETL Failures

No Unhandled Exceptions

Execution Completed Successfully
```

---

# ETL-002 Record Processing

Validate:

```text
Rows Read

Rows Inserted

Rows Updated

Rows Rejected
```

SQL:

```sql
SELECT *
FROM audit.etl_execution_log
ORDER BY execution_start DESC;
```

Expected:

```text
Execution Status = SUCCESS
```

---

# ETL-003 Rejected Records

SQL:

```sql
SELECT *
FROM audit.rejected_records
ORDER BY rejected_at DESC;
```

Validation:

```text
All rejected records have reason codes
```

---

# 11. Row Count Validation

---

# RC-001 Trusted vs Curated Dimensions

Example:

```sql
SELECT COUNT(*)
FROM trusted.project;
```

Compare Against:

```sql
SELECT COUNT(*)
FROM curated.dim_project
WHERE is_current = TRUE;
```

Tolerance:

```text
± 0%
```

---

# RC-002 Trusted Cost vs Fact Cost

SQL:

```sql
SELECT COUNT(*)
FROM trusted.cost;
```

Compare Against:

```sql
SELECT COUNT(*)
FROM curated.fact_cost;
```

Tolerance:

```text
± 0%
```

---

# RC-003 Trusted Schedule vs Fact Schedule

SQL:

```sql
SELECT COUNT(*)
FROM trusted.schedule;
```

Compare Against:

```sql
SELECT COUNT(*)
FROM curated.fact_schedule;
```

Tolerance:

```text
± 0%
```

---

# 12. Reconciliation Validation

---

# RECON-001 Financial Totals

Trusted:

```sql
SELECT SUM(actual_cost)
FROM trusted.cost;
```

Curated:

```sql
SELECT SUM(actual_cost)
FROM curated.fact_cost;
```

Expected:

```text
Values must match
```

---

# RECON-002 Planned Cost Totals

Trusted:

```sql
SELECT SUM(planned_cost)
FROM trusted.cost;
```

Curated:

```sql
SELECT SUM(planned_cost)
FROM curated.fact_cost;
```

Expected:

```text
Values must match
```

---

# RECON-003 Maintenance Cost Totals

Trusted:

```sql
SELECT SUM(maintenance_cost)
FROM trusted.maintenance;
```

Curated:

```sql
SELECT SUM(maintenance_cost)
FROM curated.fact_maintenance;
```

Expected:

```text
Values must match
```

---

# 13. Audit Validation

---

# AUDIT-001 ETL Log Completeness

SQL:

```sql
SELECT *
FROM audit.etl_execution_log;
```

Validation:

```text
Pipeline Name populated

Start Time populated

End Time populated

Status populated
```

---

# AUDIT-002 Duration Validation

SQL:

```sql
SELECT
execution_end -
execution_start
AS duration
FROM audit.etl_execution_log;
```

Expected:

```text
Positive duration
```

---

# AUDIT-003 Load Statistics

Validation:

```text
Rows Read > 0

Rows Inserted >= 0

Rows Rejected >= 0
```

---

# 14. Performance Validation

---

# PERF-001 Dimension Query

SQL:

```sql
SELECT *
FROM curated.dim_project
LIMIT 100;
```

Target:

```text
< 1 second
```

---

# PERF-002 Fact Query

SQL:

```sql
SELECT
SUM(actual_cost)
FROM curated.fact_cost;
```

Target:

```text
< 3 seconds
```

---

# PERF-003 Dashboard Query

SQL:

```sql
SELECT
project_key,
SUM(actual_cost)
FROM curated.fact_cost
GROUP BY project_key;
```

Target:

```text
< 5 seconds
```

---

# PERF-004 Star Schema Join

SQL:

```sql
SELECT
p.project_name,
SUM(f.actual_cost)
FROM curated.fact_cost f
JOIN curated.dim_project p
ON f.project_key = p.project_key
GROUP BY p.project_name;
```

Target:

```text
< 5 seconds
```

---

# 15. Acceptance Criteria

The Curated Layer is accepted only if all criteria are satisfied.

---

## AC-001

```text
All Dimension Tables Loaded
```

Status:

```text
PASS
```

---

## AC-002

```text
All Fact Tables Loaded
```

Status:

```text
PASS
```

---

## AC-003

```text
Referential Integrity = 100%
```

Status:

```text
PASS
```

---

## AC-004

```text
No Invalid KPI Calculations
```

Status:

```text
PASS
```

---

## AC-005

```text
SCD Type 2 Working Correctly
```

Status:

```text
PASS
```

---

## AC-006

```text
Audit Logging Operational
```

Status:

```text
PASS
```

---

## AC-007

```text
Data Quality Score >= 95%
```

Status:

```text
PASS
```

---

# 16. Validation Execution Checklist

---

## Dimension Validation

```text
[ ] dim_date

[ ] dim_project

[ ] dim_location

[ ] dim_vendor

[ ] dim_employee

[ ] dim_equipment

[ ] dim_risk
```

---

## Fact Validation

```text
[ ] fact_cost

[ ] fact_schedule

[ ] fact_maintenance

[ ] fact_workforce

[ ] fact_risk
```

---

## Integrity Validation

```text
[ ] Foreign Keys

[ ] Business Keys

[ ] Surrogate Keys

[ ] SCD Type 2
```

---

## KPI Validation

```text
[ ] Cost Variance

[ ] CPI

[ ] Schedule Variance

[ ] SPI

[ ] Risk Score
```

---

## Operational Validation

```text
[ ] Audit Logs

[ ] Reconciliation

[ ] Performance

[ ] ETL Execution
```

---

# 17. Sign-Off Procedure

The Curated Layer shall be approved by:

```text
Analytics Engineer

Data Engineer

Technical Lead

Project Sponsor
```

Approval Conditions:

```text
All validations completed

No critical defects

Acceptance criteria passed

Documentation updated
```

---

# Final Approval Statement

```text
The Curated Layer is considered production-ready
when all validation tests defined in this document
have been executed successfully and approved by
the designated stakeholders.
```

---

# End of Document

