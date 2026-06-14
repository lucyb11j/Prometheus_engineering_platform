# Marts Specification

## Prometheus Analytics Platform (PAP)

**Version:** 1.0
**Status:** Approved
**Owner:** Analytics Engineering Team
**Technology:** dbt + PostgreSQL
**Source Layer:** Curated
**Target Layer:** Analytics Marts

---

# 1. Purpose

This document defines the Business Data Marts that will be built from the Curated Layer.

The objective is to create subject-oriented analytical models optimized for:

* Executive Reporting
* Power BI Dashboards
* KPI Monitoring
* Forecasting
* Data Science
* Self-Service Analytics

---

# 2. Architecture

```text
RAW
 ↓
TRUSTED
 ↓
CURATED
 ↓
DBT MARTS
 ↓
POWER BI
 ↓
BUSINESS USERS
```

---

# 3. Design Principles

All marts must:

* Be business-oriented
* Be read-only
* Be denormalized when beneficial
* Contain calculated KPIs
* Support historical analysis
* Be optimized for dashboard consumption

---

# 4. Data Mart Inventory

| Mart                       | Purpose                         |
| -------------------------- | ------------------------------- |
| mart_executive_dashboard   | Executive KPIs                  |
| mart_project_performance   | Project performance monitoring  |
| mart_cost_management       | Cost control and budgeting      |
| mart_maintenance_analytics | Asset maintenance analytics     |
| mart_risk_monitoring       | Risk exposure analysis          |
| mart_workforce_analytics   | Workforce productivity analysis |

---

# 5. MART_EXECUTIVE_DASHBOARD

## Purpose

Provide a consolidated executive view of all projects.

---

## Business Users

```text
CEO

Project Sponsor

Operations Director

Finance Director
```

---

## Source Tables

```text
fact_cost

fact_schedule

fact_risk

dim_project
```

---

## KPIs

```text
Total Projects

Total Budget

Total Actual Cost

Cost Variance

Average CPI

Average SPI

Average Risk Score

Projects Delayed

Projects On Budget
```

---

## Grain

```text
One row per project
```

---

## Output Columns

| Column         |
| -------------- |
| project_name   |
| project_type   |
| status         |
| total_budget   |
| actual_cost    |
| cost_variance  |
| avg_cpi        |
| avg_spi        |
| avg_risk_score |

---

# 6. MART_PROJECT_PERFORMANCE

## Purpose

Monitor schedule and project execution.

---

## Business Users

```text
PMO

Project Managers

Program Managers
```

---

## Source Tables

```text
fact_schedule

dim_project

dim_date
```

---

## KPIs

```text
Schedule Variance

SPI

Completion %

Project Status

Forecast Finish Date
```

---

## Grain

```text
One project
per reporting period
```

---

## Output Columns

| Column            |
| ----------------- |
| project_name      |
| report_date       |
| planned_progress  |
| actual_progress   |
| schedule_variance |
| spi               |

---

# 7. MART_COST_MANAGEMENT

## Purpose

Financial monitoring and budget control.

---

## Business Users

```text
Finance

PMO

Executives
```

---

## Source Tables

```text
fact_cost

dim_project

dim_vendor

dim_date
```

---

## KPIs

```text
Budget Utilization

Actual Cost

Planned Cost

Cost Variance

Cost Performance Index (CPI)

Vendor Spend
```

---

## Grain

```text
One project
per reporting period
```

---

## Output Columns

| Column        |
| ------------- |
| project_name  |
| vendor_name   |
| report_date   |
| planned_cost  |
| actual_cost   |
| cost_variance |
| earned_value  |
| cpi           |

---

# 8. MART_MAINTENANCE_ANALYTICS

## Purpose

Equipment maintenance monitoring.

---

## Business Users

```text
Maintenance Managers

Asset Management

Operations
```

---

## Source Tables

```text
fact_maintenance

dim_equipment

dim_project

dim_date
```

---

## KPIs

```text
Maintenance Cost

Downtime Hours

MTTR

MTBF

Equipment Availability

Failure Rate
```

