# 09_Data_Dictionary.md

# PART 1

# Enterprise Data Dictionary

## Engineering Infrastructure Analytics Platform (EIAP)

### Enterprise Infrastructure Predictive Control Tower

---

# Document Information

| Field          | Value                                         |
| -------------- | --------------------------------------------- |
| Project        | Engineering Infrastructure Analytics Platform |
| Document       | Enterprise Data Dictionary                    |
| Version        | 1.0                                           |
| Database       | PostgreSQL                                    |
| Classification | Enterprise Data Governance                    |
| Status         | Approved                                      |

---

# 1. Purpose

This document defines the official metadata repository for all data assets within the Engineering Infrastructure Analytics Platform.

The data dictionary establishes:

* Data definitions
* Naming standards
* Business meanings
* Data ownership
* Validation rules
* Metadata governance

---

# 2. Naming Standards

## Tables

Format:

```text
Dim_<Entity>
Fact_<Entity>
Bridge_<Entity>
```

Examples:

```text
Dim_Project
Dim_Equipment
Fact_Cost
Fact_Productivity
```

---

## Columns

Format:

```text
snake_case
```

Examples:

```text
project_id
actual_cost
forecast_cost
```

---

## Primary Keys

Format:

```text
entity_id
```

Examples:

```text
project_id
employee_id
equipment_id
```

---

## Foreign Keys

Format:

```text
referenced_entity_id
```

Examples:

```text
project_id
time_id
vendor_id
```

---

# 3. Data Classification

| Classification | Description                    |
| -------------- | ------------------------------ |
| Public         | Public information             |
| Internal       | Internal business data         |
| Confidential   | Financial and operational data |
| Restricted     | Security-sensitive data        |

---

# 4. Dimension Tables

---

# 4.1 Dim_Time

## Description

Stores temporal attributes used across all analytical models.

---

## Owner

Analytics Engineering Team

---

## Refresh Frequency

Daily

---

## Columns

### time_id

| Attribute   | Value              |
| ----------- | ------------------ |
| Data Type   | INTEGER            |
| Nullable    | No                 |
| Primary Key | Yes                |
| Description | Surrogate time key |

---

### date

| Attribute   | Value         |
| ----------- | ------------- |
| Data Type   | DATE          |
| Nullable    | No            |
| Description | Calendar date |

---

### day

| Attribute | Value    |
| --------- | -------- |
| Data Type | SMALLINT |
| Nullable  | No       |
| Range     | 1–31     |

---

### month

| Attribute | Value    |
| --------- | -------- |
| Data Type | SMALLINT |
| Nullable  | No       |
| Range     | 1–12     |

---

### quarter

| Attribute | Value    |
| --------- | -------- |
| Data Type | SMALLINT |
| Nullable  | No       |
| Range     | 1–4      |

---

### year

| Attribute | Value   |
| --------- | ------- |
| Data Type | INTEGER |
| Nullable  | No      |

---

### week

| Attribute | Value    |
| --------- | -------- |
| Data Type | SMALLINT |
| Nullable  | No       |

---

### weekday

| Attribute | Value       |
| --------- | ----------- |
| Data Type | VARCHAR(20) |
| Nullable  | No          |

---

# 4.2 Dim_Project

## Description

Master project dimension.

---

## Owner

Project Management Office (PMO)

---

## Refresh Frequency

Daily

---

## Columns

### project_id

| Attribute | Value  |
| --------- | ------ |
| Type      | BIGINT |
| PK        | Yes    |
| Nullable  | No     |

---

### project_code

| Attribute | Value       |
| --------- | ----------- |
| Type      | VARCHAR(50) |
| Unique    | Yes         |
| Nullable  | No          |

---

### project_name

| Attribute | Value        |
| --------- | ------------ |
| Type      | VARCHAR(250) |
| Nullable  | No           |

---

### project_type

| Attribute | Value        |
| --------- | ------------ |
| Type      | VARCHAR(100) |
| Nullable  | No           |

