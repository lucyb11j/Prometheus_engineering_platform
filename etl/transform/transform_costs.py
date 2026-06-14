from datetime import datetime


def transform_costs(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "project_id": r["project_id"].strip(),
            "vendor_id": r["vendor_id"].strip(),
            "cost_date": datetime.strptime(r["cost_date"], "%Y-%m-%d").date(),
            "planned_cost": float(r["planned_cost"]),
            "actual_cost": float(r["actual_cost"]),
        })
    return transformed
