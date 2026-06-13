-- ============================================================================
-- SEED DATA — Prometheus Analytics Platform (EIAP)
-- Must run AFTER create_schemas, create_dimensions, create_facts
-- ============================================================================

BEGIN;

-- ============================================================================
-- 1. dim_date — Calendar year 2025–2026
-- ============================================================================
INSERT INTO curated.dim_date (date_key, full_date, year, quarter, month, month_name, week, day, day_name)
SELECT
    CAST(TO_CHAR(d, 'YYYYMMDD') AS INTEGER) AS date_key,
    d                                        AS full_date,
    EXTRACT(YEAR FROM d)::SMALLINT           AS year,
    EXTRACT(QUARTER FROM d)::SMALLINT        AS quarter,
    EXTRACT(MONTH FROM d)::SMALLINT          AS month,
    TO_CHAR(d, 'FMMonth')                    AS month_name,
    EXTRACT(WEEK FROM d)::SMALLINT           AS week,
    EXTRACT(DAY FROM d)::SMALLINT            AS day,
    TO_CHAR(d, 'FMDay')                      AS day_name
FROM GENERATE_SERIES(
    '2025-01-01'::DATE,
    '2026-12-31'::DATE,
    '1 day'::INTERVAL
) AS d;

-- ============================================================================
-- 2. dim_location
-- ============================================================================
INSERT INTO curated.dim_location (location_id, country, region, city, site_name) VALUES
('LOC-001', 'Peru',     'Lima',           'Lima',        'Sede Central Lima'),
('LOC-002', 'Peru',     'Cusco',          'Cusco',       'Proyecto Mina Cusco'),
('LOC-003', 'Chile',    'Antofagasta',    'Antofagasta', 'Planta Desaladora ANF'),
('LOC-004', 'Colombia', 'Antioquia',      'Medellín',    'Túnel Antioquia'),
('LOC-005', 'Argentina', 'Neuquén',       'Añelo',       'Yacimiento Vaca Muerta'),
('LOC-006', 'Peru',     'Arequipa',       'Arequipa',    'Ampliación Aeropuerto AQP'),
('LOC-007', 'Ecuador',  'Orellana',       'Coca',        'Bloque Amazonas'),
('LOC-008', 'Chile',    'Santiago',       'Santiago',    'Edificio Corporativo Costanera');

-- ============================================================================
-- 3. dim_project (SCD Type 2 — current versions)
-- ============================================================================
INSERT INTO curated.dim_project (project_id, project_name, project_type, location_key, start_date, planned_end_date, status)
VALUES
('PROJ-001', 'Mina Cusco – Fase 3',          'Minería',    2, '2024-01-15', '2026-06-30', 'Active'),
('PROJ-002', 'Planta Desaladora ANF',         'Energía',    3, '2024-03-01', '2026-12-31', 'Active'),
('PROJ-003', 'Túnel Antioquia',               'Infraestructura', 4, '2023-09-01', '2027-03-31', 'Active'),
('PROJ-004', 'Vaca Muerta – Perforación',     'Energía',    5, '2025-01-01', '2027-12-31', 'Active'),
('PROJ-005', 'Ampliación Aeropuerto AQP',     'Infraestructura', 6, '2025-06-01', '2028-05-31', 'Active'),
('PROJ-006', 'Campaña Exploración Amazonas',  'Minería',    7, '2024-07-01', '2025-09-30', 'Delayed'),
('PROJ-007', 'Costanera 2.0',                 'Construcción', 8, '2024-10-01', '2027-06-30', 'Active'),
('PROJ-008', 'Sede Central – Remodelación',   'Construcción', 1, '2023-01-01', '2025-03-31', 'Closed');

