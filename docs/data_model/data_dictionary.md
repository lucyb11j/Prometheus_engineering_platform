# Data Dictionary

## Prometheus Analytics Platform

**Version:** 1.0
**Status:** Approved
**Related Documents:**

* Project Charter
* PRD
* Logical Data Model
* Physical Data Model

---

# 1. Purpose

This document defines the business meaning, ownership, data types, and usage rules for all entities and attributes used within the Prometheus Analytics Platform.

---

# 2. Naming Conventions

## Surrogate Keys

Pattern:

```text
*_key
```

Examples:

```text
project_key
equipment_key
vendor_key
```

---

## Business Keys

Pattern:

```text
*_id
```

Examples:

```text
project_id
vendor_id
employee_id
```

---

## Fact Measures

Pattern:

```text
metric_name
```

Examples:

```text
actual_cost
planned_cost
forecast_cost
risk_score
```

---

# 3. Dimension Dictionary

---

# dim_date

Business Purpose:

Supports time-series analysis and reporting.

| Field      | Type        | Description              |
| ---------- | ----------- | ------------------------ |
| date_key   | INTEGER     | Surrogate key (YYYYMMDD) |
| full_date  | DATE        | Calendar date            |
| year       | SMALLINT    | Year                     |
| quarter    | SMALLINT    | Quarter                  |
| month      | SMALLINT    | Month number             |
| month_name | VARCHAR(20) | Month name               |
| week       | SMALLINT    | ISO week                 |
| day        | SMALLINT    | Day number               |
| day_name   | VARCHAR(20) | Weekday name             |

---

# dim_project

Business Purpose:

Stores project master information.

| Field            | Type         | Description                  |
| ---------------- | ------------ | ---------------------------- |
| project_key      | BIGINT       | Surrogate key                |
| project_id       | VARCHAR(50)  | Business project identifier  |
| project_name     | VARCHAR(200) | Official project name        |
| project_type     | VARCHAR(100) | Construction, Mining, Energy |
| location_key     | BIGINT       | Associated location          |
| start_date       | DATE         | Project start date           |
| planned_end_date | DATE         | Planned completion date      |
| status           | VARCHAR(50)  | Active, Delayed, Closed      |

---

# dim_equipment

Business Purpose:

Stores heavy equipment information.

| Field          | Type         | Description          |
| -------------- | ------------ | -------------------- |
| equipment_key  | BIGINT       | Surrogate key        |
| equipment_id   | VARCHAR(50)  | Equipment identifier |
| equipment_name | VARCHAR(200) | Equipment name       |
| equipment_type | VARCHAR(100) | Equipment category   |
| manufacturer   | VARCHAR(100) | Manufacturer         |
| purchase_date  | DATE         | Acquisition date     |
| status         | VARCHAR(50)  | Current status       |

---

# dim_employee

Business Purpose:

Stores workforce information.

| Field        | Type         | Description         |
| ------------ | ------------ | ------------------- |
| employee_key | BIGINT       | Surrogate key       |
| employee_id  | VARCHAR(50)  | Employee identifier |
| full_name    | VARCHAR(200) | Employee full name  |
| role         | VARCHAR(100) | Job title           |
| department   | VARCHAR(100) | Business unit       |
| hire_date    | DATE         | Hiring date         |

---

# dim_vendor

Business Purpose:

Stores supplier information.

| Field       | Type         | Description       |
| ----------- | ------------ | ----------------- |
| vendor_key  | BIGINT       | Surrogate key     |
| vendor_id   | VARCHAR(50)  | Vendor identifier |
| vendor_name | VARCHAR(200) | Vendor name       |
| category    | VARCHAR(100) | Supplier category |
| country     | VARCHAR(100) | Vendor country    |

---

# dim_location

Business Purpose:

Stores project locations.

| Field        | Type         | Description         |
| ------------ | ------------ | ------------------- |
| location_key | BIGINT       | Surrogate key       |
| location_id  | VARCHAR(50)  | Location identifier |
| country      | VARCHAR(100) | Country             |
| region       | VARCHAR(100) | Region              |
| city         | VARCHAR(100) | City                |
| site_name    | VARCHAR(200) | Site name           |

---

# dim_risk

Business Purpose:

Stores risk classifications.