Examples:

* Highway
* Mining
* Industrial Plant
* Bridge
* Building

---

### start_date

| Attribute | Value |
| --------- | ----- |
| Type      | DATE  |
| Nullable  | No    |

---

### end_date

| Attribute | Value |
| --------- | ----- |
| Type      | DATE  |
| Nullable  | Yes   |

---

### approved_budget

| Attribute | Value         |
| --------- | ------------- |
| Type      | NUMERIC(18,2) |
| Nullable  | No            |

Business Rule:

Must be greater than zero.

---

### location_id

| Attribute | Value  |
| --------- | ------ |
| Type      | BIGINT |
| FK        | Yes    |

---

### status_id

| Attribute | Value  |
| --------- | ------ |
| Type      | BIGINT |
| FK        | Yes    |

---

# 4.3 Dim_Location

## Description

Stores geographical information.

---

## Columns

### location_id

BIGINT

Primary Key

---

### country

VARCHAR(100)

---

### region

VARCHAR(100)

---

### city

VARCHAR(100)

---

### site_name

VARCHAR(250)

---

### latitude

NUMERIC(10,6)

---

### longitude

NUMERIC(10,6)

---

# 4.4 Dim_Status

## Description

Project status catalog.

---

## Columns

### status_id

BIGINT

PK

---

### status_name

VARCHAR(50)

Allowed Values:

```text
On Track
Warning
Critical
Completed
Cancelled
```

---

# 4.5 Dim_Cost_Category

## Description

Financial classification dimension.

---

## Columns

### category_id

BIGINT

PK

---

### category_name

VARCHAR(100)

Examples:

```text
Labor
Materials
Equipment
Fuel
Transportation
Subcontractors
Engineering
Permits
Insurance
Contingency
```

---

# 4.6 Dim_Vendor

## Description

Suppliers and contractors.

---

## Columns

### vendor_id

BIGINT

PK

---

### vendor_code

VARCHAR(50)

Unique

---

### vendor_name

VARCHAR(250)

---

### vendor_type

VARCHAR(100)

Examples:

```text
Supplier
Contractor
Consultant
Equipment Rental
```

---

### tax_identifier

VARCHAR(50)

---

### contract_start_date

DATE

---

### contract_end_date

DATE

---

# 4.7 Dim_Equipment

## Description

Fleet and equipment master table.

---

## Owner

Maintenance Department

---

## Columns

### equipment_id

BIGINT

PK

---

### equipment_code

VARCHAR(50)

Unique

---

### equipment_name

VARCHAR(250)

Examples:

```text
Excavator CAT320
Bulldozer D8
Crane 100T
Dump Truck
Generator
```

---

### equipment_type

VARCHAR(100)

---

### manufacturer

VARCHAR(100)

---

### acquisition_date

DATE

---

### acquisition_cost

NUMERIC(18,2)

---

### useful_life_years

INTEGER

---

### replacement_cost

NUMERIC(18,2)

---

# 4.8 Dim_Maintenance

## Description

Maintenance classification.

---

## Columns

### maintenance_id

BIGINT

PK

---

### maintenance_type

VARCHAR(50)

Allowed Values:

```text
Preventive
Corrective
Predictive
Emergency
```

---

### maintenance_frequency_days

INTEGER

---

# 4.9 Dim_Employee

## Description

Employee dimension.

---

## Columns

### employee_id

BIGINT

PK

---

### employee_code

VARCHAR(50)

Unique

---

### full_name

VARCHAR(250)

---

### position

VARCHAR(150)

---

### department

VARCHAR(100)

---

### hire_date

DATE

---

### salary_rate

NUMERIC(18,2)

---

### employment_status

VARCHAR(50)

Allowed Values:

```text
Active
Inactive
On Leave
Retired
```

---

# 5. Slowly Changing Dimensions (SCD)

---

## SCD Type 2

Implemented for:

* Dim_Project
* Dim_Employee
* Dim_Equipment
* Dim_Vendor

