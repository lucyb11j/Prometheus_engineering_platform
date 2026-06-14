import psycopg2
from psycopg2.extras import execute_values
from typing import Any

from etl.config.database import config


RAW_TABLES = {
    "projects": ["project_id", "project_name", "project_type", "status", "start_date", "end_date", "budget"],
    "locations": ["location_id", "country", "region", "city", "site_name"],
    "vendors": ["vendor_id", "vendor_name", "category", "country"],
    "employees": ["employee_id", "full_name", "department", "role", "hire_date"],
    "equipment": ["equipment_id", "equipment_name", "equipment_type", "manufacturer", "purchase_date", "status"],
    "costs": ["project_id", "vendor_id", "cost_date", "planned_cost", "actual_cost"],
    "schedule": ["project_id", "report_date", "planned_progress", "actual_progress"],
    "maintenance": ["equipment_id", "maintenance_date", "maintenance_type", "downtime_hours", "maintenance_cost"],
    "risks": ["risk_id", "project_id", "risk_description", "probability", "severity", "impact_cost", "impact_days", "risk_date"],
    "workforce": ["employee_id", "project_id", "report_date", "hours_worked", "productivity_score"],
}


def _ensure_raw_table(conn, table_name: str):
    with conn.cursor() as cur:
        cols = RAW_TABLES[table_name]
        col_defs = ", ".join(f"{c} TEXT" for c in cols)
        cur.execute(f"CREATE TABLE IF NOT EXISTS raw.{table_name} ({col_defs})")
        for c in cols:
            try:
                cur.execute(f"ALTER TABLE raw.{table_name} ADD COLUMN IF NOT EXISTS {c} TEXT")
            except Exception:
                pass


def load_raw(table_name: str, rows: list[dict[str, Any]]) -> int:
    if table_name not in RAW_TABLES:
        raise ValueError(f"Unknown raw table: {table_name}")

    columns = RAW_TABLES[table_name]
    values = [[r[c] for c in columns] for r in rows]

    conn = psycopg2.connect(config.DB.dsn)
    try:
        _ensure_raw_table(conn, table_name)
        with conn.cursor() as cur:
            execute_values(
                cur,
                f"INSERT INTO raw.{table_name} ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING",
                values,
            )
        conn.commit()
        return len(rows)
    finally:
        conn.close()
