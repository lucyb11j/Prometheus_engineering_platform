import psycopg2
from psycopg2.extras import execute_values
from typing import Any
from datetime import date

from etl.config.database import config
from etl.transform.curated import (
    build_dim_date, build_dim_location, build_dim_vendor,
    build_dim_employee, build_dim_equipment, build_dim_project,
    build_dim_risk,
    build_fact_cost, build_fact_schedule, build_fact_maintenance,
    build_fact_workforce, build_fact_risk,
)


def load_dim_date(conn, start: str = "2020-01-01", end: str = "2035-12-31") -> int:
    rows = build_dim_date(start, end)
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.dim_date (date_key, full_date, year, quarter, month, month_name, week, day, day_name) VALUES %s ON CONFLICT DO NOTHING",
            [[r["date_key"], r["full_date"], r["year"], r["quarter"], r["month"], r["month_name"], r["week"], r["day"], r["day_name"]] for r in rows],
        )
        conn.commit()
    return len(rows)


def _resolve_business_keys(conn, table: str, id_col: str) -> dict[str, int]:
    with conn.cursor() as cur:
        cur.execute(f"SELECT {id_col}, {table[:-4] + '_key'} FROM curated.{table} WHERE is_current = TRUE")
        return {row[0]: row[1] for row in cur.fetchall()}


def _scd2_upsert(conn, table: str, id_col: str, tracked: list[str], rows: list[dict]):
    if not rows:
        return {}
    today = date.today()
    key_col = table.replace("dim_", "") + "_key"
    cols = [id_col] + [c for c in rows[0].keys() if c not in (id_col, key_col)]
    existing: dict[str, dict] = {}
    with conn.cursor() as cur:
        cur.execute(f"SELECT {id_col}, {key_col}, {', '.join(tracked)} FROM curated.{table} WHERE is_current = TRUE")
        for row in cur.fetchall():
            bid = row[0]
            tv = {}
            for i, t in enumerate(tracked):
                tv[t] = row[2 + i]
            existing[bid] = {"key": row[1], "tracked": tv}
    to_expire: list[int] = []
    to_insert: list[dict] = []
    sk_map: dict[str, int] = {}
    seen: set[str] = set()
    for r in rows:
        bid = r[id_col]
        if bid in seen:
            continue
        seen.add(bid)
        tracked_vals = {t: r.get(t) for t in tracked}
        if bid in existing:
            if tracked_vals != existing[bid]["tracked"]:
                to_expire.append(existing[bid]["key"])
                to_insert.append(r)
            else:
                sk_map[bid] = existing[bid]["key"]
        else:
            to_insert.append(r)
    with conn.cursor() as cur:
        for sk in to_expire:
            cur.execute(f"UPDATE curated.{table} SET expiration_date = %s, is_current = FALSE WHERE {key_col} = %s", (today, sk))
        for r in to_insert:
            placeholders = ", ".join([f"%s" for _ in cols])
            col_list = ", ".join(cols + ["effective_date", "expiration_date", "is_current"])
            val_list = [r[c] for c in cols] + [today, date(9999, 12, 31), True]
            cur.execute(
                f"INSERT INTO curated.{table} ({col_list}) VALUES ({placeholders}, %s, %s, %s) RETURNING {id_col}, {key_col}",
                val_list,
            )
            row = cur.fetchone()
            if row:
                sk_map[row[0]] = row[1]
        conn.commit()
    return sk_map


def _scd1_upsert(conn, table: str, id_col: str, rows: list[dict], extra_set: str = ""):
    if not rows:
        return {}
    key_col = table.replace("dim_", "") + "_key"
    cols = [c for c in rows[0].keys() if c != key_col]
    set_clause = ", ".join(f"{c}=EXCLUDED.{c}" for c in cols if c != id_col)
    if extra_set:
        set_clause += f", {extra_set}"
    col_list = ", ".join(cols)
    placeholders = ", ".join([f"%s" for _ in cols])
    with conn.cursor() as cur:
        execute_values(
            cur,
            f"INSERT INTO curated.{table} ({col_list}) VALUES %s ON CONFLICT ({id_col}) DO UPDATE SET {set_clause} RETURNING {id_col}, {key_col}",
            [[r[c] for c in cols] for r in rows],
            fetch=True,
        )
        conn.commit()
        return {row[0]: row[1] for row in cur.fetchall()}


