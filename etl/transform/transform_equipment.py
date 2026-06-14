def transform_equipment(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "equipment_id": r["equipment_id"].strip(),
            "equipment_name": r["equipment_name"].strip(),
            "equipment_type": r["equipment_type"].strip(),
            "status": r["status"].strip(),
        })
    return transformed
