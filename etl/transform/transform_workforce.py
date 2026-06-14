from datetime import datetime


def transform_workforce(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "employee_id": r["employee_id"].strip(),
            "project_id": r["project_id"].strip(),
            "report_date": datetime.strptime(r["report_date"], "%Y-%m-%d").date(),
            "hours_worked": float(r["hours_worked"]),
            "productivity_score": float(r["productivity_score"]),
        })
    return transformed
