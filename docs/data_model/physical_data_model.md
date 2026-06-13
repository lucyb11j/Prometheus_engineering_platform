# Physical Data Model (PDM)

## Prometheus Analytics Platform (EIAP)

**Version:** 1.0
**Status:** Approved for Database Implementation
**Database Engine:** PostgreSQL 16+
**Architecture:** Raw → Trusted → Curated
**Model Type:** Enterprise Data Warehouse + Star Schema

---

# 1. Purpose

This document defines the physical implementation of the Prometheus Analytics Platform (EIAP) data model in PostgreSQL.

The model supports:

* Analytics Engineering
* Data Warehousing
* Business Intelligence
* Machine Learning
* Forecasting
* Executive Reporting

---

# 2. Database Structure

Database:

```text
eiap
```

Schemas:

```text
raw
trusted
curated
audit
```

Purpose:

| Schema  | Purpose                         |
| ------- | ------------------------------- |
| raw     | Source data ingestion           |
| trusted | Cleansed and validated data     |
| curated | Analytical star schema          |
| audit   | Data quality and ETL monitoring |

---

# 3. Naming Standards

## Tables

Pattern:

```text
schema.table_name
```

Examples:

```text
raw.raw_projects
trusted.project
curated.dim_project
curated.fact_cost
```

---

## Primary Keys

Pattern:

```text
<table>_key
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
<table>_id
```

Examples:

```text
project_id
equipment_id
vendor_id
```

---

# 4. RAW Layer

## raw.raw_projects

| Column         | Type         | Nullable |
| -------------- | ------------ | -------- |
| ingestion_id   | BIGSERIAL    | No       |
| project_id     | VARCHAR(50)  | Yes      |
| project_name   | VARCHAR(200) | Yes      |
| project_type   | VARCHAR(100) | Yes      |
| location       | VARCHAR(100) | Yes      |
| start_date     | DATE         | Yes      |
| end_date       | DATE         | Yes      |
| load_timestamp | TIMESTAMP    | No       |

Primary Key:

```text
ingestion_id
```

---

## raw.raw_costs

| Column         | Type          |
| -------------- | ------------- |
| ingestion_id   | BIGSERIAL     |
| project_id     | VARCHAR(50)   |
| vendor_id      | VARCHAR(50)   |
| cost_date      | DATE          |
| planned_cost   | NUMERIC(18,2) |
| actual_cost    | NUMERIC(18,2) |
| load_timestamp | TIMESTAMP     |

---

## raw.raw_schedule

| Column           | Type         |
| ---------------- | ------------ |
| ingestion_id     | BIGSERIAL    |
| project_id       | VARCHAR(50)  |
| report_date      | DATE         |
| planned_progress | NUMERIC(8,2) |
| actual_progress  | NUMERIC(8,2) |
| load_timestamp   | TIMESTAMP    |

---

## raw.raw_equipment

| Column         | Type         |
| -------------- | ------------ |
| ingestion_id   | BIGSERIAL    |
| equipment_id   | VARCHAR(50)  |
| equipment_name | VARCHAR(200) |
| equipment_type | VARCHAR(100) |
| manufacturer   | VARCHAR(100) |
| load_timestamp | TIMESTAMP    |

---

# 5. TRUSTED Layer

## trusted.project

| Column           | Type         | Constraint |
| ---------------- | ------------ | ---------- |
| project_id       | VARCHAR(50)  | PK         |
| project_name     | VARCHAR(200) | NOT NULL   |
| project_type     | VARCHAR(100) | NOT NULL   |
| location         | VARCHAR(100) | NOT NULL   |
| start_date       | DATE         | NOT NULL   |
| planned_end_date | DATE         | NOT NULL   |
| status           | VARCHAR(50)  | NOT NULL   |

Indexes:

```sql
CREATE INDEX idx_project_type
ON trusted.project(project_type);
```

---

## trusted.equipment

