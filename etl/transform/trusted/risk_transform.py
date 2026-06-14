from etl.transform.trusted.utils import safe_str, safe_float, safe_int


def transform_risk(rows: list[dict]) -> list[dict]:
    result = []
    for r in rows:
        rid = safe_str(r.get("risk_id"))
        pid = safe_str(r.get("project_id"))
        if not rid or not pid:
            continue

        prob = safe_float(r.get("probability"))
        sev = safe_int(r.get("severity"))
        impact = safe_float(r.get("impact_cost"))
        impact_days = safe_int(r.get("impact_days"))
        risk_score = round(prob * sev, 2)

        prob_valid = 0 <= prob <= 1
        sev_valid = 1 <= sev <= 10
        impact_valid = impact >= 0

        result.append({
            "risk_id": rid,
            "project_id": pid,
            "risk_description": safe_str(r.get("risk_description")),
            "probability": prob,
            "severity": sev,
            "impact_cost": impact,
            "impact_days": impact_days,
            "risk_score": risk_score,
            "prob_valid": prob_valid,
            "severity_valid": sev_valid,
            "impact_valid": impact_valid,
        })
    return result
