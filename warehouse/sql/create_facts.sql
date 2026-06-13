-- ============================================================================
-- FACT TABLES — curated schema
-- Prometheus Analytics Platform (EIAP)
-- Based on Physical Data Model v1.0
-- ============================================================================

-- Grain: One project cost transaction per day
CREATE TABLE curated.fact_cost (
    cost_key BIGSERIAL NOT NULL,
    date_key INTEGER NOT NULL,
    project_key BIGINT NOT NULL,
    vendor_key BIGINT,
    planned_cost NUMERIC(18, 2),
    actual_cost NUMERIC(18, 2),
    forecast_cost NUMERIC(18, 2),
    CONSTRAINT pk_fact_cost PRIMARY KEY (date_key, cost_key),
    CONSTRAINT fk_fact_cost_date FOREIGN KEY (date_key) REFERENCES curated.dim_date (date_key),
    CONSTRAINT fk_fact_cost_project FOREIGN KEY (project_key) REFERENCES curated.dim_project (project_key),
    CONSTRAINT fk_fact_cost_vendor FOREIGN KEY (vendor_key) REFERENCES curated.dim_vendor (vendor_key)
)
PARTITION BY
    RANGE (date_key);

CREATE INDEX idx_fact_cost_date ON curated.fact_cost (date_key);

CREATE INDEX idx_fact_cost_project ON curated.fact_cost (project_key);

COMMENT ON TABLE curated.fact_cost IS 'Project cost fact — daily grain, partitioned by date_key';

CREATE TABLE curated.fact_cost_2024 PARTITION OF curated.fact_cost FOR VALUES FROM (20240101) TO (20250101);
CREATE TABLE curated.fact_cost_2025 PARTITION OF curated.fact_cost FOR VALUES FROM (20250101) TO (20260101);
CREATE TABLE curated.fact_cost_2026 PARTITION OF curated.fact_cost FOR VALUES FROM (20260101) TO (20270101);
CREATE TABLE curated.fact_cost_default PARTITION OF curated.fact_cost DEFAULT;

-- ============================================================================
-- Grain: One project progress record per reporting day
CREATE TABLE curated.fact_schedule (
    schedule_key BIGSERIAL NOT NULL,
    date_key INTEGER NOT NULL,
    project_key BIGINT NOT NULL,
    planned_progress NUMERIC(8, 2),
    actual_progress NUMERIC(8, 2),
    spi NUMERIC(8, 4),
    CONSTRAINT pk_fact_schedule PRIMARY KEY (date_key, schedule_key),
    CONSTRAINT fk_fact_schedule_date FOREIGN KEY (date_key) REFERENCES curated.dim_date (date_key),
    CONSTRAINT fk_fact_schedule_project FOREIGN KEY (project_key) REFERENCES curated.dim_project (project_key)
)
PARTITION BY
    RANGE (date_key);

CREATE INDEX idx_fact_schedule_date ON curated.fact_schedule (date_key);

CREATE INDEX idx_fact_schedule_project ON curated.fact_schedule (project_key);

COMMENT ON TABLE curated.fact_schedule IS 'Schedule progress fact — daily grain, partitioned by date_key';

CREATE TABLE curated.fact_schedule_2024 PARTITION OF curated.fact_schedule FOR VALUES FROM (20240101) TO (20250101);
CREATE TABLE curated.fact_schedule_2025 PARTITION OF curated.fact_schedule FOR VALUES FROM (20250101) TO (20260101);
CREATE TABLE curated.fact_schedule_2026 PARTITION OF curated.fact_schedule FOR VALUES FROM (20260101) TO (20270101);
CREATE TABLE curated.fact_schedule_default PARTITION OF curated.fact_schedule DEFAULT;

-- ============================================================================
-- Grain: One maintenance event
CREATE TABLE curated.fact_maintenance (
    maintenance_key BIGSERIAL NOT NULL,
    date_key INTEGER NOT NULL,
    equipment_key BIGINT NOT NULL,
    maintenance_type VARCHAR(100),
    downtime_hours NUMERIC(10, 2),
    maintenance_cost NUMERIC(18, 2),
    CONSTRAINT pk_fact_maintenance PRIMARY KEY (date_key, maintenance_key),
    CONSTRAINT fk_fact_maintenance_date FOREIGN KEY (date_key) REFERENCES curated.dim_date (date_key),
    CONSTRAINT fk_fact_maintenance_equipment FOREIGN KEY (equipment_key) REFERENCES curated.dim_equipment (equipment_key)
)
PARTITION BY
    RANGE (date_key);

CREATE INDEX idx_fact_maintenance_date ON curated.fact_maintenance (date_key);

CREATE INDEX idx_fact_maintenance_equipment ON curated.fact_maintenance (equipment_key);

COMMENT ON TABLE curated.fact_maintenance IS 'Equipment maintenance event fact — partitioned by date_key';

