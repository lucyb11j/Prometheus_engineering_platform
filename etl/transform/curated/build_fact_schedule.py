def build_fact_schedule(rows: list[dict], project_map: dict[str, int]) -> list[dict]:
    result = []
    for r in rows:
        date_key = int(r["report_date"].strftime("%Y%m%d"))
        proj_key = project_map.get(r["project_id"])
        if proj_key is None:
            continue
        planned = r["planned_progress"]
        actual = r["actual_progress"]
        spi = round(actual / planned, 4) if planned > 0 else None
        result.append({
            "date_key": date_key,
            "project_key": proj_key,
            "planned_progress": planned,
            "actual_progress": actual,
            "schedule_variance": round(actual - planned, 2),
            "spi": spi,
        })
    return result
