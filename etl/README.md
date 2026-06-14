# ETL Pipeline — Engineering Platform

Pipeline ETL en Python que extrae datasets sintéticos desde CSVs, los transforma y los carga en PostgreSQL siguiendo el modelo medallión (raw → trusted → curated).

---

## Arquitectura

```
datasets/*.csv
      │
      ▼
  ┌─────────┐
  │ EXTRACT  │  Lee CSVs → dicts de Python
  └────┬────┘
       │
       ▼
  ┌───────────┐
  │ TRANSFORM  │  Limpia, tipa, valida (fechas, floats, strings)
  └─────┬─────┘
        │
        ▼
  ┌───────────┐     ┌────────────┐
  │ LOAD RAW   │────▶│ raw.*      │  Espejo del CSV, sin cambios
  └───────────┘     └────────────┘
        │
        ▼
  ┌──────────────┐  ┌──────────────┐
  │ LOAD TRUSTED  │──▶│ trusted.*    │  Datos limpios y validados
  └───────┬──────┘  └──────────────┘
          │
          ▼
  ┌──────────────┐  ┌────────────────────────────┐
  │ LOAD CURATED  │──▶│ curated.dim_* / fact_*    │
  └──────────────┘  │  Modelo dimensional (SCD)   │
                    └────────────────────────────┘
```

---

## Estructura de archivos

| Archivo | Propósito |
|---|---|
| `main.py` | Orquestador — ejecuta las fases en orden |
| `config/database.py` | Configuración de conexión PostgreSQL (vía env vars) |
| `extract/__init__.py` | `read_csv()` genérico + re-export de extractores |
| `extract/extract_*.py` | 9 extractores, uno por entidad |
| `transform/__init__.py` | Re-export de transformadores |
| `transform/transform_*.py` | 9 transformadores, limpian y tipan datos |
| `load/load_raw.py` | Inserta en esquema `raw` mediante `execute_values` |
| `load/load_trusted.py` | Inserta en esquema `trusted` |
| `load/load_curated.py` | Carga dimensiones (SCD Type 1/2) y tablas de hechos |
| `logs/etl.log` | Bitácora de ejecución |

---

## Requisitos

- Python 3.11+
- PostgreSQL 15+ con los esquemas creados:
  ```sql
  CREATE SCHEMA IF NOT EXISTS raw;
  CREATE SCHEMA IF NOT EXISTS trusted;
  CREATE SCHEMA IF NOT EXISTS curated;
  CREATE SCHEMA IF NOT EXISTS audit;
  ```
- Las tablas del modelo curated deben existir (ver `warehouse/sql/`)
- Datasets generados en `datasets/` (ejecutar `python datasets/generate_datasets.py`)

### Dependencias Python

```bash
pip install psycopg2-binary
```

---

## Configuración

Variables de entorno (o valores por defecto):

| Variable | Default | Descripción |
|---|---|---|
| `DB_HOST` | `localhost` | Host PostgreSQL |
| `DB_PORT` | `5432` | Puerto PostgreSQL |
| `DB_NAME` | `engineering_platform` | Base de datos |
| `DB_USER` | `postgres` | Usuario |
| `DB_PASSWORD` | `postgres` | Contraseña |
| `DATASETS_DIR` | `datasets` | Ruta a los CSVs |

---

## Ejecución

### Todas las fases

```bash
python etl/main.py
```

### Fases específicas

```bash
python etl/main.py --stages extract
python etl/main.py --stages extract transform
python etl/main.py --stages load_raw
python etl/main.py --stages load_curated
```

### Flujo típico completo

```bash
# 1. Generar datasets
python datasets/generate_datasets.py

# 2. Ejecutar ETL completo
python etl/main.py
```

---

## Flujo de datos por entidad

### Dimensiones (cargadas en curated)

| Entidad | Origen CSV | Tabla destino | SCD |
|---|---|---|---|
| Proyectos | `projects.csv` | `curated.dim_project` | Type 2 |
| Ubicaciones | `locations.csv` | `curated.dim_location` | Type 1 |
| Proveedores | `vendors.csv` | `curated.dim_vendor` | Type 1 |
| Empleados | `employees.csv` | `curated.dim_employee` | Type 2 |
| Equipos | `equipment.csv` | `curated.dim_equipment` | Type 2 |
| Riesgos | `risks.csv` | `curated.dim_risk` | Type 1 |
| Calendario | — (generado) | `curated.dim_date` | — |

### Hechos (cargadas en curated)

| Hecho | Origen CSV | Tabla destino | Particionado por |
|---|---|---|---|
| Costos | `costs.csv` | `curated.fact_cost` | `date_key` |
| Avance | `schedule.csv` | `curated.fact_schedule` | `date_key` |
| Mantenimiento | `maintenance.csv` | `curated.fact_maintenance` | `date_key` |
| Riesgos | `risks.csv` | `curated.fact_risk` | `date_key` |

---

## Columnas derivadas

| Tabla | Columna | Fórmula |
|---|---|---|
| `fact_schedule` | `spi` | `actual_progress / planned_progress` (Schedule Performance Index) |
| `fact_risk` | `risk_score` | `probability × severity_score` |

---

## Logging

Toda la ejecución se registra en:

```
etl/logs/etl.log
```

Con formato: `timestamp [LEVEL] mensaje` — tanto a archivo como a stdout.

---

## Prueba rápida (sin base de datos)

Para validar que extract y transform funcionan sin PostgreSQL:

```bash
python -c "
from etl.extract import extract_projects
from etl.transform import transform_projects
data = extract_projects('datasets/projects.csv')
clean = transform_projects(data)
print(f'{len(clean)} proyectos transformados correctamente')
"
```