Additional Columns:

```text
effective_start_date
effective_end_date
current_record_flag
```

Purpose:

Maintain historical attribute changes.

---

# 6. Data Ownership Matrix

| Table         | Business Owner |
| ------------- | -------------- |
| Dim_Project   | PMO            |
| Dim_Employee  | HR             |
| Dim_Equipment | Maintenance    |
| Dim_Vendor    | Procurement    |
| Dim_Location  | Operations     |

---

# 09_Data_Dictionary.md

# PART 2

# Fact Tables, KPIs and Analytical Metrics

## Engineering Infrastructure Analytics Platform (EIAP)

### Enterprise Infrastructure Predictive Control Tower

---

# 7. Fact Tables

---

# 7.1 Fact_Project

## Description

Stores project execution metrics.

---

## Business Process

Project Control

---

## Grain

One project per day.

---

## Refresh Frequency

Daily

---

## Foreign Keys

| Column      | Reference    |
| ----------- | ------------ |
| project_id  | Dim_Project  |
| time_id     | Dim_Time     |
| location_id | Dim_Location |
| status_id   | Dim_Status   |

---

## Measures

### planned_progress

| Attribute | Value        |
| --------- | ------------ |
| Type      | NUMERIC(5,2) |
| Unit      | %            |
| Range     | 0-100        |

Description:

Planned project progress.

---

### actual_progress

| Attribute | Value        |
| --------- | ------------ |
| Type      | NUMERIC(5,2) |
| Unit      | %            |

Description:

Actual progress achieved.

---

### schedule_variance

| Attribute | Value         |
| --------- | ------------- |
| Type      | NUMERIC(18,2) |

Description:

Difference between planned and actual progress.

---

### spi

Description:

Schedule Performance Index.

Formula:

SPI=\frac{EV}{PV}

---

### project_risk_score

| Attribute | Value        |
| --------- | ------------ |
| Type      | NUMERIC(5,2) |
| Range     | 0-100        |

Description:

Project risk score.

---

# Business Rules

BR-001

actual_progress ≤ 100

---

BR-002

SPI cannot be negative.

---

# 7.2 Fact_Cost

## Description

Stores financial metrics.

---

## Business Process

Cost Control

---

## Grain

One project per day per cost category.

---

## Foreign Keys

| Column      | Reference         |
| ----------- | ----------------- |
| project_id  | Dim_Project       |
| time_id     | Dim_Time          |
| category_id | Dim_Cost_Category |
| vendor_id   | Dim_Vendor        |

---

## Measures

### budget_cost

Type:

NUMERIC(18,2)

Description:

Approved budget.

---

### actual_cost

Type:

NUMERIC(18,2)

Description:

Actual incurred cost.

---

### planned_value

Type:

NUMERIC(18,2)

Description:

PV

---

### earned_value

Type:

NUMERIC(18,2)

Description:

EV

---

### cost_variance

Description:

Cost variance.

Formula:

CV=EV-AC

---

### cpi

Description:

Cost Performance Index.

Formula:

CPI=\frac{EV}{AC}

---

### forecast_cost

Description:

Forecast at completion.

Formula:

EAC=\frac{BAC}{CPI}

---

# Business Rules

BR-003

actual_cost ≥ 0

---

BR-004

budget_cost ≥ actual_cost warning threshold 5%

---

# 7.3 Fact_Equipment

## Description

Stores equipment operational metrics.

---

## Business Process

Maintenance Management

---

## Grain

One equipment per day.

---

## Foreign Keys

| Column         | Reference       |
| -------------- | --------------- |
| equipment_id   | Dim_Equipment   |
| time_id        | Dim_Time        |
| maintenance_id | Dim_Maintenance |
| location_id    | Dim_Location    |

---

## Measures

### operating_hours

Unit:

Hours

---

### downtime_hours

Unit:

Hours

---

### maintenance_cost

Unit:

USD

---

### availability

