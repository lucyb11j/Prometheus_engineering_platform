import sys
import time
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl.config.database import config
from etl.extract import (
    extract_projects, extract_costs, extract_schedule,
    extract_maintenance, extract_risks, extract_vendors,
    extract_employees, extract_equipment, extract_locations,
    extract_workforce,
)
from etl.transform import (
    transform_projects, transform_costs, transform_schedule,
    transform_maintenance, transform_risks, transform_vendors,
    transform_employees, transform_equipment, transform_locations,
    transform_workforce,
)
from etl.load import load_raw, load_trusted
from etl.load.load_curated import (
    _ensure_curated_tables,
    load_dim_date, load_dim_location, load_dim_vendor,
    load_dim_employee, load_dim_equipment, load_dim_project,
    load_dim_risk,
    load_fact_cost, load_fact_schedule, load_fact_maintenance,
    load_fact_workforce, load_fact_risk,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(Path(config.LOG_DIR) / "etl.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("etl")


def extract_all() -> dict:
    log.info("=== EXTRACT phase ===")
    files = config.SOURCE_FILES

    extractors = {
        "projects": (extract_projects, files["projects"]),
        "locations": (extract_locations, files["locations"]),
        "vendors": (extract_vendors, files["vendors"]),
        "employees": (extract_employees, files["employees"]),
        "equipment": (extract_equipment, files["equipment"]),
        "costs": (extract_costs, files["costs"]),
        "schedule": (extract_schedule, files["schedule"]),
        "maintenance": (extract_maintenance, files["maintenance"]),
        "risks": (extract_risks, files["risks"]),
        "workforce": (extract_workforce, files["workforce"]),
    }

    data = {}
    for name, (func, path) in extractors.items():
        log.info("  Extracting %s from %s...", name, path)
        data[name] = func(path)
        log.info("    -> %s records", len(data[name]))
    return data


def transform_all(data: dict) -> dict:
    log.info("=== TRANSFORM phase ===")

    transformers = {
        "projects": (transform_projects, data["projects"]),
        "locations": (transform_locations, data["locations"]),
        "vendors": (transform_vendors, data["vendors"]),
        "employees": (transform_employees, data["employees"]),
        "equipment": (transform_equipment, data["equipment"]),
        "costs": (transform_costs, data["costs"]),
        "schedule": (transform_schedule, data["schedule"]),
        "maintenance": (transform_maintenance, data["maintenance"]),
        "risks": (transform_risks, data["risks"]),
        "workforce": (transform_workforce, data["workforce"]),
    }

    transformed = {}
    for name, (func, rows) in transformers.items():
        log.info("  Transforming %s...", name)
        transformed[name] = func(rows)
        log.info("    -> %s records", len(transformed[name]))
    return transformed


def load_raw_all(data: dict) -> dict[str, int]:
    log.info("=== LOAD (raw) phase ===")
    counts = {}
    for name in ["projects", "locations", "vendors", "employees", "equipment", "costs", "schedule", "maintenance", "risks", "workforce"]:
        log.info("  Loading %s into raw.%s...", name, name)
        counts[name] = load_raw(name, data[name])
        log.info("    -> %s rows inserted", counts[name])
    return counts


def load_trusted_all(data: dict) -> dict[str, int]:
    log.info("=== LOAD (trusted) phase ===")
    counts = {}
    loaders = ["projects", "locations", "vendors", "employees", "equipment", "costs", "schedule", "maintenance", "risks", "workforce"]
    for name in loaders:
        log.info("  Loading %s into trusted...", name)
        cnt = load_trusted(name, data[name])
        log.info("    -> %s rows", cnt)
        counts[name] = cnt
    return counts


def load_curated_all(data: dict) -> dict[str, int]:
    import psycopg2

    log.info("=== LOAD (curated) phase ===")
    conn = psycopg2.connect(config.DB.dsn)
    try:
        _ensure_curated_tables(conn)

        log.info("  Loading dim_date...")
        load_dim_date(conn)

        log.info("  Loading dim_location...")
        location_map = load_dim_location(conn, data["locations"])
        log.info("    -> %s locations", len(location_map))

        log.info("  Loading dim_vendor...")
        vendor_map = load_dim_vendor(conn, data["vendors"])
        log.info("    -> %s vendors", len(vendor_map))

        log.info("  Loading dim_employee...")
        employee_map = load_dim_employee(conn, data["employees"])
        log.info("    -> %s employees", len(employee_map))

        log.info("  Loading dim_equipment...")
        equipment_map = load_dim_equipment(conn, data["equipment"])
        log.info("    -> %s equipment", len(equipment_map))

        log.info("  Loading dim_project...")
        project_map = load_dim_project(conn, data["projects"], location_map)
        log.info("    -> %s projects", len(project_map))

        log.info("  Loading dim_risk...")
        risk_map = load_dim_risk(conn, data["risks"])
        log.info("    -> %s risks", len(risk_map))

        log.info("  Loading fact_cost...")
        cost_count = load_fact_cost(conn, data["costs"], project_map, vendor_map)
        log.info("    -> %s rows", cost_count)

        log.info("  Loading fact_schedule...")
        sched_count = load_fact_schedule(conn, data["schedule"], project_map)
        log.info("    -> %s rows", sched_count)

        log.info("  Loading fact_maintenance...")
        maint_count = load_fact_maintenance(conn, data["maintenance"], equipment_map)
        log.info("    -> %s rows", maint_count)

        log.info("  Loading fact_workforce...")
        workforce_count = load_fact_workforce(conn, data["workforce"], employee_map, project_map)
        log.info("    -> %s rows", workforce_count)

        log.info("  Loading fact_risk...")
        risk_count = load_fact_risk(conn, data["risks"], project_map, risk_map)
        log.info("    -> %s rows", risk_count)

        return {
            "dim_date": 730,
            "dim_location": len(location_map),
            "dim_vendor": len(vendor_map),
            "dim_employee": len(employee_map),
            "dim_equipment": len(equipment_map),
            "dim_project": len(project_map),
            "dim_risk": len(risk_map),
            "fact_cost": cost_count,
            "fact_schedule": sched_count,
            "fact_maintenance": maint_count,
            "fact_workforce": workforce_count,
            "fact_risk": risk_count,
        }
    finally:
        conn.close()


def run_pipeline(stages: list[str] | None = None) -> int:
    start = time.time()
    log.info("=" * 50)
    log.info("ETL Pipeline started")
    log.info("=" * 50)

    stages = stages or ["extract", "transform", "load_raw", "load_trusted", "load_curated"]
    data = {}
    transformed = {}

    if "extract" in stages:
        data = extract_all()
    if "transform" in stages:
        transformed = transform_all(data)
    else:
        transformed = data
    if "load_raw" in stages:
        load_raw_all(transformed)
    if "load_trusted" in stages:
        load_trusted_all(transformed)
    if "load_curated" in stages:
        load_curated_all(transformed)

    elapsed = time.time() - start
    log.info("=" * 50)
    log.info("ETL Pipeline completed in %.2f seconds", elapsed)
    log.info("=" * 50)
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Engineering Platform ETL Pipeline")
    parser.add_argument(
        "--stages",
        nargs="+",
        choices=["extract", "transform", "load_raw", "load_trusted", "load_curated"],
        default=None,
        help="Stages to run (default: all)",
    )
    args = parser.parse_args()
    sys.exit(run_pipeline(args.stages))