-- ============================================================================
-- 4. dim_equipment (SCD Type 2 — current versions)
-- ============================================================================
INSERT INTO curated.dim_equipment (equipment_id, equipment_name, equipment_type, manufacturer, purchase_date, status)
VALUES
('EQ-001',  'Excavadora CAT 320',    'Excavadora',  'Caterpillar', '2022-05-10', 'Operational'),
('EQ-002',  'Bulldozer D6',           'Bulldozer',   'Caterpillar', '2021-08-15', 'Operational'),
('EQ-003',  'Camión Volquete 777G',  'Camión',      'Caterpillar', '2023-01-20', 'Operational'),
('EQ-004',  'Perforadora Sandvik',   'Perforadora', 'Sandvik',     '2020-11-30', 'Operational'),
('EQ-005',  'Grúa Liebherr LTM1100', 'Grúa',        'Liebherr',    '2024-02-10', 'Operational'),
('EQ-006',  'Generador Cummins 500', 'Generador',   'Cummins',     '2019-06-01', 'Under Maintenance'),
('EQ-007',  'Compactador Bomag',     'Compactador', 'Bomag',       '2023-09-12', 'Operational'),
('EQ-008',  'Camión Mixer 10m³',     'Camión',      'Mercedes',    '2022-04-18', 'Operational');

-- ============================================================================
-- 5. dim_employee (SCD Type 2 — current versions)
-- ============================================================================
INSERT INTO curated.dim_employee (employee_id, full_name, role, department, hire_date)
VALUES
('EMP-001', 'Carlos Mendoza',      'Project Manager',        'PMO',          '2020-01-10'),
('EMP-002', 'María Torres',        'Cost Controller',        'Finance',      '2021-03-22'),
('EMP-003', 'José Ramírez',        'Site Supervisor',        'Operations',   '2019-07-15'),
('EMP-004', 'Ana Lucía Guerra',    'Safety Officer',         'HSE',          '2022-09-01'),
('EMP-005', 'Luis Huamán',         'Equipment Operator',     'Operations',   '2020-11-20'),
('EMP-006', 'Rosa Paredes',        'Data Analyst',           'Analytics',    '2023-05-10'),
('EMP-007', 'Pedro Castillo',      'Maintenance Technician', 'Maintenance',  '2018-04-30'),
('EMP-008', 'Diana Quispe',        'Risk Analyst',           'Risk Mgmt',    '2024-01-15');

-- ============================================================================
-- 6. dim_vendor
-- ============================================================================
INSERT INTO curated.dim_vendor (vendor_id, vendor_name, category, country) VALUES
('VEN-001', 'Ferreyros S.A.',        'Equipment',        'Peru'),
('VEN-002', 'Graña y Montero',       'Construction',     'Peru'),
('VEN-003', 'SK Ingeniería',         'Engineering',      'Chile'),
('VEN-004', 'Techint E&C',           'Engineering',      'Argentina'),
('VEN-005', 'Cummins Perú',          'Parts & Service',  'Peru'),
('VEN-006', 'Sandvik Chile',         'Equipment',        'Chile'),
('VEN-007', 'Construequipos',        'Equipment',        'Colombia'),
('VEN-008', 'Maptek Latam',          'Software',         'Chile');

-- ============================================================================
-- 7. dim_risk
-- ============================================================================
INSERT INTO curated.dim_risk (risk_id, risk_name, risk_category, risk_description) VALUES
('RSK-001', 'Geotechnical Failure',      'Technical',  'Landslide, collapse or geological instability'),
('RSK-002', 'Budget Overrun',            'Financial',  'Project execution exceeds approved budget'),
('RSK-003', 'Schedule Delay',            'Schedule',   'Critical path activities behind plan'),
('RSK-004', 'Equipment Breakdown',       'Operational','Unexpected failure of heavy equipment'),
('RSK-005', 'Labor Shortage',            'Workforce',  'Insufficient skilled labor available'),
('RSK-006', 'Supply Chain Disruption',   'Procurement','Delay in material or part delivery'),
('RSK-007', 'Environmental Incident',    'Regulatory', 'Spill, emission or permit violation'),
('RSK-008', 'Safety Accident',           'HSE',        'Personal injury or fatality');

