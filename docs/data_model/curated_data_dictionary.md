# Curated Data Dictionary

## Engineering Infrastructure Analytics Platform (EIAP)

**Version:** 1.0
**Status:** Approved
**Layer:** Curated
**Schema:** curated

---

# 1. Purpose

This document provides detailed metadata definitions for all analytical tables within the Curated Layer.

The objective is to establish a common business vocabulary across:

* Analytics Engineering
* Data Engineering
* Business Intelligence
* Data Science
* Executive Reporting

---

# 2. Curated Schema Overview

Dimensions:

```text
dim_date
dim_project
dim_location
dim_vendor
dim_employee
dim_equipment
dim_risk
```

Facts:

```text
fact_cost
fact_schedule
fact_maintenance
fact_workforce
fact_risk
```

---

# 3. DIM_DATE

## Table Description

Calendar dimension used across all fact tables.

---

| Column     | Type        | Description               | Source    |
| ---------- | ----------- | ------------------------- | --------- |
| date_key   | INTEGER     | Surrogate date identifier | Generated |
| full_date  | DATE        | Calendar date             | Generated |
| year       | INTEGER     | Year number               | Generated |
| quarter    | INTEGER     | Quarter number            | Generated |
| month      | INTEGER     | Month number              | Generated |
| month_name | VARCHAR(20) | Month name                | Generated |
| week       | INTEGER     | ISO week number           | Generated |
| day        | INTEGER     | Day of month              | Generated |
| day_name   | VARCHAR(20) | Weekday name              | Generated |

---

# 4. DIM_PROJECT

## Table Description

Project master dimension.

---

| Column          | Type          | Description          | Source          |
| --------------- | ------------- | -------------------- | --------------- |
| project_key     | BIGINT        | Surrogate key        | ETL             |
| project_id      | VARCHAR(50)   | Business identifier  | trusted.project |
| project_name    | VARCHAR(255)  | Project name         | trusted.project |
| project_type    | VARCHAR(100)  | Project category     | trusted.project |
| status          | VARCHAR(50)   | Project status       | trusted.project |
| budget          | NUMERIC(18,2) | Approved budget      | trusted.project |
| start_date      | DATE          | Planned start date   | trusted.project |
| end_date        | DATE          | Planned end date     | trusted.project |
| effective_date  | DATE          | SCD start date       | ETL             |
| expiration_date | DATE          | SCD end date         | ETL             |
| is_current      | BOOLEAN       | Current version flag | ETL             |

---

# 5. DIM_LOCATION

## Table Description

Project geographic dimension.

---

| Column       | Type         | Description         | Source           |
| ------------ | ------------ | ------------------- | ---------------- |
| location_key | BIGINT       | Surrogate key       | ETL              |
| location_id  | VARCHAR(50)  | Business identifier | trusted.location |
| country      | VARCHAR(100) | Country             | trusted.location |
| region       | VARCHAR(100) | Region              | trusted.location |
| city         | VARCHAR(100) | City                | trusted.location |
| site_name    | VARCHAR(255) | Site name           | trusted.location |

---

# 6. DIM_VENDOR

## Table Description

Vendor master dimension.

---

| Column          | Type         | Description       | Source         |
| --------------- | ------------ | ----------------- | -------------- |
| vendor_key      | BIGINT       | Surrogate key     | ETL            |
| vendor_id       | VARCHAR(50)  | Vendor identifier | trusted.vendor |
| vendor_name     | VARCHAR(255) | Vendor name       | trusted.vendor |
| category        | VARCHAR(100) | Vendor category   | trusted.vendor |
| country         | VARCHAR(100) | Vendor country    | trusted.vendor |
| effective_date  | DATE         | SCD start date    | ETL            |
| expiration_date | DATE         | SCD end date      | ETL            |
| is_current      | BOOLEAN      | Current version   | ETL            |

---

# 7. DIM_EMPLOYEE

## Table Description

