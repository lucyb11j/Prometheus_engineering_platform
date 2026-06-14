from datetime import date
from etl.transform.trusted.utils import safe_str, safe_float


def transform_employee(rows: list[dict]) -> list[dict]:
    today = date.today()
    result = []
    for r in rows:
        eid = safe_str(r.get("employee_id"))
        name = safe_str(r.get("full_name"))
        if not eid or not name:
            continue

        dept = safe_str(r.get("department"))
        role = safe_str(r.get("role"))
        hire = r.get("hire_date")
        salary = safe_float(r.get("salary"))

        if isinstance(hire, str):
            from datetime import datetime
            hire = datetime.strptime(hire, "%Y-%m-%d").date()

        hire_valid = True
        if hire and hire > today:
            hire_valid = False

        salary_valid = salary > 0

        result.append({
            "employee_id": eid,
            "full_name": name,
            "department": dept,
            "role": role,
            "hire_date": hire,
            "salary": salary,
            "hire_date_valid": hire_valid,
            "salary_valid": salary_valid,
        })
    return result
