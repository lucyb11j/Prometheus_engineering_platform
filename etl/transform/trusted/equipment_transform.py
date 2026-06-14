from datetime import date
from etl.transform.trusted.utils import safe_str, normalize_status, VALID_EQUIPMENT_STATUSES


def transform_equipment(rows: list[dict]) -> list[dict]:
    today = date.today()
    result = []
    for r in rows:
        eid = safe_str(r.get("equipment_id"))
        name = safe_str(r.get("equipment_name"))
        if not eid or not name:
            continue

        etype = safe_str(r.get("equipment_type"))
        status = normalize_status(r.get("status")) or ""
        purchase = r.get("purchase_date")

        if isinstance(purchase, str):
            from datetime import datetime
            purchase = datetime.strptime(purchase, "%Y-%m-%d").date()

        status_valid = status in VALID_EQUIPMENT_STATUSES
        purchase_valid = True
        if purchase and purchase > today:
            purchase_valid = False

        result.append({
            "equipment_id": eid,
            "equipment_name": name,
            "equipment_type": etype,
            "status": status,
            "purchase_date": purchase,
            "status_valid": status_valid,
            "purchase_date_valid": purchase_valid,
        })
    return result