Employee dimension.

---

| Column          | Type          | Description         | Source           |
| --------------- | ------------- | ------------------- | ---------------- |
| employee_key    | BIGINT        | Surrogate key       | ETL              |
| employee_id     | VARCHAR(50)   | Employee identifier | trusted.employee |
| full_name       | VARCHAR(255)  | Employee name       | trusted.employee |
| department      | VARCHAR(100)  | Department          | trusted.employee |
| role            | VARCHAR(100)  | Job role            | trusted.employee |
| salary          | NUMERIC(18,2) | Base salary         | trusted.employee |
| hire_date       | DATE          | Hiring date         | trusted.employee |
| effective_date  | DATE          | SCD start date      | ETL              |
| expiration_date | DATE          | SCD end date        | ETL              |
| is_current      | BOOLEAN       | Current record      | ETL              |

---

# 8. DIM_EQUIPMENT

## Table Description

Equipment master dimension.

---

| Column          | Type         | Description          | Source            |
| --------------- | ------------ | -------------------- | ----------------- |
| equipment_key   | BIGINT       | Surrogate key        | ETL               |
| equipment_id    | VARCHAR(50)  | Equipment identifier | trusted.equipment |
| equipment_name  | VARCHAR(255) | Equipment name       | trusted.equipment |
| equipment_type  | VARCHAR(100) | Equipment category   | trusted.equipment |
| manufacturer    | VARCHAR(255) | Manufacturer         | trusted.equipment |
| status          | VARCHAR(50)  | Equipment status     | trusted.equipment |
| purchase_date   | DATE         | Purchase date        | trusted.equipment |
| effective_date  | DATE         | SCD start date       | ETL               |
| expiration_date | DATE         | SCD end date         | ETL               |
| is_current      | BOOLEAN      | Current record       | ETL               |

---

# 9. DIM_RISK

## Table Description

Risk catalog dimension.

---

| Column        | Type          | Description           | Source       |
| ------------- | ------------- | --------------------- | ------------ |
| risk_key      | BIGINT        | Surrogate key         | ETL          |
| risk_id       | VARCHAR(50)   | Risk identifier       | trusted.risk |
| risk_category | VARCHAR(100)  | Risk category         | trusted.risk |
| severity      | INTEGER       | Severity level        | trusted.risk |
| probability   | NUMERIC(5,2)  | Probability value     | trusted.risk |
| risk_score    | NUMERIC(10,2) | Calculated risk score | ETL          |

---

# 10. FACT_COST

## Table Description

Stores project cost transactions.

---

## Grain

```text
One project
+
One vendor
+
One date
```

---

| Column        | Type          | Description            | Source       |
| ------------- | ------------- | ---------------------- | ------------ |
| cost_fact_key | BIGINT        | Fact surrogate key     | ETL          |
| date_key      | BIGINT        | Date FK                | dim_date     |
| project_key   | BIGINT        | Project FK             | dim_project  |
| vendor_key    | BIGINT        | Vendor FK              | dim_vendor   |
| planned_cost  | NUMERIC(18,2) | Planned cost           | trusted.cost |
| actual_cost   | NUMERIC(18,2) | Actual cost            | trusted.cost |
| cost_variance | NUMERIC(18,2) | Actual - Planned       | ETL          |
| earned_value  | NUMERIC(18,2) | Earned value           | trusted.cost |
| cpi           | NUMERIC(10,4) | Cost Performance Index | ETL          |

---

# 11. FACT_SCHEDULE

## Grain

```text
One project status snapshot
per reporting date
```

---

| Column            | Type          | Description                | Source           |
| ----------------- | ------------- | -------------------------- | ---------------- |
| schedule_fact_key | BIGINT        | Fact surrogate key         | ETL              |
| date_key          | BIGINT        | Date FK                    | dim_date         |
| project_key       | BIGINT        | Project FK                 | dim_project      |
| planned_progress  | NUMERIC(5,2)  | Planned progress %         | trusted.schedule |
| actual_progress   | NUMERIC(5,2)  | Actual progress %          | trusted.schedule |
| schedule_variance | NUMERIC(5,2)  | Actual - Planned           | ETL              |
| spi               | NUMERIC(10,4) | Schedule Performance Index | ETL              |