| Column         | Type         |
| -------------- | ------------ |
| equipment_id   | VARCHAR(50)  |
| equipment_name | VARCHAR(200) |
| equipment_type | VARCHAR(100) |
| manufacturer   | VARCHAR(100) |
| purchase_date  | DATE         |
| status         | VARCHAR(50)  |

---

## trusted.employee

| Column      | Type         |
| ----------- | ------------ |
| employee_id | VARCHAR(50)  |
| full_name   | VARCHAR(200) |
| role        | VARCHAR(100) |
| department  | VARCHAR(100) |
| hire_date   | DATE         |

---

## trusted.vendor

| Column      | Type         |
| ----------- | ------------ |
| vendor_id   | VARCHAR(50)  |
| vendor_name | VARCHAR(200) |
| category    | VARCHAR(100) |
| country     | VARCHAR(100) |

---

## trusted.location

| Column      | Type         |
| ----------- | ------------ |
| location_id | VARCHAR(50)  |
| country     | VARCHAR(100) |
| region      | VARCHAR(100) |
| city        | VARCHAR(100) |
| site_name   | VARCHAR(200) |

---

## trusted.risk

| Column           | Type         |
| ---------------- | ------------ |
| risk_id          | VARCHAR(50)  |
| risk_name        | VARCHAR(200) |
| risk_category    | VARCHAR(100) |
| risk_description | TEXT         |

---

# 6. CURATED Layer

# 6.1 Dimensions

---

## curated.dim_date

| Column     | Type        |
| ---------- | ----------- |
| date_key   | INTEGER     |
| full_date  | DATE        |
| year       | SMALLINT    |
| quarter    | SMALLINT    |
| month      | SMALLINT    |
| month_name | VARCHAR(20) |
| week       | SMALLINT    |
| day        | SMALLINT    |
| day_name   | VARCHAR(20) |

Primary Key:

```text
date_key
```

---

## curated.dim_location

| Column       | Type         |
| ------------ | ------------ |
| location_key | BIGSERIAL    |
| location_id  | VARCHAR(50)  |
| country      | VARCHAR(100) |
| region       | VARCHAR(100) |
| city         | VARCHAR(100) |
| site_name    | VARCHAR(200) |

Primary Key:

```text
location_key
```

Unique:

```text
location_id
```

---

## curated.dim_project

| Column           | Type         |
| ---------------- | ------------ |
| project_key      | BIGSERIAL    |
| project_id       | VARCHAR(50)  |
| project_name     | VARCHAR(200) |
| project_type     | VARCHAR(100) |
| location_key     | BIGINT       |
| start_date       | DATE         |
| planned_end_date | DATE         |
| status           | VARCHAR(50)  |

Primary Key:

```text
project_key
```

Foreign Keys:

```text
location_key
→ dim_location(location_key)
```

Indexes:

```sql
CREATE INDEX idx_project_status
ON curated.dim_project(status);
```

---

## curated.dim_equipment

| Column         | Type         |
| -------------- | ------------ |
| equipment_key  | BIGSERIAL    |
| equipment_id   | VARCHAR(50)  |
| equipment_name | VARCHAR(200) |
| equipment_type | VARCHAR(100) |
| manufacturer   | VARCHAR(100) |
| purchase_date  | DATE         |
| status         | VARCHAR(50)  |

---

## curated.dim_employee

| Column       | Type         |
| ------------ | ------------ |
| employee_key | BIGSERIAL    |
| employee_id  | VARCHAR(50)  |
| full_name    | VARCHAR(200) |
| role         | VARCHAR(100) |
| department   | VARCHAR(100) |
| hire_date    | DATE         |

---

## curated.dim_vendor

| Column      | Type         |
| ----------- | ------------ |
| vendor_key  | BIGSERIAL    |
| vendor_id   | VARCHAR(50)  |
| vendor_name | VARCHAR(200) |
| category    | VARCHAR(100) |
| country     | VARCHAR(100) |

---

## curated.dim_risk

