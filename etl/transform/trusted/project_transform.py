from datetime import date
from etl.transform.trusted.utils import safe_str, safe_float, normalize_status

VALID_STATUSES = {"Active", "Completed", "Delayed", "Cancelled"}


def transform_project(rows: list[dict]) -> list[dict]:
    result = []
    for r in rows:
        pid = safe_str(r.get("project_id"))
        name = safe_str(r.get("project_name"))
        if not pid or not name:
            continue

        ptype = safe_str(r.get("project_type")).title()
        status = normalize_status(r.get("status")) or ""
        budget = safe_float(r.get("budget"))
        start = r.get("start_date")
        end = r.get("end_date")

        budget_valid = budget > 0
        status_valid = status in VALID_STATUSES
        date_valid = True
        if start and end:
            if isinstance(start, str):
                from datetime import datetime
                start = datetime.strptime(start, "%Y-%m-%d").date()
            if isinstance(end, str):
                from datetime import datetime
                end = datetime.strptime(end, "%Y-%m-%d").date()
            date_valid = start < end

        result.append({
            "project_id": pid,
            "project_name": name,
            "project_type": ptype,
            "status": status,
            "start_date": start,
            "end_date": end,
            "budget": budget,
            "budget_valid": budget_valid,
            "status_valid": status_valid,
            "date_valid": date_valid,
        })
    return result
