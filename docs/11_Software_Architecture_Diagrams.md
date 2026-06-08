# Software Architecture Diagrams Specification

## Prometheus Analytics Platform (pAP)

### Prometheus Analytics Platform

---

# Document Information

| Field         | Value                                                     |
| ------------- | --------------------------------------------------------- |
| Project       | Prometheus Analytics Platform             |
| Document Type | Software Architecture Diagrams                            |
| Version       | 1.0                                                       |
| Status        | Approved                                                  |
| Notation      | UML 2.5, C4 Model, Mermaid                                |
| Audience      | Architects, Developers, Analytics Engineers, Stakeholders |

---

# 1. Purpose

This document contains the architectural diagrams required to understand, develop, deploy, maintain, and scale the Engineering Infrastructure Analytics Platform.

The diagrams follow:

* UML 2.5
* C4 Model
* Enterprise Architecture Practices
* Microservice-ready Design
* Cloud Native Principles

---

# 2. System Context Diagram (C4 Level 1)

## Objective

Show the platform and external systems.

```mermaid
flowchart LR

    User[Executive User]
    PM[Project Director]
    MM[Maintenance Manager]
    DA[Data Analyst]

    EIAP[Engineering Infrastructure Analytics Platform]

    ERP[ERP System]
    P6[Primavera P6]
    HR[HR System]
    IOT[IoT Sensors]
    EMAIL[Email Service]

    User --> EIAP
    PM --> EIAP
    MM --> EIAP
    DA --> EIAP

    ERP --> EIAP
    P6 --> EIAP
    HR --> EIAP
    IOT --> EIAP

    EIAP --> EMAIL
```

---

# 3. Container Diagram (C4 Level 2)

## Objective

Show major containers.

```mermaid
flowchart TB

    Browser[React Frontend]

    API[FastAPI Backend]

    DW[(PostgreSQL DW)]

    AIRFLOW[Apache Airflow]

    REDIS[(Redis Cache)]

    STORAGE[(Object Storage)]

    MONITOR[Monitoring Stack]

    Browser --> API

    API --> DW

    API --> REDIS

    AIRFLOW --> DW

    AIRFLOW --> STORAGE

    API --> STORAGE

    API --> MONITOR
```

---

# 4. Component Diagram

## Backend Components

```mermaid
flowchart TB

    API[REST API]

    AUTH[Authentication Module]

    USERS[User Management]

    PROJECTS[Project Analytics]

    COSTS[Cost Analytics]

    EQUIPMENT[Equipment Analytics]

    FORECAST[Forecast Engine]

    REPORTS[Reporting Engine]

    ALERTS[Alert Engine]

    REPO[Repository Layer]

    API --> AUTH
    API --> USERS
    API --> PROJECTS
    API --> COSTS
    API --> EQUIPMENT
    API --> FORECAST
    API --> REPORTS
    API --> ALERTS

    PROJECTS --> REPO
    COSTS --> REPO
    EQUIPMENT --> REPO
    FORECAST --> REPO
```

---

# 5. Layered Architecture Diagram

```mermaid
flowchart TB

    UI[Presentation Layer]

    API[API Layer]

    DOMAIN[Domain Layer]

    APP[Application Layer]

    DATA[Data Layer]

    DB[(PostgreSQL)]

    UI --> API

    API --> APP

    APP --> DOMAIN

    DOMAIN --> DATA

    DATA --> DB
```

---

# 6. Domain Driven Design Diagram

```mermaid
flowchart LR

    PROJECTS[Project Domain]

    FINANCE[Financial Domain]

    EQUIPMENT[Equipment Domain]

    WORKFORCE[Workforce Domain]

    RISK[Risk Domain]

    FORECAST[Forecast Domain]

    PROJECTS --- FINANCE

    PROJECTS --- EQUIPMENT

    PROJECTS --- WORKFORCE

    PROJECTS --- RISK

    RISK --- FORECAST
```

---

# 7. Deployment Diagram

## Development Environment

```mermaid
flowchart TB

    DEV[Developer Laptop]

    FRONT[React Container]

    BACK[FastAPI Container]

    DB[(PostgreSQL)]

    AIRFLOW[Airflow]

    DEV --> FRONT

    FRONT --> BACK

    BACK --> DB

    AIRFLOW --> DB
```

---

## Production Environment

```mermaid
flowchart TB

    LB[Load Balancer]

    FRONT[Frontend Pods]

    API[Backend Pods]

    DB[(PostgreSQL Cluster)]

    CACHE[(Redis)]

    AIRFLOW[Airflow Cluster]

    MONITOR[Prometheus + Grafana]

    LB --> FRONT

    FRONT --> API

    API --> DB

    API --> CACHE

    AIRFLOW --> DB

    API --> MONITOR
```

---

# 8. Data Flow Diagram

```mermaid
flowchart LR

    ERP[ERP]

    P6[Primavera]

    EXCEL[Excel Files]

    IOT[IoT Sensors]

    ETL[ETL Pipelines]

    DW[(Data Warehouse)]

    MART[Data Marts]

    DASH[Dashboards]

    ERP --> ETL

    P6 --> ETL

    EXCEL --> ETL

    IOT --> ETL

    ETL --> DW

    DW --> MART

    MART --> DASH
```