| Column           | Type         |
| ---------------- | ------------ |
| risk_key         | BIGSERIAL    |
| risk_id          | VARCHAR(50)  |
| risk_name        | VARCHAR(200) |
| risk_category    | VARCHAR(100) |
| risk_description | TEXT         |

---

# 6.2 Fact Tables

---

## curated.fact_cost

Grain:

One project cost transaction per day.

| Column        | Type          |
| ------------- | ------------- |
| cost_key      | BIGSERIAL     |
| date_key      | INTEGER       |
| project_key   | BIGINT        |
| vendor_key    | BIGINT        |
| planned_cost  | NUMERIC(18,2) |
| actual_cost   | NUMERIC(18,2) |
| forecast_cost | NUMERIC(18,2) |

Foreign Keys:

```text
date_key → dim_date
project_key → dim_project
vendor_key → dim_vendor
```

---

## curated.fact_schedule

Grain:

One project progress record per reporting day.

| Column           | Type         |
| ---------------- | ------------ |
| schedule_key     | BIGSERIAL    |
| date_key         | INTEGER      |
| project_key      | BIGINT       |
| planned_progress | NUMERIC(8,2) |
| actual_progress  | NUMERIC(8,2) |
| spi              | NUMERIC(8,4) |

---

## curated.fact_maintenance

Grain:

One maintenance event.

| Column           | Type          |
| ---------------- | ------------- |
| maintenance_key  | BIGSERIAL     |
| date_key         | INTEGER       |
| equipment_key    | BIGINT        |
| maintenance_type | VARCHAR(100)  |
| downtime_hours   | NUMERIC(10,2) |
| maintenance_cost | NUMERIC(18,2) |

---

## curated.fact_workforce

Grain:

One employee work record per day.

| Column             | Type          |
| ------------------ | ------------- |
| workforce_key      | BIGSERIAL     |
| date_key           | INTEGER       |
| employee_key       | BIGINT        |
| project_key        | BIGINT        |
| hours_worked       | NUMERIC(10,2) |
| productivity_score | NUMERIC(8,2)  |

---

## curated.fact_risk

Grain:

One risk occurrence event.

| Column         | Type          |
| -------------- | ------------- |
| risk_event_key | BIGSERIAL     |
| date_key       | INTEGER       |
| project_key    | BIGINT        |
| risk_key       | BIGINT        |
| probability    | NUMERIC(5,2)  |
| severity_score | NUMERIC(5,2)  |
| impact_cost    | NUMERIC(18,2) |
| impact_days    | INTEGER       |
| risk_score     | NUMERIC(10,2) |

Formula:

```text
risk_score = probability × severity_score
```

---

# 7. Indexing Strategy

Indexes required:

```sql
fact_cost(date_key)
fact_cost(project_key)

fact_schedule(project_key)

fact_maintenance(equipment_key)

fact_workforce(employee_key)

fact_risk(project_key)
fact_risk(risk_key)
```

---

# 8. Partitioning Strategy

Large fact tables should be partitioned by:

```text
date_key
```

Recommended:

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

# 9. Audit Schema

## audit.etl_execution_log

| Column         | Type         |
| -------------- | ------------ |
| execution_id   | BIGSERIAL    |
| pipeline_name  | VARCHAR(100) |
| start_time     | TIMESTAMP    |
| end_time       | TIMESTAMP    |
| status         | VARCHAR(50)  |
| rows_processed | BIGINT       |
| error_message  | TEXT         |

---

# 10. Physical Relationship Diagram

```text
dim_location
      │
      ▼
dim_project
      │
      ├──────────┐
      │          │
      ▼          ▼

fact_cost   fact_schedule

      ▲
      │

dim_vendor

---------------------------------

dim_equipment
      │
      ▼

fact_maintenance

---------------------------------

dim_employee
      │
      ▼

fact_workforce

---------------------------------

dim_risk
      │
      ▼

fact_risk

---------------------------------

dim_date

connected to all fact tables
```

# End of Document