CREATE TABLE curated.fact_maintenance_2024 PARTITION OF curated.fact_maintenance FOR VALUES FROM (20240101) TO (20250101);
CREATE TABLE curated.fact_maintenance_2025 PARTITION OF curated.fact_maintenance FOR VALUES FROM (20250101) TO (20260101);
CREATE TABLE curated.fact_maintenance_2026 PARTITION OF curated.fact_maintenance FOR VALUES FROM (20260101) TO (20270101);
CREATE TABLE curated.fact_maintenance_default PARTITION OF curated.fact_maintenance DEFAULT;

-- ============================================================================
-- Grain: One employee work record per day
CREATE TABLE curated.fact_workforce (
    workforce_key BIGSERIAL NOT NULL,
    date_key INTEGER NOT NULL,
    employee_key BIGINT NOT NULL,
    project_key BIGINT NOT NULL,
    hours_worked NUMERIC(10, 2),
    productivity_score NUMERIC(8, 2),
    CONSTRAINT pk_fact_workforce PRIMARY KEY (date_key, workforce_key),
    CONSTRAINT fk_fact_workforce_date FOREIGN KEY (date_key) REFERENCES curated.dim_date (date_key),
    CONSTRAINT fk_fact_workforce_employee FOREIGN KEY (employee_key) REFERENCES curated.dim_employee (employee_key),
    CONSTRAINT fk_fact_workforce_project FOREIGN KEY (project_key) REFERENCES curated.dim_project (project_key)
)
PARTITION BY
    RANGE (date_key);

CREATE INDEX idx_fact_workforce_date ON curated.fact_workforce (date_key);

CREATE INDEX idx_fact_workforce_employee ON curated.fact_workforce (employee_key);

COMMENT ON TABLE curated.fact_workforce IS 'Workforce productivity fact — daily grain, partitioned by date_key';

CREATE TABLE curated.fact_workforce_2024 PARTITION OF curated.fact_workforce FOR VALUES FROM (20240101) TO (20250101);
CREATE TABLE curated.fact_workforce_2025 PARTITION OF curated.fact_workforce FOR VALUES FROM (20250101) TO (20260101);
CREATE TABLE curated.fact_workforce_2026 PARTITION OF curated.fact_workforce FOR VALUES FROM (20260101) TO (20270101);
CREATE TABLE curated.fact_workforce_default PARTITION OF curated.fact_workforce DEFAULT;

-- ============================================================================
-- Grain: One risk occurrence event
CREATE TABLE curated.fact_risk (
    risk_event_key BIGSERIAL NOT NULL,
    date_key INTEGER NOT NULL,
    project_key BIGINT NOT NULL,
    risk_key BIGINT NOT NULL,
    probability NUMERIC(5, 2),
    severity_score NUMERIC(5, 2),
    impact_cost NUMERIC(18, 2),
    impact_days INTEGER,
    risk_score NUMERIC(10, 2),
    CONSTRAINT pk_fact_risk PRIMARY KEY (date_key, risk_event_key),
    CONSTRAINT fk_fact_risk_date FOREIGN KEY (date_key) REFERENCES curated.dim_date (date_key),
    CONSTRAINT fk_fact_risk_project FOREIGN KEY (project_key) REFERENCES curated.dim_project (project_key),
    CONSTRAINT fk_fact_risk_risk FOREIGN KEY (risk_key) REFERENCES curated.dim_risk (risk_key)
)
PARTITION BY
    RANGE (date_key);

CREATE INDEX idx_fact_risk_date ON curated.fact_risk (date_key);

CREATE INDEX idx_fact_risk_project ON curated.fact_risk (project_key);

CREATE INDEX idx_fact_risk_risk ON curated.fact_risk (risk_key);

COMMENT ON TABLE curated.fact_risk IS 'Risk event fact — partitioned by date_key';

CREATE TABLE curated.fact_risk_2024 PARTITION OF curated.fact_risk FOR VALUES FROM (20240101) TO (20250101);
CREATE TABLE curated.fact_risk_2025 PARTITION OF curated.fact_risk FOR VALUES FROM (20250101) TO (20260101);
CREATE TABLE curated.fact_risk_2026 PARTITION OF curated.fact_risk FOR VALUES FROM (20260101) TO (20270101);
CREATE TABLE curated.fact_risk_default PARTITION OF curated.fact_risk DEFAULT;

COMMENT ON COLUMN curated.fact_risk.risk_score IS 'Derived: probability × severity_score';

-- ============================================================================
-- AUDIT TABLE
-- ============================================================================
CREATE TABLE audit.etl_execution_log (
    execution_id BIGSERIAL NOT NULL,
    pipeline_name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT NOW(),
    end_time TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    rows_processed BIGINT,
    error_message TEXT,
    CONSTRAINT pk_etl_execution_log PRIMARY KEY (execution_id)
);

COMMENT ON TABLE audit.etl_execution_log IS 'ETL pipeline audit trail';