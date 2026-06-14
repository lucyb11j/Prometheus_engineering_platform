def build_dim_project(rows: list[dict], location_map: dict[str, int]) -> list[dict]:
    result = []
    for r in rows:
        loc_key = location_map.get(r.get("location_id", ""))
        result.append({
            "project_id": r["project_id"],
            "project_name": r["project_name"],
            "project_type": r["project_type"],
            "location_key": loc_key,
            "start_date": r["start_date"],
            "planned_end_date": r["end_date"],
            "status": r["status"],
            "budget": r.get("budget"),
        })
    return result
