from etl.transform.trusted.utils import safe_str, safe_float


def transform_schedule(rows: list[dict]) -> list[dict]:
    result = []
    for r in rows:
        pid = safe_str(r.get("project_id"))
        rdate = r.get("report_date")
        if not pid or not rdate:
            continue

        if isinstance(rdate, str):
            from datetime import datetime
            rdate = datetime.strptime(rdate, "%Y-%m-%d").date()

        planned = safe_float(r.get("planned_progress"))
        actual = safe_float(r.get("actual_progress"))
        variance = actual - planned
        spi = round(actual / planned, 4) if planned != 0 else None
        is_behind = actual < planned

        planned_valid = 0 <= planned <= 100
        actual_valid = 0 <= actual <= 100

        result.append({
            "project_id": pid,
            "report_date": rdate,
            "planned_progress": planned,
            "actual_progress": actual,
            "schedule_variance": variance,
            "spi": spi,
            "is_behind_schedule": is_behind,
            "planned_valid": planned_valid,
            "actual_valid": actual_valid,
        })
    return result
