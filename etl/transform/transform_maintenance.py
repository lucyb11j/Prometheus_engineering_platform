from datetime import datetime


def transform_maintenance(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "equipment_id": r["equipment_id"].strip(),
            "maintenance_date": datetime.strptime(r["maintenance_date"], "%Y-%m-%d").date(),
            "maintenance_type": r["maintenance_type"].strip(),
            "downtime_hours": float(r["downtime_hours"]),
            "maintenance_cost": float(r["maintenance_cost"]),
        })
    return transformed
