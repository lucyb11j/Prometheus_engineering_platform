def build_dim_risk(rows: list[dict]) -> list[dict]:
    return [
        {
            "risk_id": r["risk_id"],
            "risk_name": r.get("risk_description", "")[:200],
            "risk_category": "General",
            "risk_description": r.get("risk_description", ""),
        }
        for r in rows
    ]
