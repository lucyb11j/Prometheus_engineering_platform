import psycopg2
from psycopg2.extras import execute_values
from datetime import date, datetime
from typing import Any

from etl.config.database import config
from etl.transform.trusted import (
    transform_project,
    transform_location,
    transform_vendor,
    transform_employee,
    transform_equipment,
    transform_cost,
    transform_schedule,
    transform_maintenance,
    transform_risk,
    transform_workforce,
)


def _insert_audit_log(conn, pipeline: str, status: str, rows: int, error: str | None = None):
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO audit.etl_execution_log
               (pipeline_name, start_time, end_time, status, rows_processed, error_message)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (pipeline, datetime.now(), datetime.now(), status, rows, error),
        )
        conn.commit()


def _insert_rejected(conn, source: str, records: list[tuple[str, str]]):
    if not records:
        return
    with conn.cursor() as cur:
        execute_values(
            cur,
            """INSERT INTO audit.rejected_records
               (source_table, record_id, rejection_reason, rejected_at)
               VALUES %s""",
            [[s, rid, reason, datetime.now()] for s, rid, reason in records],
        )
        conn.commit()


def _ensure_trusted_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS audit.rejected_records (
                rejection_id BIGSERIAL PRIMARY KEY,
                source_table VARCHAR(100) NOT NULL,
                record_id VARCHAR(200),
                rejection_reason TEXT,
                rejected_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.project (
                project_id VARCHAR(50) PRIMARY KEY,
                project_name VARCHAR(200),
                project_type VARCHAR(100),
                status VARCHAR(50),
                start_date DATE,
                end_date DATE,
                budget NUMERIC(18,2),
                budget_valid BOOLEAN DEFAULT TRUE,
                status_valid BOOLEAN DEFAULT TRUE,
                date_valid BOOLEAN DEFAULT TRUE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.location (
                location_id VARCHAR(50) PRIMARY KEY,
                country VARCHAR(100),
                region VARCHAR(100),
                city VARCHAR(100),
                site_name VARCHAR(200)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.vendor (
                vendor_id VARCHAR(50) PRIMARY KEY,
                vendor_name VARCHAR(200),
                category VARCHAR(100),
                country VARCHAR(100),
                category_valid BOOLEAN DEFAULT TRUE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.employee (
                employee_id VARCHAR(50) PRIMARY KEY,
                full_name VARCHAR(200),
                department VARCHAR(100),
                role VARCHAR(100),
                hire_date DATE,
                salary NUMERIC(12,2) DEFAULT 0,
                hire_date_valid BOOLEAN DEFAULT TRUE,
                salary_valid BOOLEAN DEFAULT TRUE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.equipment (
                equipment_id VARCHAR(50) PRIMARY KEY,
                equipment_name VARCHAR(200),
                equipment_type VARCHAR(100),
                status VARCHAR(50),
                purchase_date DATE,
                status_valid BOOLEAN DEFAULT TRUE,
                purchase_date_valid BOOLEAN DEFAULT TRUE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.cost (
                project_id VARCHAR(50),
                vendor_id VARCHAR(50) DEFAULT '',
                cost_date DATE,
                planned_cost NUMERIC(18,2) DEFAULT 0,
                actual_cost NUMERIC(18,2) DEFAULT 0,
                cost_variance NUMERIC(18,2) DEFAULT 0,
                variance_pct NUMERIC(10,4),
                planned_valid BOOLEAN DEFAULT TRUE,
                actual_valid BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (project_id, vendor_id, cost_date)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.schedule (
                project_id VARCHAR(50),
                report_date DATE,
                planned_progress NUMERIC(8,2) DEFAULT 0,
                actual_progress NUMERIC(8,2) DEFAULT 0,
                schedule_variance NUMERIC(8,2) DEFAULT 0,
                spi NUMERIC(8,4),
                is_behind_schedule BOOLEAN DEFAULT FALSE,
                planned_valid BOOLEAN DEFAULT TRUE,
                actual_valid BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (project_id, report_date)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.maintenance (
                equipment_id VARCHAR(50),
                maintenance_date DATE,
                maintenance_type VARCHAR(100),
                maintenance_type_normalized VARCHAR(100),
                downtime_hours NUMERIC(10,2) DEFAULT 0,
                maintenance_cost NUMERIC(18,2) DEFAULT 0,
                type_valid BOOLEAN DEFAULT TRUE,
                downtime_valid BOOLEAN DEFAULT TRUE,
                cost_valid BOOLEAN DEFAULT TRUE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.risk (
                risk_id VARCHAR(50) PRIMARY KEY,
                project_id VARCHAR(50),
                risk_description TEXT,
                probability NUMERIC(5,2) DEFAULT 0,
                severity INTEGER DEFAULT 0,
                impact_cost NUMERIC(18,2) DEFAULT 0,
                impact_days INTEGER DEFAULT 0,
                risk_score NUMERIC(10,2) DEFAULT 0,
                prob_valid BOOLEAN DEFAULT TRUE,
                severity_valid BOOLEAN DEFAULT TRUE,
                impact_valid BOOLEAN DEFAULT TRUE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trusted.workforce (
                employee_id VARCHAR(50),
                project_id VARCHAR(50),
                report_date DATE,
                hours_worked NUMERIC(10,2) DEFAULT 0,
                productivity_score NUMERIC(8,2) DEFAULT 0,
                hours_valid BOOLEAN DEFAULT TRUE,
                productivity_valid BOOLEAN DEFAULT TRUE,
                PRIMARY KEY (employee_id, project_id, report_date)
            )
        """)
        conn.commit()


# ============================================================
#  PROJECT  trusted.project
# ============================================================
def load_trusted_project(conn, rows: list[dict]) -> int:
    trusted = transform_project(rows)
    rejected: list[tuple[str, str]] = []
    processed = set()
    to_insert = []
    for t in trusted:
        pid = t["project_id"]
        if pid in processed:
            rejected.append(("project", pid, "Duplicate project_id"))
            continue
        processed.add(pid)
        if not t.get("budget_valid"):
            rejected.append(("project", pid, "Budget must be positive"))
        if not t.get("status_valid"):
            rejected.append(("project", pid, f"Invalid status: {t.get('status')}"))
        if not t.get("date_valid"):
            rejected.append(("project", pid, "End date must be after start date"))
        to_insert.append(t)
    if to_insert:
        deduped: dict[str, dict] = {}
        for t in to_insert:
            pid = t["project_id"]
            if pid not in deduped or (t["end_date"] or date.min) > (deduped[pid]["end_date"] or date.min):
                deduped[pid] = t
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.project
                   (project_id, project_name, project_type, status, start_date, end_date, budget, budget_valid, status_valid, date_valid)
                   VALUES %s
                   ON CONFLICT (project_id) DO UPDATE SET
                     project_name = EXCLUDED.project_name,
                     project_type = EXCLUDED.project_type,
                     status = EXCLUDED.status,
                     start_date = EXCLUDED.start_date,
                     end_date = EXCLUDED.end_date,
                     budget = EXCLUDED.budget,
                     budget_valid = EXCLUDED.budget_valid,
                     status_valid = EXCLUDED.status_valid,
                     date_valid = EXCLUDED.date_valid
                """,
                [[t["project_id"], t["project_name"], t["project_type"],
                  t["status"], t["start_date"], t["end_date"],
                  t["budget"], t["budget_valid"], t["status_valid"], t["date_valid"]]
                 for t in deduped.values()]
            )
            conn.commit()
    _insert_rejected(conn, "project", rejected)
    return len(deduped) if to_insert else 0


# ============================================================
#  LOCATION  trusted.location
# ============================================================
def load_trusted_location(conn, rows: list[dict]) -> int:
    trusted = transform_location(rows)
    seen = set()
    to_insert = []
    for t in trusted:
        lid = t["location_id"]
        if lid in seen:
            continue
        seen.add(lid)
        to_insert.append(t)
    if not to_insert:
        return 0
    with conn.cursor() as cur:
        execute_values(
            cur,
            """INSERT INTO trusted.location (location_id, country, region, city, site_name)
               VALUES %s
               ON CONFLICT (location_id) DO UPDATE SET
                 country = EXCLUDED.country, region = EXCLUDED.region,
                 city = EXCLUDED.city, site_name = EXCLUDED.site_name
            """,
            [[t["location_id"], t["country"], t["region"], t["city"], t["site_name"]] for t in to_insert]
        )
        conn.commit()
    return len(to_insert)


# ============================================================
#  VENDOR  trusted.vendor
# ============================================================
def load_trusted_vendor(conn, rows: list[dict]) -> int:
    trusted = transform_vendor(rows)
    rejected = []
    seen = set()
    to_insert = []
    for t in trusted:
        vid = t["vendor_id"]
        if vid in seen:
            rejected.append(("vendor", vid, "Duplicate vendor_id"))
            continue
        seen.add(vid)
        if not t.get("category_valid"):
            rejected.append(("vendor", vid, f"Invalid category: {t.get('category')}"))
        to_insert.append(t)
    if to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.vendor (vendor_id, vendor_name, category, country, category_valid)
                   VALUES %s
                   ON CONFLICT (vendor_id) DO UPDATE SET
                     vendor_name = EXCLUDED.vendor_name, category = EXCLUDED.category,
                     country = EXCLUDED.country, category_valid = EXCLUDED.category_valid
                """,
                [[t["vendor_id"], t["vendor_name"], t["category"], t["country"], t["category_valid"]] for t in to_insert]
            )
            conn.commit()
    _insert_rejected(conn, "vendor", rejected)
    return len(to_insert)


# ============================================================
#  EMPLOYEE  trusted.employee
# ============================================================
def load_trusted_employee(conn, rows: list[dict]) -> int:
    trusted = transform_employee(rows)
    rejected = []
    seen = set()
    to_insert = []
    for t in trusted:
        eid = t["employee_id"]
        if eid in seen:
            rejected.append(("employee", eid, "Duplicate employee_id"))
            continue
        seen.add(eid)
        if not t.get("hire_date_valid"):
            rejected.append(("employee", eid, "Hire date cannot be in the future"))
        if not t.get("salary_valid"):
            rejected.append(("employee", eid, "Salary must be > 0"))
        to_insert.append(t)
    if to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.employee
                   (employee_id, full_name, department, role, hire_date, salary, hire_date_valid, salary_valid)
                   VALUES %s
                   ON CONFLICT (employee_id) DO UPDATE SET
                     full_name = EXCLUDED.full_name, department = EXCLUDED.department,
                     role = EXCLUDED.role, hire_date = EXCLUDED.hire_date,
                     salary = EXCLUDED.salary, hire_date_valid = EXCLUDED.hire_date_valid,
                     salary_valid = EXCLUDED.salary_valid
                """,
                [[t["employee_id"], t["full_name"], t["department"], t["role"],
                  t["hire_date"], t["salary"], t["hire_date_valid"], t["salary_valid"]] for t in to_insert]
            )
            conn.commit()
    _insert_rejected(conn, "employee", rejected)
    return len(to_insert)


# ============================================================
#  EQUIPMENT  trusted.equipment
# ============================================================
def load_trusted_equipment(conn, rows: list[dict]) -> int:
    trusted = transform_equipment(rows)
    rejected = []
    seen = set()
    to_insert = []
    for t in trusted:
        eid = t["equipment_id"]
        if eid in seen:
            rejected.append(("equipment", eid, "Duplicate equipment_id"))
            continue
        seen.add(eid)
        if not t.get("status_valid"):
            rejected.append(("equipment", eid, f"Invalid status: {t.get('status')}"))
        if not t.get("purchase_date_valid"):
            rejected.append(("equipment", eid, "Purchase date cannot be in the future"))
        to_insert.append(t)
    if to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.equipment
                   (equipment_id, equipment_name, equipment_type, status, purchase_date, status_valid, purchase_date_valid)
                   VALUES %s
                   ON CONFLICT (equipment_id) DO UPDATE SET
                     equipment_name = EXCLUDED.equipment_name, equipment_type = EXCLUDED.equipment_type,
                     status = EXCLUDED.status, purchase_date = EXCLUDED.purchase_date,
                     status_valid = EXCLUDED.status_valid, purchase_date_valid = EXCLUDED.purchase_date_valid
                """,
                [[t["equipment_id"], t["equipment_name"], t["equipment_type"],
                  t["status"], t["purchase_date"], t["status_valid"], t["purchase_date_valid"]] for t in to_insert]
            )
            conn.commit()
    _insert_rejected(conn, "equipment", rejected)
    return len(to_insert)


# ============================================================
#  COST  trusted.cost
# ============================================================
def load_trusted_cost(conn, rows: list[dict]) -> int:
    trusted = transform_cost(rows)
    rejected = []
    seen = set()
    to_insert = []
    for t in trusted:
        key = (t["project_id"], t.get("vendor_id", ""), str(t["cost_date"]))
        if key in seen:
            rejected.append(("cost", f"{t['project_id']}/{t['cost_date']}", "Duplicate cost record"))
            continue
        seen.add(key)
        if not t.get("planned_valid"):
            rejected.append(("cost", t["project_id"], "planned_cost must be >= 0"))
        if not t.get("actual_valid"):
            rejected.append(("cost", t["project_id"], "actual_cost must be >= 0"))
        to_insert.append(t)
    if to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.cost
                   (project_id, vendor_id, cost_date, planned_cost, actual_cost, cost_variance, variance_pct, planned_valid, actual_valid)
                   VALUES %s
                   ON CONFLICT (project_id, vendor_id, cost_date) DO UPDATE SET
                     planned_cost = EXCLUDED.planned_cost, actual_cost = EXCLUDED.actual_cost,
                     cost_variance = EXCLUDED.cost_variance, variance_pct = EXCLUDED.variance_pct,
                     planned_valid = EXCLUDED.planned_valid, actual_valid = EXCLUDED.actual_valid
                """,
                [[t["project_id"], t["vendor_id"], t["cost_date"],
                  t["planned_cost"], t["actual_cost"], t["cost_variance"],
                  t["variance_pct"], t["planned_valid"], t["actual_valid"]] for t in to_insert]
            )
            conn.commit()
    _insert_rejected(conn, "cost", rejected)
    return len(to_insert)


# ============================================================
#  SCHEDULE  trusted.schedule
# ============================================================
def load_trusted_schedule(conn, rows: list[dict]) -> int:
    trusted = transform_schedule(rows)
    rejected = []
    seen = set()
    to_insert = []
    for t in trusted:
        key = (t["project_id"], str(t["report_date"]))
        if key in seen:
            rejected.append(("schedule", f"{t['project_id']}/{t['report_date']}", "Duplicate schedule record"))
            continue
        seen.add(key)
        if not t.get("planned_valid"):
            rejected.append(("schedule", t["project_id"], "planned_progress must be between 0 and 100"))
        if not t.get("actual_valid"):
            rejected.append(("schedule", t["project_id"], "actual_progress must be between 0 and 100"))
        to_insert.append(t)
    if to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.schedule
                   (project_id, report_date, planned_progress, actual_progress, schedule_variance, spi, is_behind_schedule, planned_valid, actual_valid)
                   VALUES %s
                   ON CONFLICT (project_id, report_date) DO UPDATE SET
                     planned_progress = EXCLUDED.planned_progress,
                     actual_progress = EXCLUDED.actual_progress,
                     schedule_variance = EXCLUDED.schedule_variance,
                     spi = EXCLUDED.spi,
                     is_behind_schedule = EXCLUDED.is_behind_schedule,
                     planned_valid = EXCLUDED.planned_valid,
                     actual_valid = EXCLUDED.actual_valid
                """,
                [[t["project_id"], t["report_date"],
                  t["planned_progress"], t["actual_progress"],
                  t["schedule_variance"], t["spi"], t["is_behind_schedule"],
                  t["planned_valid"], t["actual_valid"]] for t in to_insert]
            )
            conn.commit()
    _insert_rejected(conn, "schedule", rejected)
    return len(to_insert)


# ============================================================
#  MAINTENANCE  trusted.maintenance
# ============================================================
def load_trusted_maintenance(conn, rows: list[dict]) -> int:
    trusted = transform_maintenance(rows)
    rejected = []
    seen = set()
    to_insert = []
    for t in trusted:
        key = (t["equipment_id"], str(t["maintenance_date"]), t.get("maintenance_type", ""))
        if key in seen:
            rejected.append(("maintenance", t["equipment_id"], "Duplicate maintenance record"))
            continue
        seen.add(key)
        if not t.get("type_valid"):
            rejected.append(("maintenance", t["equipment_id"], f"Invalid type: {t.get('maintenance_type')}"))
        if not t.get("downtime_valid"):
            rejected.append(("maintenance", t["equipment_id"], "downtime_hours must be >= 0"))
        if not t.get("cost_valid"):
            rejected.append(("maintenance", t["equipment_id"], "maintenance_cost must be >= 0"))
        to_insert.append(t)
    if to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.maintenance
                   (equipment_id, maintenance_date, maintenance_type, maintenance_type_normalized, downtime_hours, maintenance_cost, type_valid, downtime_valid, cost_valid)
                   VALUES %s
                """,
                [[t["equipment_id"], t["maintenance_date"], t["maintenance_type"],
                  t["maintenance_type_normalized"], t["downtime_hours"], t["maintenance_cost"],
                  t["type_valid"], t["downtime_valid"], t["cost_valid"]] for t in to_insert]
            )
            conn.commit()
    _insert_rejected(conn, "maintenance", rejected)
    return len(to_insert)


# ============================================================
#  RISK  trusted.risk
# ============================================================
def load_trusted_risk(conn, rows: list[dict]) -> int:
    trusted = transform_risk(rows)
    rejected = []
    seen = set()
    to_insert = []
    for t in trusted:
        rid = t["risk_id"]
        if rid in seen:
            rejected.append(("risk", rid, "Duplicate risk_id"))
            continue
        seen.add(rid)
        if not t.get("prob_valid"):
            rejected.append(("risk", rid, "probability must be between 0 and 1"))
        if not t.get("severity_valid"):
            rejected.append(("risk", rid, "severity must be between 1 and 10"))
        if not t.get("impact_valid"):
            rejected.append(("risk", rid, "impact_cost must be >= 0"))
        to_insert.append(t)
    if to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.risk
                   (risk_id, project_id, risk_description, probability, severity, impact_cost, impact_days, risk_score, prob_valid, severity_valid, impact_valid)
                   VALUES %s
                   ON CONFLICT (risk_id) DO UPDATE SET
                     project_id = EXCLUDED.project_id,
                     risk_description = EXCLUDED.risk_description,
                     probability = EXCLUDED.probability, severity = EXCLUDED.severity,
                     impact_cost = EXCLUDED.impact_cost, impact_days = EXCLUDED.impact_days,
                     risk_score = EXCLUDED.risk_score,
                     prob_valid = EXCLUDED.prob_valid, severity_valid = EXCLUDED.severity_valid,
                     impact_valid = EXCLUDED.impact_valid
                """,
                [[t["risk_id"], t["project_id"], t["risk_description"],
                  t["probability"], t["severity"], t["impact_cost"],
                  t["impact_days"], t["risk_score"],
                  t["prob_valid"], t["severity_valid"], t["impact_valid"]] for t in to_insert]
            )
            conn.commit()
    _insert_rejected(conn, "risk", rejected)
    return len(to_insert)


# ============================================================
#  WORKFORCE  trusted.workforce
# ============================================================
def load_trusted_workforce(conn, rows: list[dict]) -> int:
    trusted = transform_workforce(rows)
    rejected = []
    seen = set()
    to_insert = []
    for t in trusted:
        key = (t["employee_id"], t["project_id"], str(t["report_date"]))
        if key in seen:
            rejected.append(("workforce", f"{t['employee_id']}/{t['project_id']}/{t['report_date']}", "Duplicate workforce record"))
            continue
        seen.add(key)
        if not t.get("hours_valid"):
            rejected.append(("workforce", t["employee_id"], "hours_worked must be between 0 and 24"))
        if not t.get("productivity_valid"):
            rejected.append(("workforce", t["employee_id"], "productivity_score must be between 0 and 1"))
        to_insert.append(t)
    if to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """INSERT INTO trusted.workforce
                   (employee_id, project_id, report_date, hours_worked, productivity_score, hours_valid, productivity_valid)
                   VALUES %s
                   ON CONFLICT (employee_id, project_id, report_date) DO UPDATE SET
                     hours_worked = EXCLUDED.hours_worked,
                     productivity_score = EXCLUDED.productivity_score,
                     hours_valid = EXCLUDED.hours_valid,
                     productivity_valid = EXCLUDED.productivity_valid
                """,
                [[t["employee_id"], t["project_id"], t["report_date"],
                  t["hours_worked"], t["productivity_score"],
                  t["hours_valid"], t["productivity_valid"]] for t in to_insert]
            )
            conn.commit()
    _insert_rejected(conn, "workforce", rejected)
    return len(to_insert)


# ============================================================
#  GENERIC DISPATCHER
# ============================================================
TRUSTED_LOADERS = {
    "projects": load_trusted_project,
    "locations": load_trusted_location,
    "vendors": load_trusted_vendor,
    "employees": load_trusted_employee,
    "equipment": load_trusted_equipment,
    "costs": load_trusted_cost,
    "schedule": load_trusted_schedule,
    "maintenance": load_trusted_maintenance,
    "risks": load_trusted_risk,
    "workforce": load_trusted_workforce,
}


def load_trusted(table_name: str, rows: list[dict[str, Any]]) -> int:
    if table_name not in TRUSTED_LOADERS:
        raise ValueError(f"No trusted loader for: {table_name}")
    conn = psycopg2.connect(config.DB.dsn)
    try:
        _ensure_trusted_tables(conn)
        count = TRUSTED_LOADERS[table_name](conn, rows)
        return count
    except Exception as e:
        _insert_audit_log(conn, f"trusted.{table_name}", "FAILED", 0, str(e))
        raise
    finally:
        conn.close()
