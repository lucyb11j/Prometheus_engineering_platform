# 08_Data_Model_ERD.md

# Data Model & Enterprise Data Warehouse Design

## Prometheus Analytics Platform (PAP)

### Prometheus Infrastructure Predictive Control Tower

---

# Document Information

| Field             | Value                                         |
| ----------------- | --------------------------------------------- |
| Project           | Prometheus Analytics Platform                 |
| Document Type     | Data Model & ERD                              |
| Version           | 1.0                                           |
| Database          | PostgreSQL                                    |
| Architecture      | Data Warehouse                                |
| Modeling Approach | Dimensional Modeling                          |
| Status            | Approved                                      |

---

# 1. Purpose

This document defines the Enterprise Data Warehouse architecture for the Prometheus Analytics Platform.

The objective is to establish a centralized analytical repository that integrates operational, financial, scheduling, workforce, and equipment data into a unified analytical model.

---

# 2. Data Architecture Overview

```text
ERP Systems
     |
     |
Primavera P6
     |
     |
Excel Sources
     |
     |
IoT Sensors
     |
     |
APIs
     |
     v

+----------------+
|     ETL        |
| Airflow/Python |
+----------------+
        |
        v

+----------------+
| Data Warehouse |
| PostgreSQL     |
+----------------+
        |
        v

+----------------+
| Analytics      |
| Power BI       |
| React          |
| FastAPI        |
+----------------+
```

---

# 3. Data Warehouse Architecture

## Architecture Type

Star Schema

### Advantages

* Fast analytical queries
* Easy reporting
* Simple KPI calculations
* Scalable

---

# 4. Core Business Domains

The warehouse stores information from:

### Project Management

* Projects
* Activities
* Schedules

### Financial Management

* Budgets
* Costs
* Forecasts

### Equipment Management

* Fleet
* Maintenance
* Failures

### Workforce Management

* Employees
* Productivity
* Attendance

### Risk Management

* Risk Events
* Forecasts
* Alerts

---

# 5. Enterprise Data Warehouse Schema

```text
                    Dim_Time
                         |
                         |
                         |
Dim_Project ----- Fact_Project ----- Dim_Location
                         |
                         |
                         |
                    Dim_Status


                    Dim_Time
                         |
                         |
                         |
Dim_Project ----- Fact_Cost ----- Dim_Cost_Category
                         |
                         |
                         |
                    Dim_Vendor


                    Dim_Time
                         |
                         |
                         |
Dim_Equipment --- Fact_Equipment --- Dim_Maintenance
                         |
                         |
                         |
                    Dim_Location


                    Dim_Time
                         |
                         |
                         |
Dim_Employee ---- Fact_Productivity ---- Dim_Project
```

---

# 6. Dimension Tables

---

# 6.1 Dim_Time

## Description

Stores calendar information.

---

## Attributes

| Column  | Type    |
| ------- | ------- |
| time_id | PK      |
| date    | DATE    |
| day     | INTEGER |
| month   | INTEGER |
| quarter | INTEGER |
| year    | INTEGER |
| week    | INTEGER |
| weekday | VARCHAR |

---

# 6.2 Dim_Project

## Description

Stores project information.

---

## Attributes

| Column       | Type    |
| ------------ | ------- |
| project_id   | PK      |
| project_code | VARCHAR |
| project_name | VARCHAR |
| project_type | VARCHAR |
| start_date   | DATE    |
| end_date     | DATE    |
| budget       | NUMERIC |
| location_id  | FK      |
| status_id    | FK      |

---

# 6.3 Dim_Location

## Description

Stores geographical information.

---

## Attributes

| Column      | Type    |
| ----------- | ------- |
| location_id | PK      |
| country     | VARCHAR |
| region      | VARCHAR |
| city        | VARCHAR |
| site_name   | VARCHAR |

---

# 6.4 Dim_Status

## Description

Stores project status information.

---

## Attributes

| Column      | Type    |
| ----------- | ------- |
| status_id   | PK      |
| status_name | VARCHAR |

Values:

* On Track
* Warning
* Critical
* Completed

---

# 6.5 Dim_Cost_Category

## Description

Stores cost categories.

---

## Attributes

| Column        | Type    |
| ------------- | ------- |
| category_id   | PK      |
| category_name | VARCHAR |

Examples:

* Labor
* Materials
* Equipment
* Subcontractors
* Logistics

---

# 6.6 Dim_Vendor

## Description

Suppliers and contractors.

---

## Attributes

| Column      | Type    |
| ----------- | ------- |
| vendor_id   | PK      |
| vendor_name | VARCHAR |
| vendor_type | VARCHAR |

---

# 6.7 Dim_Equipment

## Description

Equipment information.

---

## Attributes

| Column           | Type    |
| ---------------- | ------- |
| equipment_id     | PK      |
| equipment_code   | VARCHAR |
| equipment_name   | VARCHAR |
| equipment_type   | VARCHAR |
| manufacturer     | VARCHAR |
| acquisition_date | DATE    |

---

# 6.8 Dim_Maintenance

## Description

Maintenance classifications.

---

## Attributes

| Column           | Type    |
| ---------------- | ------- |
| maintenance_id   | PK      |
| maintenance_type | VARCHAR |

Values:

* Preventive
* Corrective
* Predictive

---

# 6.9 Dim_Employee

## Description

Employee master data.

---

## Attributes

| Column        | Type    |
| ------------- | ------- |
| employee_id   | PK      |
| employee_code | VARCHAR |
| full_name     | VARCHAR |
| position      | VARCHAR |
| department    | VARCHAR |

