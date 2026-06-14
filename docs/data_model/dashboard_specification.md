# Dashboard Specification

## Prometheus Analytics Platform (PAP)

**Version:** 1.0
**Status:** Approved
**Platform:** Power BI
**Source:** dbt Analytics Marts
**Owner:** Business Intelligence Team

---

# 1. Purpose

This document defines all analytical dashboards that will be developed using Power BI.

The dashboards provide visibility into:

* Project Performance
* Cost Control
* Workforce Productivity
* Equipment Maintenance
* Risk Management
* Executive KPIs

---

# 2. Dashboard Architecture

```text
PostgreSQL
     ↓
Curated Layer
     ↓
dbt Marts
     ↓
Power BI Dataset
     ↓
Dashboards
     ↓
Business Users
```

---

# 3. Dashboard Portfolio

| Dashboard                       | Data Mart                  |
| ------------------------------- | -------------------------- |
| Executive Dashboard             | mart_executive_dashboard   |
| Project Performance Dashboard   | mart_project_performance   |
| Cost Management Dashboard       | mart_cost_management       |
| Maintenance Analytics Dashboard | mart_maintenance_analytics |
| Risk Monitoring Dashboard       | mart_risk_monitoring       |
| Workforce Analytics Dashboard   | mart_workforce_analytics   |

---

# 4. Executive Dashboard

## Purpose

Provide executives with a consolidated view of organizational performance.

---

## Users

```text
CEO

COO

Finance Director

Operations Director

Project Sponsors
```

---

## KPIs

| KPI                |
| ------------------ |
| Total Projects     |
| Total Budget       |
| Total Actual Cost  |
| Cost Variance      |
| Average CPI        |
| Average SPI        |
| Average Risk Score |
| Delayed Projects   |
| Projects On Budget |

---

## Visualizations

### KPI Cards

```text
Total Projects

Total Budget

Total Cost

Average CPI

Average SPI
```

---

### Budget vs Actual Cost

```text
Clustered Column Chart
```

X-Axis:

```text
Project
```

Y-Axis:

```text
Budget

Actual Cost
```

---

### CPI Trend

```text
Line Chart
```

---

### Risk Distribution

```text
Donut Chart
```

---

### Project Status

```text
Stacked Bar Chart
```

---

## Filters

```text
Project

Project Type

Status

Date

Region
```

---

# 5. Project Performance Dashboard

## Purpose

Monitor project execution and schedule adherence.

---

## Users

```text
PMO

Project Managers

Program Managers
```

---

## KPIs

| KPI                   |
| --------------------- |
| SPI                   |
| Schedule Variance     |
| Completion Percentage |
| Delayed Projects      |
| Planned Progress      |
| Actual Progress       |

---

## Visualizations

### Progress Comparison

```text
Line Chart
```

---

### SPI by Project

```text
Bar Chart
```

---

### Completion Heatmap

```text
Matrix Visual
```

---

### Schedule Variance

```text
Waterfall Chart
```

---

## Filters

```text
Project

Date

Project Manager

Project Type
```

---

# 6. Cost Management Dashboard

## Purpose

Control project financial performance.

---

## Users

```text
Finance Team

Controllers

PMO

Executives
```

---

## KPIs

| KPI                |
| ------------------ |
| Actual Cost        |
| Planned Cost       |
| Cost Variance      |
| CPI                |
| Vendor Spend       |
| Budget Utilization |

---

## Visualizations

### Cost Trend

```text
Line Chart
```

---

### Vendor Spend Ranking

```text
Horizontal Bar Chart
```

---

### Budget Utilization

```text
Gauge Chart
```

---

### Cost Variance Analysis

```text
Waterfall Chart
```

---

## Filters

```text
Project

Vendor

Date

Region
```

---

# 7. Maintenance Analytics Dashboard

## Purpose

Analyze equipment maintenance and reliability.

---

## Users

