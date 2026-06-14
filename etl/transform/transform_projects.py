from datetime import datetime


def transform_projects(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "project_id": r["project_id"].strip(),
            "project_name": r["project_name"].strip(),
            "project_type": r["project_type"].strip(),
            "status": r["status"].strip(),
            "start_date": datetime.strptime(r["start_date"], "%Y-%m-%d").date(),
            "end_date": datetime.strptime(r["end_date"], "%Y-%m-%d").date(),
            "budget": float(r["budget"]),
        })
    return transformed
