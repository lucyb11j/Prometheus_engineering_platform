from etl.transform.trusted.utils import safe_str, safe_float, normalize_mtype, VALID_MAINTENANCE_TYPES


def transform_maintenance(rows: list[dict]) -> list[dict]:
    result = []
    for r in rows:
        eid = safe_str(r.get("equipment_id"))
        mdate = r.get("maintenance_date")
        mtype = safe_str(r.get("maintenance_type"))
        if not eid or not mdate or not mtype:
            continue

        if isinstance(mdate, str):
            from datetime import datetime
            mdate = datetime.strptime(mdate, "%Y-%m-%d").date()

        mtype_norm = normalize_mtype(mtype) or mtype
        downtime = safe_float(r.get("downtime_hours"))
        cost = safe_float(r.get("maintenance_cost"))
        type_valid = mtype_norm in VALID_MAINTENANCE_TYPES
        downtime_valid = downtime >= 0
        cost_valid = cost >= 0

        result.append({
            "equipment_id": eid,
            "maintenance_date": mdate,
            "maintenance_type": mtype,
            "maintenance_type_normalized": mtype_norm,
            "downtime_hours": downtime,
            "maintenance_cost": cost,
            "type_valid": type_valid,
            "downtime_valid": downtime_valid,
            "cost_valid": cost_valid,
        })
    return result