| Field            | Type         | Description          |
| ---------------- | ------------ | -------------------- |
| risk_key         | BIGINT       | Surrogate key        |
| risk_id          | VARCHAR(50)  | Risk identifier      |
| risk_name        | VARCHAR(200) | Risk title           |
| risk_category    | VARCHAR(100) | Risk category        |
| risk_description | TEXT         | Detailed description |

---

# 4. Fact Dictionary

---

# fact_cost

Business Purpose:

Stores financial performance metrics.

| Field         | Type          | Description      |
| ------------- | ------------- | ---------------- |
| cost_key      | BIGINT        | Surrogate key    |
| date_key      | INTEGER       | Reporting date   |
| project_key   | BIGINT        | Related project  |
| vendor_key    | BIGINT        | Related supplier |
| planned_cost  | NUMERIC(18,2) | Budgeted cost    |
| actual_cost   | NUMERIC(18,2) | Actual cost      |
| forecast_cost | NUMERIC(18,2) | Forecasted cost  |

Derived Metrics:

```text
Cost Variance = Actual Cost - Planned Cost

CPI = Earned Value / Actual Cost
```

---

# fact_schedule

Business Purpose:

Stores schedule performance.

| Field            | Type         | Description                   |
| ---------------- | ------------ | ----------------------------- |
| schedule_key     | BIGINT       | Surrogate key                 |
| date_key         | INTEGER      | Reporting date                |
| project_key      | BIGINT       | Related project               |
| planned_progress | NUMERIC(8,2) | Planned completion percentage |
| actual_progress  | NUMERIC(8,2) | Actual completion percentage  |
| spi              | NUMERIC(8,4) | Schedule Performance Index    |

Derived Metrics:

```text
Schedule Variance

SPI
```

---

# fact_maintenance

Business Purpose:

Stores maintenance events.

| Field            | Type          | Description              |
| ---------------- | ------------- | ------------------------ |
| maintenance_key  | BIGINT        | Surrogate key            |
| date_key         | INTEGER       | Maintenance date         |
| equipment_key    | BIGINT        | Equipment                |
| maintenance_type | VARCHAR(100)  | Preventive or corrective |
| downtime_hours   | NUMERIC(10,2) | Downtime duration        |
| maintenance_cost | NUMERIC(18,2) | Maintenance cost         |

Derived Metrics:

```text
MTBF

MTTR

Equipment Availability
```

---

# fact_workforce

Business Purpose:

Stores workforce productivity.

| Field              | Type          | Description            |
| ------------------ | ------------- | ---------------------- |
| workforce_key      | BIGINT        | Surrogate key          |
| date_key           | INTEGER       | Work date              |
| employee_key       | BIGINT        | Employee               |
| project_key        | BIGINT        | Project                |
| hours_worked       | NUMERIC(10,2) | Hours worked           |
| productivity_score | NUMERIC(8,2)  | Productivity indicator |

Derived Metrics:

```text
Productivity Rate

Labor Utilization
```

---

# fact_risk

Business Purpose:

Stores risk occurrences.

| Field          | Type          | Description         |
| -------------- | ------------- | ------------------- |
| risk_event_key | BIGINT        | Surrogate key       |
| date_key       | INTEGER       | Event date          |
| project_key    | BIGINT        | Project             |
| risk_key       | BIGINT        | Risk classification |
| probability    | NUMERIC(5,2)  | Risk probability    |
| severity_score | NUMERIC(5,2)  | Impact severity     |
| impact_cost    | NUMERIC(18,2) | Financial impact    |
| impact_days    | INTEGER       | Schedule impact     |
| risk_score     | NUMERIC(10,2) | Exposure score      |

Formula:

```text
risk_score = probability × severity_score
```

---

# 5. Data Ownership

| Domain    | Owner                      |
| --------- | -------------------------- |
| Projects  | PMO                        |
| Finance   | CFO Office                 |
| Equipment | Maintenance Department     |
| Workforce | Human Resources            |
| Risks     | Enterprise Risk Management |
| Analytics | Analytics Engineering Team |

---

# 6. Data Quality Rules

| Rule ID | Rule                               |
| ------- | ---------------------------------- |
| DQ-001  | project_id must be unique          |
| DQ-002  | actual_cost >= 0                   |
| DQ-003  | planned_progress between 0 and 100 |
| DQ-004  | actual_progress between 0 and 100  |
| DQ-005  | downtime_hours >= 0                |
| DQ-006  | probability between 0 and 1        |

---

# End of Document