---

## Grain

```text
One maintenance event
```

---

## Output Columns

| Column                |
| --------------------- |
| equipment_name        |
| equipment_type        |
| project_name          |
| downtime_hours        |
| maintenance_cost      |
| repair_duration_hours |

---

# 9. MART_RISK_MONITORING

## Purpose

Risk exposure and mitigation monitoring.

---

## Business Users

```text
Risk Managers

Project Managers

Executives
```

---

## Source Tables

```text
fact_risk

dim_risk

dim_project

dim_date
```

---

## KPIs

```text
Average Risk Score

High Risk Count

Financial Exposure

Schedule Exposure

Risk Trend
```

---

## Grain

```text
One risk
per project
per reporting date
```

---

## Output Columns

| Column        |
| ------------- |
| project_name  |
| risk_category |
| severity      |
| probability   |
| risk_score    |
| impact_cost   |
| impact_days   |

---

# 10. MART_WORKFORCE_ANALYTICS

## Purpose

Workforce productivity and labor utilization.

---

## Business Users

```text
Human Resources

Operations

Project Managers
```

---

## Source Tables

```text
fact_workforce

dim_employee

dim_project

dim_date
```

---

## KPIs

```text
Hours Worked

Overtime Hours

Labor Cost

Productivity Score

Utilization Rate

Employee Allocation
```

---

## Grain

```text
One employee
per project
per reporting date
```

---

## Output Columns

| Column             |
| ------------------ |
| employee_name      |
| department         |
| role               |
| project_name       |
| hours_worked       |
| overtime_hours     |
| labor_cost         |
| productivity_score |

---

# 11. Common Business Rules

---

## Budget Rule

```text
Budget > 0
```

---

## CPI Rule

```text
CPI =
Earned Value
/
Actual Cost
```

---

## SPI Rule

```text
SPI =
Actual Progress
/
Planned Progress
```

---

## Risk Score Rule

```text
Risk Score =
Probability × Severity
```

---

# 12. dbt Model Structure

```text
models/

├── staging/

├── marts/

│   ├── executive/
│   │   └── mart_executive_dashboard.sql
│
│   ├── projects/
│   │   └── mart_project_performance.sql
│
│   ├── finance/
│   │   └── mart_cost_management.sql
│
│   ├── maintenance/
│   │   └── mart_maintenance_analytics.sql
│
│   ├── workforce/
│   │   └── mart_workforce_analytics.sql
│
│   └── risks/
│       └── mart_risk_monitoring.sql
```

---

# 13. dbt Tests

Each mart must include:

```text
not_null

unique

relationships

accepted_values
```

---

# 14. Refresh Strategy

Refresh Type:

```text
Incremental
```

Frequency:

```text
Daily
```

Execution:

```bash
dbt run
```

---

# 15. Documentation Requirements

Generate automatically using:

```bash
dbt docs generate
```

Serve:

```bash
dbt docs serve
```

Documentation must include:

```text
Column Definitions

Lineage Graph

Data Quality Tests

Dependencies

Business Definitions
```

---

# 16. Power BI Mapping

| Dashboard             | Data Mart                  |
| --------------------- | -------------------------- |
| Executive Dashboard   | mart_executive_dashboard   |
| Project Dashboard     | mart_project_performance   |
| Cost Dashboard        | mart_cost_management       |
| Maintenance Dashboard | mart_maintenance_analytics |
| Risk Dashboard        | mart_risk_monitoring       |
| Workforce Dashboard   | mart_workforce_analytics   |

---

# 17. Future Marts

Planned:

```text
mart_contract_analytics

mart_procurement_analytics

mart_weather_impact

mart_safety_incidents

mart_predictive_maintenance

mart_project_forecasting
```

---

# 18. Acceptance Criteria

```text
✓ All marts created

✓ dbt tests passing

✓ Documentation generated

✓ Lineage validated

✓ Power BI connected

✓ KPIs validated

✓ Executive dashboards operational
```

---

# End of Document
