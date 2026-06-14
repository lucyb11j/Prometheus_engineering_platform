def build_fact_risk(rows: list[dict], project_map: dict[str, int], risk_map: dict[str, int]) -> list[dict]:
    result = []
    for r in rows:
        date_key = int(r["risk_date"].strftime("%Y%m%d"))
        proj_key = project_map.get(r["project_id"])
        risk_key = risk_map.get(r["risk_id"])
        if proj_key is None or risk_key is None:
            continue
        risk_score = round(r["probability"] * r["severity"], 2)
        result.append({
            "date_key": date_key,
            "project_key": proj_key,
            "risk_key": risk_key,
            "probability": r["probability"],
            "severity_score": r["severity"],
            "impact_cost": r["impact_cost"],
            "impact_days": r["impact_days"],
            "risk_score": risk_score,
        })
    return result
