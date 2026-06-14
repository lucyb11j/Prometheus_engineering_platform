def build_fact_maintenance(rows: list[dict], equipment_map: dict[str, int]) -> list[dict]:
    result = []
    for r in rows:
        date_key = int(r["maintenance_date"].strftime("%Y%m%d"))
        eq_key = equipment_map.get(r["equipment_id"])
        if eq_key is None:
            continue
        result.append({
            "date_key": date_key,
            "equipment_key": eq_key,
            "maintenance_type": r["maintenance_type"],
            "downtime_hours": r["downtime_hours"],
            "maintenance_cost": r["maintenance_cost"],
        })
    return result
