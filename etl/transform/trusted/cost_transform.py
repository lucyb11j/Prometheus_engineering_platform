from etl.transform.trusted.utils import safe_str, safe_float


def transform_cost(rows: list[dict]) -> list[dict]:
    result = []
    for r in rows:
        pid = safe_str(r.get("project_id"))
        cdate = r.get("cost_date")
        if not pid or not cdate:
            continue

        if isinstance(cdate, str):
            from datetime import datetime
            cdate = datetime.strptime(cdate, "%Y-%m-%d").date()

        planned = safe_float(r.get("planned_cost"))
        actual = safe_float(r.get("actual_cost"))
        variance = actual - planned
        var_pct = round(variance / planned, 4) if planned != 0 else None

        planned_valid = planned >= 0
        actual_valid = actual >= 0

        result.append({
            "project_id": pid,
            "vendor_id": safe_str(r.get("vendor_id")),
            "cost_date": cdate,
            "planned_cost": planned,
            "actual_cost": actual,
            "cost_variance": variance,
            "variance_pct": var_pct,
            "planned_valid": planned_valid,
            "actual_valid": actual_valid,
        })
    return result