def load_dim_location(conn, rows: list[dict]) -> dict[str, int]:
    built = build_dim_location(rows)
    return _scd1_upsert(conn, "dim_location", "location_id", built)


def load_dim_vendor(conn, rows: list[dict]) -> dict[str, int]:
    built = build_dim_vendor(rows)
    return _scd2_upsert(conn, "dim_vendor", "vendor_id", ["vendor_name", "category", "country"], built)


def load_dim_employee(conn, rows: list[dict]) -> dict[str, int]:
    built = build_dim_employee(rows)
    return _scd2_upsert(conn, "dim_employee", "employee_id", ["department", "role", "salary"], built)


def load_dim_equipment(conn, rows: list[dict]) -> dict[str, int]:
    built = build_dim_equipment(rows)
    return _scd2_upsert(conn, "dim_equipment", "equipment_id", ["status", "equipment_type", "manufacturer"], built)


def load_dim_project(conn, rows: list[dict], location_map: dict[str, int]) -> dict[str, int]:
    built = build_dim_project(rows, location_map)
    return _scd2_upsert(conn, "dim_project", "project_id", ["project_name", "status", "budget", "project_type"], built)


def load_dim_risk(conn, rows: list[dict]) -> dict[str, int]:
    built = build_dim_risk(rows)
    return _scd1_upsert(conn, "dim_risk", "risk_id", built)


def load_fact_cost(conn, rows: list[dict], project_map: dict[str, int], vendor_map: dict[str, int]) -> int:
    built = build_fact_cost(rows, project_map, vendor_map)
    if not built:
        return 0
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.fact_cost (date_key, project_key, vendor_key, planned_cost, actual_cost, cost_variance, forecast_cost) VALUES %s ON CONFLICT DO NOTHING",
            [[r["date_key"], r["project_key"], r["vendor_key"], r["planned_cost"], r["actual_cost"], r["cost_variance"], r["forecast_cost"]] for r in built],
        )
        conn.commit()
    return len(built)


def load_fact_schedule(conn, rows: list[dict], project_map: dict[str, int]) -> int:
    built = build_fact_schedule(rows, project_map)
    if not built:
        return 0
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.fact_schedule (date_key, project_key, planned_progress, actual_progress, schedule_variance, spi) VALUES %s ON CONFLICT DO NOTHING",
            [[r["date_key"], r["project_key"], r["planned_progress"], r["actual_progress"], r["schedule_variance"], r["spi"]] for r in built],
        )
        conn.commit()
    return len(built)


def load_fact_maintenance(conn, rows: list[dict], equipment_map: dict[str, int]) -> int:
    built = build_fact_maintenance(rows, equipment_map)
    if not built:
        return 0
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.fact_maintenance (date_key, equipment_key, maintenance_type, downtime_hours, maintenance_cost) VALUES %s ON CONFLICT DO NOTHING",
            [[r["date_key"], r["equipment_key"], r["maintenance_type"], r["downtime_hours"], r["maintenance_cost"]] for r in built],
        )
        conn.commit()
    return len(built)


def load_fact_workforce(conn, rows: list[dict], employee_map: dict[str, int], project_map: dict[str, int]) -> int:
    built = build_fact_workforce(rows, employee_map, project_map)
    if not built:
        return 0
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.fact_workforce (date_key, employee_key, project_key, hours_worked, productivity_score) VALUES %s ON CONFLICT DO NOTHING",
            [[r["date_key"], r["employee_key"], r["project_key"], r["hours_worked"], r["productivity_score"]] for r in built],
        )
        conn.commit()
    return len(built)


def load_fact_risk(conn, rows: list[dict], project_map: dict[str, int], risk_map: dict[str, int]) -> int:
    built = build_fact_risk(rows, project_map, risk_map)
    if not built:
        return 0
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO curated.fact_risk (date_key, project_key, risk_key, probability, severity_score, impact_cost, impact_days, risk_score) VALUES %s ON CONFLICT DO NOTHING",
            [[r["date_key"], r["project_key"], r["risk_key"], r["probability"], r["severity_score"], r["impact_cost"], r["impact_days"], r["risk_score"]] for r in built],
        )
        conn.commit()
    return len(built)
