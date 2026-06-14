def build_dim_employee(rows: list[dict]) -> list[dict]:
    return [
        {
            "employee_id": r["employee_id"],
            "full_name": r["full_name"],
            "role": r["role"],
            "department": r["department"],
            "hire_date": r["hire_date"],
            "salary": r.get("salary", 0),
        }
        for r in rows
    ]
