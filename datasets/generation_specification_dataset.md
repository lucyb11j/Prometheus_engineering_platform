# Dataset Generation Specification

## Prometheus Analytics Platform (PAP)

**Version:** 1.0
**Status:** Approved for Synthetic Data Generation
**Owner:** Analytics Engineering Team

---

# 1. Purpose

This document defines the specifications required to generate realistic synthetic datasets for the Prometheus Analytics Platform (PAP).

The generated datasets must support:

* Data Warehouse Validation
* ETL Pipeline Testing
* Data Quality Testing
* Analytics Engineering Development
* Dashboard Development
* Machine Learning Training
* Portfolio Demonstration

---

# 2. Dataset Inventory

| Dataset         | Records |
| --------------- | ------- |
| projects.csv    | 50      |
| locations.csv   | 20      |
| vendors.csv     | 100     |
| employees.csv   | 250     |
| equipment.csv   | 120     |
| costs.csv       | 10,000  |
| schedule.csv    | 5,000   |
| maintenance.csv | 3,000   |
| risks.csv       | 1,500   |

---

# 3. Business Context

The synthetic data represents a multinational engineering and construction company operating in:

* Infrastructure
* Mining
* Industrial Plants
* Energy Projects

Countries:

```text
Peru
Chile
Colombia
Mexico
Brazil
```

---

# 4. Dataset Specifications

---

# 4.1 locations.csv

## Description

Project locations.

## Record Count

```text
20
```

## Fields

| Field       |
| ----------- |
| location_id |
| country     |
| region      |
| city        |
| site_name   |

---

## Distribution

Country Distribution:

| Country  | Percentage |
| -------- | ---------- |
| Peru     | 40%        |
| Chile    | 20%        |
| Colombia | 15%        |
| Mexico   | 15%        |
| Brazil   | 10%        |

---

# 4.2 projects.csv

## Description

Construction projects.

## Record Count

```text
50
```

## Fields

| Field        |
| ------------ |
| project_id   |
| project_name |
| project_type |
| location_id  |
| status       |
| budget       |
| start_date   |
| end_date     |

---

## Distribution

Project Types:

| Type           | Percentage |
| -------------- | ---------- |
| Infrastructure | 40%        |
| Mining         | 25%        |
| Industrial     | 20%        |
| Energy         | 15%        |

---

## Status Distribution

| Status    | Percentage |
| --------- | ---------- |
| Active    | 60%        |
| Completed | 25%        |
| Delayed   | 15%        |

---

## Budget Distribution

Minimum:

```text
500,000 USD
```

Maximum:

```text
25,000,000 USD
```

Distribution:

```text
Log-Normal
```

---

# 4.3 vendors.csv

## Record Count

```text
100
```

---

## Categories

| Category       | Percentage |
| -------------- | ---------- |
| Materials      | 40%        |
| Equipment      | 20%        |
| Labor Services | 20%        |
| Logistics      | 10%        |
| Consulting     | 10%        |

---

# 4.4 employees.csv

## Record Count

```text
250
```

---

## Departments

| Department   | Percentage |
| ------------ | ---------- |
| Engineering  | 35%        |
| Construction | 25%        |
| Maintenance  | 15%        |
| Finance      | 10%        |
| Procurement  | 10%        |
| Management   | 5%         |

---

## Salary Distribution

Minimum:

```text
800 USD
```

Maximum:

```text
12,000 USD
```

Distribution:

```text
Normal Distribution
```

---

# 4.5 equipment.csv

## Record Count

```text
120
```

---

## Equipment Types

| Type       | Percentage |
| ---------- | ---------- |
| Excavator  | 30%        |
| Crane      | 20%        |
| Dump Truck | 25%        |
| Bulld      |            |
