# Guía de Ejecución — Data Warehouse

## Orden de ejecución

Los scripts deben ejecutarse en este orden estricto:

```powershell
# 1. Crear esquemas (raw, trusted, curated, audit)
Get-Content warehouse/sql/create_schemas.sql | docker exec -i platform_postgres psql -U admin -d analytics_db

# 2. Crear tablas dimensionales (curated)
Get-Content warehouse/sql/create_dimensions.sql | docker exec -i platform_postgres psql -U admin -d analytics_db

# 3. Crear tablas de hechos + particiones + auditoría (curated, audit)
Get-Content warehouse/sql/create_facts.sql | docker exec -i platform_postgres psql -U admin -d analytics_db

# 4. Cargar datos semilla
Get-Content warehouse/sql/seed_data.sql | docker exec -i platform_postgres psql -U admin -d analytics_db
```

## Reset completo (borra todo y vuelve a empezar)

```powershell
docker exec platform_postgres psql -U admin -d analytics_db -c "DROP SCHEMA curated CASCADE; DROP SCHEMA audit CASCADE;"
```

Luego ejecutar los pasos 1–4 de arriba.

## Conexión a la base de datos

| Variable | Valor |
|---|---|
| Host | `localhost` |
| Puerto | `5432` |
| Usuario | `admin` |
| Base de datos | `analytics_db` |

## Verificación

```powershell
docker exec platform_postgres psql -U admin -d analytics_db -c "
SELECT table_name, rows FROM (
  SELECT 'dim_date' AS table_name, COUNT(*) AS rows FROM curated.dim_date
  UNION ALL SELECT 'dim_location', COUNT(*) FROM curated.dim_location
  UNION ALL SELECT 'dim_project', COUNT(*) FROM curated.dim_project
  UNION ALL SELECT 'dim_equipment', COUNT(*) FROM curated.dim_equipment
  UNION ALL SELECT 'dim_employee', COUNT(*) FROM curated.dim_employee
  UNION ALL SELECT 'dim_vendor', COUNT(*) FROM curated.dim_vendor
  UNION ALL SELECT 'dim_risk', COUNT(*) FROM curated.dim_risk
  UNION ALL SELECT 'fact_cost', COUNT(*) FROM curated.fact_cost
  UNION ALL SELECT 'fact_schedule', COUNT(*) FROM curated.fact_schedule
  UNION ALL SELECT 'fact_maintenance', COUNT(*) FROM curated.fact_maintenance
  UNION ALL SELECT 'fact_workforce', COUNT(*) FROM curated.fact_workforce
  UNION ALL SELECT 'fact_risk', COUNT(*) FROM curated.fact_risk
  UNION ALL SELECT 'etl_execution_log', COUNT(*) FROM audit.etl_execution_log
) sub ORDER BY table_name;
"
```

## Esquema del modelo

```
raw         → Staging / carga inicial (datos sin transformar)
trusted     → Datos limpiados y validados
curated     → Modelo dimensional (estrellas)
  ├── dim_date         (calendario)
  ├── dim_location     (SCD Type 1)
  ├── dim_project      (SCD Type 2)
  ├── dim_equipment    (SCD Type 2)
  ├── dim_employee     (SCD Type 2)
  ├── dim_vendor       (SCD Type 1)
  ├── dim_risk         (SCD Type 1)
  ├── fact_cost        (particionada por date_key)
  ├── fact_schedule    (particionada por date_key)
  ├── fact_maintenance (particionada por date_key)
  ├── fact_workforce   (particionada por date_key)
  └── fact_risk        (particionada por date_key)
audit       → Logs de ejecución ETL
  └── etl_execution_log
```

## Notas

- Las tablas de hechos usan `PARTITION BY RANGE (date_key)` con particiones anuales (`_2024`, `_2025`, `_2026`) más una partición `_default`.
- El seed data cubre calendario 2025–2026 y datos de muestra para 8 proyectos.
- Para conectarte desde otra herramienta (DBeaver, Tableau, etc.) usa las credenciales de `docker-compose.yml`.
