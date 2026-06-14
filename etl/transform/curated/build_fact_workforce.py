def build_fact_workforce(rows: list[dict], employee_map: dict[str, int], project_map: dict[str, int]) -> list[dict]:
    result = []
    for r in rows:
        date_key = int(r["report_date"].strftime("%Y%m%d"))
        emp_key = employee_map.get(r["employee_id"])
        proj_key = project_map.get(r["project_id"])
        if emp_key is None or proj_key is None:
            continue
        result.append({
            "date_key": date_key,
            "employee_key": emp_key,
            "project_key": proj_key,
            "hours_worked": r["hours_worked"],
            "productivity_score": r["productivity_score"],
        })
    return result
