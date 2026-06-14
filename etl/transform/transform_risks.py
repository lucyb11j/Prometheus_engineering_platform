from datetime import datetime


def transform_risks(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        risk_date = r.get("risk_date", "").strip()
        transformed.append({
            "risk_id": r["risk_id"].strip(),
            "project_id": r["project_id"].strip(),
            "risk_description": r.get("risk_description", "").strip(),
            "probability": float(r["probability"]),
            "severity": int(r["severity"]),
            "impact_cost": float(r["impact_cost"]),
            "impact_days": int(r["impact_days"]),
            "risk_date": datetime.strptime(risk_date, "%Y-%m-%d").date() if risk_date else None,
        })
    return transformed
