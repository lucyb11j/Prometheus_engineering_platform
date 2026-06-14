def build_dim_equipment(rows: list[dict]) -> list[dict]:
    return [
        {
            "equipment_id": r["equipment_id"],
            "equipment_name": r["equipment_name"],
            "equipment_type": r["equipment_type"],
            "manufacturer": r.get("manufacturer"),
            "purchase_date": r.get("purchase_date"),
            "status": r["status"],
        }
        for r in rows
    ]