---

# 9. ETL Process Diagram

```mermaid
flowchart LR

    EXTRACT[Extract]

    VALIDATE[Validate]

    TRANSFORM[Transform]

    LOAD[Load]

    MONITOR[Monitor]

    EXTRACT --> VALIDATE

    VALIDATE --> TRANSFORM

    TRANSFORM --> LOAD

    LOAD --> MONITOR
```

---

# 10. Data Warehouse Architecture Diagram

```mermaid
flowchart TB

    RAW[Raw Layer]

    STAGING[Staging Layer]

    WAREHOUSE[Data Warehouse]

    MARTS[Data Marts]

    BI[BI Tools]

    RAW --> STAGING

    STAGING --> WAREHOUSE

    WAREHOUSE --> MARTS

    MARTS --> BI
```

---

# 11. Star Schema Diagram

```mermaid
flowchart TB

    FACT[Fact_Cost]

    TIME[Dim_Time]

    PROJECT[Dim_Project]

    CATEGORY[Dim_Cost_Category]

    VENDOR[Dim_Vendor]

    TIME --> FACT

    PROJECT --> FACT

    CATEGORY --> FACT

    VENDOR --> FACT
```

---

# 12. Authentication Sequence Diagram

```mermaid
sequenceDiagram

    actor User

    participant Frontend

    participant API

    participant Database

    User->>Frontend: Login

    Frontend->>API: Credentials

    API->>Database: Validate User

    Database-->>API: User Found

    API-->>Frontend: JWT Token

    Frontend-->>User: Access Granted
```

---

# 13. Forecast Execution Sequence Diagram

```mermaid
sequenceDiagram

    participant User

    participant Frontend

    participant API

    participant ForecastEngine

    participant Database

    User->>Frontend: Request Forecast

    Frontend->>API: Forecast Request

    API->>ForecastEngine: Execute Model

    ForecastEngine->>Database: Load Data

    Database-->>ForecastEngine: Dataset

    ForecastEngine-->>API: Prediction

    API-->>Frontend: Forecast Result
```

---

# 14. Alert Generation Sequence Diagram

```mermaid
sequenceDiagram

    participant ETL

    participant Analytics

    participant AlertEngine

    participant Email

    ETL->>Analytics: New Data

    Analytics->>AlertEngine: Risk Detected

    AlertEngine->>Email: Send Alert

    Email-->>AlertEngine: Delivered
```

---

# 15. State Machine Diagram

## Project Lifecycle

```mermaid
stateDiagram-v2

    [*] --> Planned

    Planned --> Active

    Active --> Delayed

    Active --> Completed

    Delayed --> Active

    Delayed --> Cancelled

    Completed --> [*]

    Cancelled --> [*]
```

---

# 16. Equipment State Machine

```mermaid
stateDiagram-v2

    [*] --> Operational

    Operational --> Maintenance

    Maintenance --> Operational

    Operational --> Failure

    Failure --> Repair

    Repair --> Operational
```

---

# 17. Future Microservice Extraction Diagram

## Evolution Roadmap

```mermaid
flowchart LR

    MONOLITH[Modular Monolith]

    FORECAST[Forecast Service]

    ALERT[Alert Service]

    REPORT[Reporting Service]

    KAFKA[Kafka Event Bus]

    MONOLITH --> FORECAST

    MONOLITH --> ALERT

    MONOLITH --> REPORT

    FORECAST --> KAFKA

    ALERT --> KAFKA

    REPORT --> KAFKA
```

---

# 18. Event Driven Architecture Diagram

```mermaid
flowchart LR

    COST[Cost Module]

    PROJECT[Project Module]

    FORECAST[Forecast Module]

    KAFKA[Kafka]

    ALERT[Alert Module]

    REPORT[Reporting Module]

    COST --> KAFKA

    PROJECT --> KAFKA

    FORECAST --> KAFKA

    KAFKA --> ALERT

    KAFKA --> REPORT
```

---

# 19. Monitoring Architecture Diagram

```mermaid
flowchart TB

    APP[Application]

    PROM[Prometheus]

    GRAF[Grafana]

    LOKI[Loki]

    OTEL[OpenTelemetry]

    APP --> OTEL

    OTEL --> PROM

    OTEL --> LOKI

    PROM --> GRAF
```

---

# 20. Infrastructure Roadmap

## Phase 1

```text
Docker Compose
React
FastAPI
PostgreSQL
Airflow
```

## Phase 2

```text
Redis
Object Storage
Grafana
Prometheus
```

## Phase 3

```text
Kafka
Forecast Service
Alert Service
```

## Phase 4

```text
Kubernetes
Service Mesh
Autoscaling
```

## Phase 5

```text
Digital Twin
IoT Streaming
AI Copilot
```

---

# 21. Architecture Validation Checklist

| Requirement                | Covered |
| -------------------------- | ------- |
| Scalability                | Yes     |
| Modularity                 | Yes     |
| Cloud Ready                | Yes     |
| Docker Ready               | Yes     |
| Kubernetes Ready           | Yes     |
| Event Driven Ready         | Yes     |
| Data Warehouse Ready       | Yes     |
| MLOps Ready                | Yes     |
| Analytics Ready            | Yes     |
| Future Microservices Ready | Yes     |

---
