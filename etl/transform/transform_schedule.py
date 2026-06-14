from datetime import datetime


def transform_schedule(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "project_id": r["project_id"].strip(),
            "report_date": datetime.strptime(r["report_date"], "%Y-%m-%d").date(),
            "planned_progress": float(r["planned_progress"]),
            "actual_progress": float(r["actual_progress"]),
        })
    return transformed