Description:

Equipment availability.

Formula:

Availability=\frac{Operating\ Time}{Total\ Time}

---

### utilization

Description:

Equipment utilization.

Formula:

Used Time / Available Time

---

### mtbf

Description:

Mean Time Between Failures.

Formula:

MTBF = Total Running Hours / Number of Failures

---

### mttr

Description:

Mean Time To Repair.

Formula:

MTTR = Repair Hours / Repairs

---

# Business Rules

BR-005

Availability must be between 0 and 100%.

---

# 7.4 Fact_Productivity

## Description

Stores workforce productivity.

---

## Business Process

Workforce Management

---

## Grain

One employee per day.

---

## Foreign Keys

| Column      | Reference    |
| ----------- | ------------ |
| employee_id | Dim_Employee |
| project_id  | Dim_Project  |
| time_id     | Dim_Time     |

---

## Measures

### hours_worked

Unit:

Hours

---

### productive_hours

Unit:

Hours

---

### productivity_index

Description:

Productive efficiency.

Formula:

Productivity\ Index=\frac{Productive\ Hours}{Total\ Hours}

---

### labor_cost

Description:

Labor cost.

Formula:

Hours × Hourly Rate

---

# Business Rules

BR-006

productive_hours ≤ hours_worked

---

# 7.5 Fact_Risk

## Description

Stores risk indicators.

---

## Business Process

Enterprise Risk Management

---

## Grain

One project per day.

---

## Foreign Keys

| Column     | Reference   |
| ---------- | ----------- |
| project_id | Dim_Project |
| time_id    | Dim_Time    |

---

## Measures

### probability

Type:

NUMERIC(5,2)

Range:

0-100

---

### impact

Type:

NUMERIC(5,2)

Range:

0-100

---

### risk_score

Description:

Risk exposure score.

Formula:

Probability × Impact

---

### mitigation_cost

Type:

NUMERIC(18,2)

---

### risk_level

Allowed Values:

* Low
* Medium
* High
* Critical

---

# Business Rules

BR-007

Risk Score > 70 = High Risk

---

# 7.6 Fact_Forecast

## Description

Stores predictive analytics results.

---

## Business Process

Forecasting

---

## Grain

One project prediction per execution date.

---

## Foreign Keys

| Column     | Reference   |
| ---------- | ----------- |
| project_id | Dim_Project |
| time_id    | Dim_Time    |

---

## Measures

### predicted_cost

Forecasted final cost.

---

### predicted_delay_days

Forecasted delay.

---

### predicted_risk

Forecasted risk score.

---

### confidence_interval

Prediction confidence interval.

---

### model_version

Model identifier.

---

### forecast_date

Prediction generation date.

---

# Business Rules

BR-008

Prediction confidence > 80%

---

# 8. Analytical KPIs

---

# Project KPIs

## SPI

Schedule Performance Index.

Interpretation:

| Value   | Meaning           |
| ------- | ----------------- |
| SPI > 1 | Ahead of schedule |
| SPI = 1 | On schedule       |
| SPI < 1 | Behind schedule   |

---

## Schedule Variance

Formula:

SV = EV − PV

---

# Financial KPIs

## CPI

Cost Performance Index.

Interpretation:

| Value   | Meaning      |
| ------- | ------------ |
| CPI > 1 | Under Budget |
| CPI = 1 | On Budget    |
| CPI < 1 | Over Budget  |

---

## Cost Variance

Formula:

CV = EV − AC

---

## Forecast at Completion

Formula:

EAC = BAC / CPI

---

# Equipment KPIs

## Availability

Target:

≥ 90%

---

## Utilization

Target:

≥ 75%

---

## MTBF

Higher is better.

---

## MTTR

Lower is better.

---

# Workforce KPIs

## Productivity Index

Target:

≥ 85%

---

## Labor Cost Variance

Actual Labor Cost − Planned Labor Cost

---

# Risk KPIs

## Risk Exposure

Probability × Impact