```text
Maintenance Managers

Operations Team

Asset Managers
```

---

## KPIs

| KPI              |
| ---------------- |
| MTTR             |
| MTBF             |
| Downtime Hours   |
| Maintenance Cost |
| Availability     |
| Failure Rate     |

---

## Visualizations

### MTTR Trend

```text
Line Chart
```

---

### MTBF Trend

```text
Line Chart
```

---

### Downtime by Equipment

```text
Bar Chart
```

---

### Maintenance Cost Breakdown

```text
Treemap
```

---

### Equipment Availability

```text
Gauge Chart
```

---

## Filters

```text
Equipment

Project

Date

Equipment Type
```

---

# 8. Risk Monitoring Dashboard

## Purpose

Monitor risk exposure across projects.

---

## Users

```text
Risk Managers

Project Managers

Executives
```

---

## KPIs

| KPI                |
| ------------------ |
| Average Risk Score |
| High Risk Count    |
| Financial Exposure |
| Schedule Exposure  |
| Critical Risks     |

---

## Visualizations

### Risk Heat Map

```text
Matrix
```

Probability:

```text
Rows
```

Severity:

```text
Columns
```

---

### Risk Trend

```text
Line Chart
```

---

### Financial Exposure

```text
Column Chart
```

---

### Risk Categories

```text
Donut Chart
```

---

## Filters

```text
Project

Risk Category

Date

Severity
```

---

# 9. Workforce Analytics Dashboard

## Purpose

Analyze workforce utilization and productivity.

---

## Users

```text
Human Resources

Operations

Project Managers
```

---

## KPIs

| KPI                |
| ------------------ |
| Hours Worked       |
| Overtime Hours     |
| Labor Cost         |
| Productivity Score |
| Utilization Rate   |

---

## Visualizations

### Productivity by Department

```text
Bar Chart
```

---

### Labor Cost Trend

```text
Line Chart
```

---

### Overtime Analysis

```text
Stacked Column Chart
```

---

### Employee Utilization

```text
Gauge Chart
```

---

### Workforce Allocation

```text
Treemap
```

---

## Filters

```text
Department

Role

Project

Date
```

---

# 10. Drill-Through Requirements

All dashboards must support:

```text
Executive
    ↓
Project
    ↓
Detail
```

---

Example:

```text
Executive Dashboard
     ↓
Project Performance Dashboard
     ↓
Project Detail Page
```

---

# 11. Global Filters

Available in all dashboards:

```text
Date

Project

Region

Project Type

Status
```

---

# 12. Refresh Strategy

Data Source:

```text
PostgreSQL
```

Refresh Type:

```text
Scheduled Refresh
```

Frequency:

```text
Daily
```

Recommended:

```text
06:00 AM
```

---

# 13. Security Model

Role-Based Access Control

---

## Executive Role

Access:

```text
All Dashboards
```

---

## Project Manager Role

Access:

```text
Projects

Costs

Risks
```

---

## Maintenance Role

Access:

```text
Maintenance Dashboard
```

---

## HR Role

Access:

```text
Workforce Dashboard
```

---

# 14. Dashboard Performance Targets

| Metric          | Target   |
| --------------- | -------- |
| Initial Load    | < 5 sec  |
| Filter Response | < 2 sec  |
| Drill Through   | < 3 sec  |
| Dataset Refresh | < 15 min |

---

# 15. Acceptance Criteria

```text
✓ Dashboards Connected

✓ KPIs Validated

✓ Drill-Through Working

✓ Security Implemented

✓ Refresh Operational

✓ Performance Targets Met

✓ User Acceptance Completed
```

---

# 16. Future Dashboards

Planned Extensions:

```text
Predictive Maintenance Dashboard

Project Forecast Dashboard

Procurement Analytics Dashboard

Contract Analytics Dashboard

Safety Analytics Dashboard

Machine Learning Insights Dashboard
```

---

# End of Document
