-- ============================================================================
-- DIMENSION TABLES — curated schema
-- Prometheus Analytics Platform (EIAP)
-- Based on Physical Data Model v1.0
-- ============================================================================

-- SCD Type: None (static calendar)
-- Grain: One record per calendar day
CREATE TABLE curated.dim_date (
    date_key      INTEGER     NOT NULL,
    full_date     DATE        NOT NULL,
    year          SMALLINT    NOT NULL,
    quarter       SMALLINT    NOT NULL,
    month         SMALLINT    NOT NULL,
    month_name    VARCHAR(20) NOT NULL,
    week          SMALLINT    NOT NULL,
    day           SMALLINT    NOT NULL,
    day_name      VARCHAR(20) NOT NULL,
    CONSTRAINT pk_dim_date PRIMARY KEY (date_key)
);

COMMENT ON TABLE curated.dim_date IS 'Calendar dimension for time-series analysis';
COMMENT ON COLUMN curated.dim_date.date_key IS 'Surrogate key in YYYYMMDD format';


-- ============================================================================
-- SCD Type: 1 (overwrite)
-- Grain: One record per location
CREATE TABLE curated.dim_location (
    location_key  BIGSERIAL   NOT NULL,
    location_id   VARCHAR(50) NOT NULL,
    country       VARCHAR(100),
    region        VARCHAR(100),
    city          VARCHAR(100),
    site_name     VARCHAR(200),
    CONSTRAINT pk_dim_location PRIMARY KEY (location_key),
    CONSTRAINT uq_dim_location_id UNIQUE (location_id)
);

COMMENT ON TABLE curated.dim_location IS 'Geographic location dimension (SCD Type 1)';


-- ============================================================================
-- SCD Type: 2 (preserve history via effective_date, expiration_date, is_current)
-- Grain: One record per project
CREATE TABLE curated.dim_project (
    project_key      BIGSERIAL   NOT NULL,
    project_id       VARCHAR(50) NOT NULL,
    project_name     VARCHAR(200),
    project_type     VARCHAR(100),
    location_key     BIGINT,
    start_date       DATE,
    planned_end_date DATE,
    status           VARCHAR(50),
    effective_date   DATE        NOT NULL DEFAULT CURRENT_DATE,
    expiration_date  DATE        NOT NULL DEFAULT '9999-12-31',
    is_current       BOOLEAN     NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_dim_project PRIMARY KEY (project_key),
    CONSTRAINT fk_dim_project_location
        FOREIGN KEY (location_key)
        REFERENCES curated.dim_location (location_key)
);

CREATE INDEX idx_dim_project_status
    ON curated.dim_project (status);

COMMENT ON TABLE curated.dim_project IS 'Project dimension (SCD Type 2 — full history tracked)';


-- ============================================================================
-- SCD Type: 2 (preserve history)
-- Grain: One record per equipment asset
CREATE TABLE curated.dim_equipment (
    equipment_key  BIGSERIAL   NOT NULL,
    equipment_id   VARCHAR(50) NOT NULL,
    equipment_name VARCHAR(200),
    equipment_type VARCHAR(100),
    manufacturer   VARCHAR(100),
    purchase_date  DATE,
    status         VARCHAR(50),
    effective_date   DATE    NOT NULL DEFAULT CURRENT_DATE,
    expiration_date  DATE    NOT NULL DEFAULT '9999-12-31',
    is_current       BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_dim_equipment PRIMARY KEY (equipment_key)
);

COMMENT ON TABLE curated.dim_equipment IS 'Equipment dimension (SCD Type 2 — full history tracked)';


-- ============================================================================
-- SCD Type: 2 (preserve history)
-- Grain: One record per employee
CREATE TABLE curated.dim_employee (
    employee_key  BIGSERIAL   NOT NULL,
    employee_id   VARCHAR(50) NOT NULL,
    full_name     VARCHAR(200),
    role          VARCHAR(100),
    department    VARCHAR(100),
    hire_date     DATE,
    effective_date   DATE    NOT NULL DEFAULT CURRENT_DATE,
    expiration_date  DATE    NOT NULL DEFAULT '9999-12-31',
    is_current       BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_dim_employee PRIMARY KEY (employee_key)
);

COMMENT ON TABLE curated.dim_employee IS 'Employee dimension (SCD Type 2 — full history tracked)';


-- ============================================================================
-- SCD Type: 1 (overwrite)
-- Grain: One record per vendor
CREATE TABLE curated.dim_vendor (
    vendor_key  BIGSERIAL   NOT NULL,
    vendor_id   VARCHAR(50) NOT NULL,
    vendor_name VARCHAR(200),
    category    VARCHAR(100),
    country     VARCHAR(100),
    CONSTRAINT pk_dim_vendor PRIMARY KEY (vendor_key),
    CONSTRAINT uq_dim_vendor_id UNIQUE (vendor_id)
);

COMMENT ON TABLE curated.dim_vendor IS 'Vendor / supplier dimension (SCD Type 1)';


-- ============================================================================
-- SCD Type: 1 (overwrite)
-- Grain: One record per risk category
CREATE TABLE curated.dim_risk (
    risk_key         BIGSERIAL   NOT NULL,
    risk_id          VARCHAR(50) NOT NULL,
    risk_name        VARCHAR(200),
    risk_category    VARCHAR(100),
    risk_description TEXT,
    CONSTRAINT pk_dim_risk PRIMARY KEY (risk_key),
    CONSTRAINT uq_dim_risk_id UNIQUE (risk_id)
);

COMMENT ON TABLE curated.dim_risk IS 'Risk classification dimension (SCD Type 1)';
