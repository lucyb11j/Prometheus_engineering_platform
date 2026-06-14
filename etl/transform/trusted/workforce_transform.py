from datetime import date
from etl.transform.trusted.utils import safe_str, safe_float


def transform_workforce(rows: list[dict]) -> list[dict]:
    result = []
    for r in rows:
        eid = safe_str(r.get("employee_id"))
        pid = safe_str(r.get("project_id"))
        if not eid or not pid:
            continue

        hours = safe_float(r.get("hours_worked"))
        prod = safe_float(r.get("productivity_score"))
        report_date = r.get("report_date")

        hours_valid = 0 < hours <= 24
        prod_valid = 0 <= prod <= 1

        result.append({
            "employee_id": eid,
            "project_id": pid,
            "report_date": report_date,
            "hours_worked": hours,
            "productivity_score": prod,
            "hours_valid": hours_valid,
            "productivity_valid": prod_valid,
        })
    return result
