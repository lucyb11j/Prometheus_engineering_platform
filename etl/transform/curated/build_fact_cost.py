def build_fact_cost(rows: list[dict], project_map: dict[str, int], vendor_map: dict[str, int]) -> list[dict]:
    result = []
    for r in rows:
        date_key = int(r["cost_date"].strftime("%Y%m%d"))
        proj_key = project_map.get(r["project_id"])
        if proj_key is None:
            continue
        vend_key = vendor_map.get(r.get("vendor_id", ""))
        planned = r["planned_cost"]
        actual = r["actual_cost"]
        result.append({
            "date_key": date_key,
            "project_key": proj_key,
            "vendor_key": vend_key,
            "planned_cost": planned,
            "actual_cost": actual,
            "cost_variance": round(actual - planned, 2),
            "forecast_cost": None,
        })
    return result