---

# 12. FACT_MAINTENANCE

## Grain

```text
One maintenance event
```

---

| Column                | Type          | Description        | Source              |
| --------------------- | ------------- | ------------------ | ------------------- |
| maintenance_fact_key  | BIGINT        | Fact surrogate key | ETL                 |
| date_key              | BIGINT        | Date FK            | dim_date            |
| equipment_key         | BIGINT        | Equipment FK       | dim_equipment       |
| project_key           | BIGINT        | Project FK         | dim_project         |
| downtime_hours        | NUMERIC(10,2) | Downtime duration  | trusted.maintenance |
| maintenance_cost      | NUMERIC(18,2) | Maintenance cost   | trusted.maintenance |
| repair_duration_hours | NUMERIC(10,2) | Repair duration    | trusted.maintenance |

---

# 13. FACT_WORKFORCE

## Grain

```text
One employee
per project
per reporting date
```

---

| Column             | Type          | Description        | Source                        |
| ------------------ | ------------- | ------------------ | ----------------------------- |
| workforce_fact_key | BIGINT        | Fact surrogate key | ETL                           |
| date_key           | BIGINT        | Date FK            | dim_date                      |
| employee_key       | BIGINT        | Employee FK        | dim_employee                  |
| project_key        | BIGINT        | Project FK         | dim_project                   |
| hours_worked       | NUMERIC(10,2) | Worked hours       | trusted.employee_productivity |
| overtime_hours     | NUMERIC(10,2) | Overtime hours     | trusted.employee_productivity |
| labor_cost         | NUMERIC(18,2) | Labor cost         | trusted.employee_productivity |
| productivity_score | NUMERIC(10,2) | Productivity KPI   | ETL                           |

---

# 14. FACT_RISK

## Grain

```text
One risk assessment
per project
per date
```

---

| Column        | Type          | Description            | Source       |
| ------------- | ------------- | ---------------------- | ------------ |
| risk_fact_key | BIGINT        | Fact surrogate key     | ETL          |
| date_key      | BIGINT        | Date FK                | dim_date     |
| project_key   | BIGINT        | Project FK             | dim_project  |
| risk_key      | BIGINT        | Risk FK                | dim_risk     |
| probability   | NUMERIC(5,2)  | Probability            | trusted.risk |
| severity      | INTEGER       | Severity               | trusted.risk |
| impact_cost   | NUMERIC(18,2) | Financial impact       | trusted.risk |
| impact_days   | INTEGER       | Schedule impact        | trusted.risk |
| risk_score    | NUMERIC(10,2) | Probability × Severity | ETL          |

---

# 15. Business KPIs

| KPI               | Formula                            |
| ----------------- | ---------------------------------- |
| Cost Variance     | actual_cost - planned_cost         |
| CPI               | earned_value / actual_cost         |
| Schedule Variance | actual_progress - planned_progress |
| SPI               | actual_progress / planned_progress |
| Risk Score        | probability × severity             |
| MTTR              | Total Repair Time / Failures       |
| MTBF              | Operating Time / Failures          |

---

# 16. Data Ownership

| Domain    | Owner                     |
| --------- | ------------------------- |
| Projects  | Project Management Office |
| Vendors   | Procurement               |
| Employees | Human Resources           |
| Equipment | Asset Management          |
| Costs     | Finance                   |
| Risks     | Risk Management           |

---

# 17. Data Retention Policy

Dimensions:

```text
Permanent Historical Storage
```

Facts:

```text
Minimum 10 Years
```

Audit Tables:

```text
Minimum 5 Years
```

---

# 18. End of Document

