from datetime import datetime


def transform_equipment(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        purchase = r.get("purchase_date", "").strip()
        transformed.append({
            "equipment_id": r["equipment_id"].strip(),
            "equipment_name": r["equipment_name"].strip(),
            "equipment_type": r["equipment_type"].strip(),
            "manufacturer": r.get("manufacturer", "").strip(),
            "purchase_date": datetime.strptime(purchase, "%Y-%m-%d").date() if purchase else None,
            "status": r["status"].strip(),
        })
    return transformed
