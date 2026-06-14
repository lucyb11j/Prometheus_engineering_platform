from datetime import datetime


def transform_employees(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "employee_id": r["employee_id"].strip(),
            "full_name": r["full_name"].strip(),
            "department": r["department"].strip(),
            "role": r["role"].strip(),
            "hire_date": datetime.strptime(r["hire_date"], "%Y-%m-%d").date(),
        })
    return transformed