---

## High Risk Projects

Projects with Risk Score > 70

---

# Forecasting KPIs

## Forecast Accuracy

Formula:

MAPE

Target:

< 10%

---

## Model Precision

Target:

> 85%

---

## Model Recall

Target:

> 80%

---

# 9. Aggregation Tables

---

## Agg_Project_Monthly

Monthly project metrics.

---

## Agg_Cost_Monthly

Monthly financial metrics.

---

## Agg_Equipment_Monthly

Monthly equipment metrics.

---

## Agg_Workforce_Monthly

Monthly workforce metrics.

---

## Agg_Risk_Monthly

Monthly risk indicators.

---

# 10. Materialized Views

---

## mv_executive_dashboard

Executive KPIs.

---

## mv_project_health

Project status.

---

## mv_equipment_health

Equipment status.

---

## mv_cost_forecast

Forecast metrics.

---

## mv_risk_heatmap

Risk analysis.

---

# 11. Data Mart Mapping

| Data Mart   | Tables                             |
| ----------- | ---------------------------------- |
| Executive   | Fact_Project, Fact_Cost, Fact_Risk |
| Project     | Fact_Project                       |
| Financial   | Fact_Cost                          |
| Maintenance | Fact_Equipment                     |
| Workforce   | Fact_Productivity                  |
| Forecasting | Fact_Forecast                      |

---

# 09_Data_Dictionary.md

# PART 3

# Data Governance, Metadata, Lineage and Data Quality

## Engineering Infrastructure Analytics Platform (EIAP)

### Enterprise Infrastructure Predictive Control Tower

---

# 12. Metadata Management

## Purpose

Metadata provides context, meaning, ownership, lineage, and governance for all enterprise data assets.

The platform shall maintain a centralized Metadata Repository.

---

# Metadata Categories

| Category             | Description                |
| -------------------- | -------------------------- |
| Business Metadata    | Business definitions       |
| Technical Metadata   | Database structures        |
| Operational Metadata | ETL execution information  |
| Analytical Metadata  | KPIs and Metrics           |
| Security Metadata    | Access control information |

---

# Metadata Repository Structure

```text
Business Glossary
       |
       |
Data Dictionary
       |
       |
Data Catalog
       |
       |
Lineage Repository
       |
       |
Quality Repository
```

---

# Metadata Attributes

Every table shall contain:

| Attribute         | Description          |
| ----------------- | -------------------- |
| Asset Name        | Data Asset Name      |
| Description       | Business Definition  |
| Owner             | Responsible Area     |
| Steward           | Data Steward         |
| Source System     | Origin               |
| Refresh Frequency | Update Frequency     |
| Security Level    | Classification       |
| Retention Period  | Historical Retention |

---

# 13. Data Catalog

---

## Purpose

Provide discoverability for all analytical assets.

---

## Catalog Structure

### Data Assets

* Tables
* Views
* Materialized Views
* Data Marts
* Reports
* Dashboards
* Machine Learning Models

---

## Example

### Asset Name

Fact_Cost

### Description

Stores project financial performance.

### Owner

Finance Department

### Steward

Analytics Engineer

### Classification

Confidential

### Refresh

Daily

---

# 14. Data Lineage

## Purpose

Track data movement across systems.

---

## End-to-End Lineage

```text
ERP
 |
 |
Primavera
 |
 |
Excel Files
 |
 |
IoT Sources
 |
 |
API Sources
 |
 v

Landing Zone
 |
 |
Raw Layer
 |
 |
ETL Processing
 |
 |
Data Warehouse
 |
 |
Data Mart
 |
 |
Dashboard
 |
 |
Business User
```

---

# Column-Level Lineage Example

Source:

```text
ERP.actual_cost
```

Transformation:

```text
SUM(actual_cost)
GROUP BY project
```

Destination:

```text
Fact_Cost.actual_cost
```

---

# Lineage Tracking Requirements

---

## LIN-001

All ETL jobs
