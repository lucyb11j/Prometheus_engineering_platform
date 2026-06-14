import psycopg2
from psycopg2.extras import execute_values
from typing import Any

from etl.config.database import config


def load_dim_date(conn, start: str = "2024-01-01", end: str = "2027-12-31") -> int:
    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO curated.dim_date (date_key, full_date, year, quarter, month, month_name, week, day, day_name)
            SELECT
                CAST(TO_CHAR(d, 'YYYYMMDD') AS INTEGER),
                d,
                EXTRACT(YEAR FROM d)::SMALLINT,
                EXTRACT(QUARTER FROM d)::SMALLINT,
                EXTRACT(MONTH FROM d)::SMALLINT,
                TO_CHAR(d, 'FMMonth'),
                EXTRACT(WEEK FROM d)::SMALLINT,
                EXTRACT(DAY FROM d)::SMALLINT,
                TO_CHAR(d, 'FMDay')
            FROM GENERATE_SERIES(%s::DATE, %s::DATE, '1 day'::INTERVAL) AS d
            ON CONFLICT DO NOTHING
        """, (start, end))
        conn.commit()
        return cur.rowcount
    return 0


def load_dim_location(conn, rows: list[dict[str, Any]]) -> dict[str, int]:
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.dim_location (location_id, country, region, city, site_name) VALUES %s ON CONFLICT (location_id) DO UPDATE SET country=EXCLUDED.country, region=EXCLUDED.region, city=EXCLUDED.city, site_name=EXCLUDED.site_name RETURNING location_id, location_key",
            [[r["location_id"], r["country"], r["region"], r["city"], r["site_name"]] for r in rows],
            fetch=True,
        )
        conn.commit()
        return {row[0]: row[1] for row in cur.fetchall()}


def load_dim_vendor(conn, rows: list[dict[str, Any]]) -> dict[str, int]:
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.dim_vendor (vendor_id, vendor_name, category, country) VALUES %s ON CONFLICT (vendor_id) DO UPDATE SET vendor_name=EXCLUDED.vendor_name, category=EXCLUDED.category, country=EXCLUDED.country RETURNING vendor_id, vendor_key",
            [[r["vendor_id"], r["vendor_name"], r["category"], r["country"]] for r in rows],
            fetch=True,
        )
        conn.commit()
        return {row[0]: row[1] for row in cur.fetchall()}


def load_dim_employee(conn, rows: list[dict[str, Any]]) -> dict[str, int]:
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.dim_employee (employee_id, full_name, role, department, hire_date) VALUES %s ON CONFLICT DO NOTHING RETURNING employee_id, employee_key",
            [[r["employee_id"], r["full_name"], r["role"], r["department"], r["hire_date"]] for r in rows],
            fetch=True,
        )
        conn.commit()
        result = cur.fetchall()
        return {row[0]: row[1] for row in result} if result else {}


def load_dim_equipment(conn, rows: list[dict[str, Any]]) -> dict[str, int]:
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.dim_equipment (equipment_id, equipment_name, equipment_type, status) VALUES %s ON CONFLICT DO NOTHING RETURNING equipment_id, equipment_key",
            [[r["equipment_id"], r["equipment_name"], r["equipment_type"], r["status"]] for r in rows],
            fetch=True,
        )
        conn.commit()
        result = cur.fetchall()
        return {row[0]: row[1] for row in result} if result else {}


def load_dim_project(conn, rows: list[dict[str, Any]], location_map: dict[str, int]) -> dict[str, int]:
    with conn.cursor() as cur:
        projected_rows = []
        for r in rows:
            loc_key = location_map.get(r.get("location_id", ""), None)
            projected_rows.append([r["project_id"], r["project_name"], r["project_type"], loc_key, r["start_date"], r["end_date"], r["status"]])
        execute_values(
            cur,
            "INSERT INTO curated.dim_project (project_id, project_name, project_type, location_key, start_date, planned_end_date, status) VALUES %s ON CONFLICT DO NOTHING RETURNING project_id, project_key",
            projected_rows,
            fetch=True,
        )
        conn.commit()
        result = cur.fetchall()
        return {row[0]: row[1] for row in result} if result else {}


def load_dim_risk(conn, rows: list[dict[str, Any]]) -> dict[str, int]:
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.dim_risk (risk_id, risk_name, risk_category, risk_description) VALUES %s ON CONFLICT (risk_id) DO UPDATE SET risk_description=EXCLUDED.risk_description RETURNING risk_id, risk_key",
            [[r["risk_id"], r.get("risk_name", ""), r.get("risk_category", "General"), r.get("risk_description", "")] for r in rows],
            fetch=True,
        )
        conn.commit()
        return {row[0]: row[1] for row in cur.fetchall()}


def load_fact_cost(conn, rows: list[dict], project_map: dict[str, int], vendor_map: dict[str, int]) -> int:
    with conn.cursor() as cur:
        values = []
        for r in rows:
            date_key = int(r["cost_date"].strftime("%Y%m%d"))
            proj_key = project_map.get(r["project_id"])
            vend_key = vendor_map.get(r.get("vendor_id", ""))
            if proj_key is None:
                continue
            values.append([date_key, proj_key, vend_key, r["planned_cost"], r["actual_cost"], None])
        if not values:
            return 0
        execute_values(
            cur,
            "INSERT INTO curated.fact_cost (date_key, project_key, vendor_key, planned_cost, actual_cost, forecast_cost) VALUES %s ON CONFLICT DO NOTHING",
            values,
        )
        conn.commit()
        return len(values)


def load_fact_schedule(conn, rows: list[dict], project_map: dict[str, int]) -> int:
    with conn.cursor() as cur:
        values = []
        for r in rows:
            date_key = int(r["report_date"].strftime("%Y%m%d"))
            proj_key = project_map.get(r["project_id"])
            if proj_key is None:
                continue
            spi = round(r["actual_progress"] / r["planned_progress"], 4) if r["planned_progress"] > 0 else None
            values.append([date_key, proj_key, r["planned_progress"], r["actual_progress"], spi])
        if not values:
            return 0
        execute_values(
            cur,
            "INSERT INTO curated.fact_schedule (date_key, project_key, planned_progress, actual_progress, spi) VALUES %s ON CONFLICT DO NOTHING",
            values,
        )
        conn.commit()
        return len(values)


def load_fact_maintenance(conn, rows: list[dict], equipment_map: dict[str, int]) -> int:
    with conn.cursor() as cur:
        values = []
        for r in rows:
            date_key = int(r["maintenance_date"].strftime("%Y%m%d"))
            eq_key = equipment_map.get(r["equipment_id"])
            if eq_key is None:
                continue
            values.append([date_key, eq_key, r["maintenance_type"], r["downtime_hours"], r["maintenance_cost"]])
        if not values:
            return 0
        execute_values(
            cur,
            "INSERT INTO curated.fact_maintenance (date_key, equipment_key, maintenance_type, downtime_hours, maintenance_cost) VALUES %s ON CONFLICT DO NOTHING",
            values,
        )
        conn.commit()
        return len(values)


def load_fact_workforce(conn, rows: list[dict], employee_map: dict[str, int], project_map: dict[str, int]) -> int:
    with conn.cursor() as cur:
        values = []
        for r in rows:
            date_key = int(r["report_date"].strftime("%Y%m%d"))
            emp_key = employee_map.get(r["employee_id"])
            proj_key = project_map.get(r["project_id"])
            if emp_key is None or proj_key is None:
                continue
            values.append([date_key, emp_key, proj_key, r["hours_worked"], r["productivity_score"]])
        if not values:
            return 0
        execute_values(
            cur,
            "INSERT INTO curated.fact_workforce (date_key, employee_key, project_key, hours_worked, productivity_score) VALUES %s ON CONFLICT DO NOTHING",
            values,
        )
        conn.commit()
        return len(values)


def load_fact_risk(conn, rows: list[dict], project_map: dict[str, int], risk_map: dict[str, int]) -> int:
    with conn.cursor() as cur:
        values = []
        for r in rows:
            proj_key = project_map.get(r["project_id"])
            risk_key = risk_map.get(r["risk_id"])
            if proj_key is None or risk_key is None:
                continue
            risk_score = round(r["probability"] * r["severity"], 2)
            values.append([proj_key, risk_key, r["probability"], r["severity"], r["impact_cost"], r["impact_days"], risk_score])
        if not values:
            return 0
        execute_values(
            cur,
            "INSERT INTO curated.fact_risk (project_key, risk_key, probability, severity_score, impact_cost, impact_days, risk_score) VALUES %s ON CONFLICT DO NOTHING",
            values,
        )
        conn.commit()
        return len(values)
