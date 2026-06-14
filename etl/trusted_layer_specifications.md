# Trusted Layer Specification

## Engineering Infrastructure Analytics Platform (EIAP)

**Version:** 1.0
**Status:** Approved for Development
**Layer:** Trusted
**Owner:** Analytics Engineering Team

---

# 1. Purpose

The Trusted Layer is responsible for transforming raw ingested data into validated, standardized, and business-ready datasets.

This layer acts as the single source of truth before analytical modeling and Data Warehouse population.

Data Flow:

```text
CSV Files
    ↓
RAW Layer
    ↓
TRUSTED Layer
    ↓
CURATED Layer
```

---

# 2. Objectives

The Trusted Layer must:

* Remove duplicates
* Validate business keys
* Standardize formats
* Validate business rules
* Ensure referential integrity
* Create auditability
* Generate quality metrics

---

# 3. Trusted Layer Architecture

Schema:

```sql
trusted
```

Tables:

```text
trusted.project

trusted.vendor

trusted.employee

trusted.equipment

trusted.location

trusted.cost

trusted.schedule

trusted.maintenance

trusted.risk
```

---

# 4. Data Quality Framework

All records entering Trusted must pass validation.

Validation Categories:

```text
Completeness

Uniqueness

Consistency

Validity

Referential Integrity
```

---

# 5. Common Transformation Rules

## TR-001 Null Handling

Mandatory fields:

```text
project_id
vendor_id
employee_id
equipment_id
```

Rule:

```text
Reject records with NULL business keys
```

---

## TR-002 Duplicate Removal

Rule:

```text
Keep latest record
Remove duplicates
```

Example:

```text
project_id = PRJ001

Multiple identical records

Keep most recent
```

---

## TR-003 Text Standardization

Convert:

```text
active
ACTIVE
Active
```

Into:

```text
Active
```

Method:

```python
str.title()
```

---

## TR-004 Whitespace Cleanup

Convert:

```text
" Lima Highway Project "
```

Into:

```text
"Lima Highway Project"
```

Method:

```python
str.strip()
```

---

## TR-005 Date Standardization

Accepted Formats:

```text
YYYY-MM-DD
```

Examples:

```text
2025-01-15
2025-12-31
```

---

## TR-006 Numeric Validation

Examples:

```text
planned_cost >= 0

actual_cost >= 0

maintenance_cost >= 0
```

---

# 6. Trusted Project Specification

Source:

```text
raw.raw_projects
```

Destination:

```text
trusted.project
```

---

## Business Rules

### PROJECT-001

Project ID must be unique.

Example:

```text
PRJ001
```

---

### PROJECT-002

Budget must be positive.

Validation:

```text
budget > 0
```

---

### PROJECT-003

Project status must belong to:

```text
Active

Completed

Delayed

Cancelled
```

---

### PROJECT-004

End date must be after start date.

Validation:

```text
end_date > start_date
```

---

# 7. Trusted Vendor Specification

Source:

```text
raw.raw_vendors
```

Destination:

```text
trusted.vendor
```

Business Rules:

```text
vendor_id unique

vendor_name required

category required
```

Allowed Categories:

```text
Materials

Equipment

Services

Logistics

Consulting
```

---

# 8. Trusted Employee Specification

Source:

```text
raw.raw_employees
```

Destination:

```text
trusted.employee
```

Business Rules:

```text
employee_id unique

hire_date <= current_date

salary > 0
```

---

# 9. Trusted Equipment Specification

Source:

```text
raw.raw_equipment
```

Destination:

```text
trusted.equipment
```

Allowed Status:

```text
Active

Maintenance

Retired
```

Business Rules:

```text
equipment_id unique

purchase_date <= current_date
```

---

# 10. Trusted Cost Specification

Source:

```text
raw.raw_costs
```

Destination:

```text
trusted.cost
```

Business Rules:

```text
planned_cost >= 0

actual_cost >= 0
```

---

## Variance Calculation

Formula:

```text
cost_variance = actual_cost - planned_cost
```

---

## Cost Performance Index

Formula:

```text
CPI = earned_value / actual_cost
```

---

# 11. Trusted Schedule Specification

Source:

```text
raw.raw_schedule
```

Destination:

```text
trusted.schedule
```

Business Rules:

```text
planned_progress between 0 and 100

actual_progress between 0 and 100
```

---

## Schedule Variance

Formula:

```text
SV = actual_progress - planned_progress
```

---

## Schedule Performance Index

Formula:

```text
SPI = actual_progress / planned_progress
```

Special Case:

```text
If planned_progress = 0

SPI = NULL
```

---

# 12. Trusted Maintenance Specification

Source:

```text
raw.raw_maintenance
```

Destination:

```text
trusted.maintenance
```

Business Rules:

```text
downtime_hours >= 0

maintenance_cost >= 0
```

Allowed Types:

```text
Preventive

Corrective

Predictive
```

---

# 13. Trusted Risk Specification

Source:

```text
raw.raw_risks
```

Destination:

```text
trusted.risk
```

Business Rules:

```text
0 <= probability <= 1

severity_score between 1 and 10

impact_cost >= 0
```

---

## Risk Score

Formula:

```text
risk_score = probability × severity_score
```

---

# 14. Rejected Records Framework

Schema:

```sql
audit
```

Table:

```sql
audit.rejected_records
```

Columns:

```text
rejection_id

source_table

record_id

rejection_reason

rejected_at
```

Purpose:

Store invalid records for review.

---

# 15. Audit Logging

Table:

```sql
audit.etl_execution_log
```

Captured Information:

```text
Pipeline Name

Start Time

End Time

Status

Rows Processed

Rows Rejected

Execution Duration
```

---

# 16. Data Quality KPIs

Metrics:

```text
Completeness %

Duplicate Rate %

Rejected Records %

Referential Integrity %

Data Freshness
```

Target:

```text
Data Quality Score ≥ 95%
```

---

# 17. Trusted Layer Output

Expected Outputs:

```text
trusted.project

trusted.vendor

trusted.employee

trusted.location

trusted.equipment

trusted.cost

trusted.schedule

trusted.maintenance

trusted.risk
```

These tables become the official source for all Curated Layer dimensions and fact tables.

---

# 18. Future Enhancements

Future Data Domains:

```text
Materials

Contracts

Weather

IoT Sensors

Safety Incidents

Quality Inspections
```

Future Capabilities:

```text
Automated Data Profiling

Great Expectations

dbt Tests

Anomaly Detection

Data Observability
```

---

# End of Document