---

# 7. Fact Tables

---

# 7.1 Fact_Project

## Description

Stores project execution metrics.

---

## Grain

One record per project per day.

---

## Measures

| Column             |
| ------------------ |
| planned_progress   |
| actual_progress    |
| spi                |
| schedule_variance  |
| project_risk_score |

---

## Foreign Keys

| FK          |
| ----------- |
| project_id  |
| time_id     |
| location_id |
| status_id   |

---

# 7.2 Fact_Cost

## Description

Stores financial metrics.

---

## Grain

One project per day per cost category.

---

## Measures

| Column        |
| ------------- |
| budget_cost   |
| actual_cost   |
| earned_value  |
| planned_value |
| cost_variance |
| cpi           |
| forecast_cost |

---

## Foreign Keys

| FK          |
| ----------- |
| project_id  |
| time_id     |
| category_id |
| vendor_id   |

---

# 7.3 Fact_Equipment

## Description

Stores equipment performance.

---

## Grain

One equipment per day.

---

## Measures

| Column           |
| ---------------- |
| operating_hours  |
| downtime_hours   |
| availability     |
| utilization      |
| mtbf             |
| mttr             |
| maintenance_cost |

---

## Foreign Keys

| FK             |
| -------------- |
| equipment_id   |
| time_id        |
| location_id    |
| maintenance_id |

---

# 7.4 Fact_Productivity

## Description

Stores workforce productivity.

---

## Grain

One employee per day.

---

## Measures

| Column             |
| ------------------ |
| hours_worked       |
| productive_hours   |
| productivity_index |
| labor_cost         |

---

## Foreign Keys

| FK          |
| ----------- |
| employee_id |
| project_id  |
| time_id     |

---

# 7.5 Fact_Risk

## Description

Stores project risk indicators.

---

## Measures

| Column          |
| --------------- |
| risk_score      |
| probability     |
| impact          |
| mitigation_cost |
| risk_level      |

---

## Foreign Keys

| FK         |
| ---------- |
| project_id |
| time_id    |

---

# 7.6 Fact_Forecast

## Description

Stores ML predictions.

---

## Measures

| Column              |
| ------------------- |
| predicted_cost      |
| predicted_delay     |
| confidence_interval |
| anomaly_score       |

---

## Foreign Keys

| FK         |
| ---------- |
| project_id |
| time_id    |

---

# 8. Enterprise KPIs

---

# Cost KPIs

| KPI           | Formula   |
| ------------- | --------- |
| CPI           | EV / AC   |
| Cost Variance | EV - AC   |
| Forecast Cost | BAC / CPI |

---

# Schedule KPIs

| KPI               | Formula |
| ----------------- | ------- |
| SPI               | EV / PV |
| Schedule Variance | EV - PV |

---

# Equipment KPIs

| KPI          | Formula                        |
| ------------ | ------------------------------ |
| Availability | Operating Time / Total Time    |
| Utilization  | Used Time / Available Time     |
| MTBF         | Total Running Hours / Failures |
| MTTR         | Repair Hours / Repairs         |

---

# Workforce KPIs

| KPI                | Formula                        |
| ------------------ | ------------------------------ |
| Productivity Index | Productive Hours / Total Hours |
| Labor Cost         | Hours × Rate                   |

---

# 9. Data Mart Layer

Specialized Data Marts:

### Executive Data Mart

* Portfolio KPIs
* Risks
* Forecasts

---

### Project Data Mart

* Progress
* Schedule
* Costs

---

### Equipment Data Mart

* Availability
* Failures
* Maintenance

---

### Workforce Data Mart

* Productivity
* Attendance
* Labor Cost

---

# 10. Data Quality Rules

---

## DQ-01

Project code must be unique.

---

## DQ-02

Budget values cannot be negative.

---

## DQ-03

Dates must be valid.

---

## DQ-04

Foreign keys must exist.

---

## DQ-05

Project progress must be between:

0 and 100%

---

# 11. Slowly Changing Dimensions

## SCD Type 2

Applied to:

* Employee
* Project
* Equipment
* Vendor

Historical changes shall be preserved.

---

# 12. Partitioning Strategy

Fact tables shall be partitioned by:

* Year
* Month

Benefits:

* Faster queries
* Easier maintenance

---

# 13. Indexing Strategy

Indexes shall be created on:

* project_id
* equipment_id
* employee_id
* time_id
* location_id

---

# 14. Future Expansion

Future versions shall include:

* IoT Telemetry Fact Tables
* Digital Twin Data Mart
* GIS Spatial Analytics
* BIM Integration
* Carbon Footprint Analytics

---

# 15. Complete Enterprise ERD

```text
Dim_Time
   |
   +------------------+
   |                  |
Fact_Project      Fact_Cost
   |                  |
Dim_Project------Dim_Cost_Category
   |
Fact_Risk
   |
Fact_Forecast

Dim_Equipment
      |
Fact_Equipment
      |
Dim_Maintenance

Dim_Employee
      |
Fact_Productivity
      |
Dim_Project
```

---

# 16. Traceability Matrix

| Business Area     | Fact Table        |
| ----------------- | ----------------- |
| Project Control   | Fact_Project      |
| Financial Control | Fact_Cost         |
| Maintenance       | Fact_Equipment    |
| Workforce         | Fact_Productivity |
| Risk Management   | Fact_Risk         |
| Forecasting       | Fact_Forecast     |

---

# End of Data Model & ERD Specification