-- ============================================================================
-- 8. fact_cost — Sample daily costs for each active project
-- ============================================================================
INSERT INTO curated.fact_cost (date_key, project_key, vendor_key, planned_cost, actual_cost, forecast_cost) VALUES
-- PROJ-001 (project_key = 1)
(20250115, 1, 1, 150000.00, 148500.00, 150000.00),
(20250131, 1, 1, 155000.00, 162000.00, 158000.00),
(20250215, 1, 2, 150000.00, 151200.00, 152000.00),
(20250228, 1, 1, 160000.00, 155000.00, 158000.00),
-- PROJ-002 (project_key = 2)
(20250301, 2, 3, 250000.00, 248000.00, 250000.00),
(20250315, 2, 3, 260000.00, 270000.00, 265000.00),
(20250331, 2, 6, 245000.00, 240000.00, 242000.00),
-- PROJ-003 (project_key = 3)
(20250105, 3, 2, 320000.00, 318000.00, 320000.00),
(20250120, 3, 4, 310000.00, 325000.00, 315000.00),
(20250205, 3, 7, 330000.00, 332000.00, 335000.00),
-- PROJ-007 (project_key = 7)
(20250401, 7, 5, 85000.00, 85200.00, 86000.00),
(20250415, 7, 5, 88000.00, 87500.00, 88000.00);

-- ============================================================================
-- 9. fact_schedule
-- ============================================================================
INSERT INTO curated.fact_schedule (date_key, project_key, planned_progress, actual_progress, spi) VALUES
(20250115, 1, 45.00, 43.50, 0.9667),
(20250131, 1, 47.00, 46.00, 0.9787),
(20250215, 1, 49.00, 48.20, 0.9837),
(20250228, 1, 51.00, 50.10, 0.9824),
(20250301, 2, 8.00,  8.50,  1.0625),
(20250315, 2, 10.00, 9.80,  0.9800),
(20250331, 2, 12.00, 11.50, 0.9583),
(20250105, 3, 35.00, 36.00, 1.0286),
(20250120, 3, 37.00, 37.50, 1.0135),
(20250205, 3, 39.00, 38.00, 0.9744),
(20250401, 7, 12.00, 11.80, 0.9833),
(20250415, 7, 14.00, 14.20, 1.0143);

-- ============================================================================
-- 10. fact_maintenance
-- ============================================================================
INSERT INTO curated.fact_maintenance (date_key, equipment_key, maintenance_type, downtime_hours, maintenance_cost) VALUES
(20250110, 6, 'Corrective', 8.5,  12500.00),
(20250220, 1, 'Preventive', 4.0,   5800.00),
(20250305, 4, 'Preventive', 6.0,   9200.00),
(20250310, 6, 'Corrective', 12.0, 18700.00),
(20250318, 2, 'Preventive', 3.5,   4300.00),
(20250401, 5, 'Preventive', 5.0,   7600.00);

-- ============================================================================
-- 11. fact_workforce
-- ============================================================================
INSERT INTO curated.fact_workforce (date_key, employee_key, project_key, hours_worked, productivity_score) VALUES
(20250115, 1, 1, 8.0, 92.50),
(20250115, 3, 1, 9.5, 88.00),
(20250115, 5, 1, 10.0, 85.00),
(20250301, 2, 2, 8.0, 95.00),
(20250301, 4, 2, 8.0, 90.00),
(20250315, 2, 2, 8.5, 91.50),
(20250105, 6, 7, 7.5, 93.00),
(20250401, 7, 7, 8.0, 89.00);

-- ============================================================================
-- 12. fact_risk
-- ============================================================================
INSERT INTO curated.fact_risk (date_key, project_key, risk_key, probability, severity_score, impact_cost, impact_days, risk_score) VALUES
(20250120, 1, 1, 0.30, 8.0, 500000.00, 45, 2.40),
(20250215, 1, 2, 0.60, 7.0, 1200000.00, 0,  4.20),
(20250310, 3, 3, 0.50, 6.0, 800000.00,  30, 3.00),
(20250320, 2, 6, 0.40, 5.0, 350000.00,  15, 2.00),
(20250405, 7, 4, 0.25, 7.0, 150000.00,  10, 1.75),
(20250410, 1, 8, 0.15, 9.0, 2000000.00, 60, 1.35);

COMMIT;
