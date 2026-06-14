VALID_STATUSES = {"Active", "Completed", "Delayed", "Cancelled"}
VALID_CATEGORIES = {"Materials", "Equipment", "Services", "Logistics", "Consulting"}
VALID_MAINTENANCE_TYPES = {"Preventive", "Corrective", "Predictive"}
VALID_EQUIPMENT_STATUSES = {"Active", "Maintenance", "Retired"}


def normalize_status(status: str | None) -> str | None:
    if not status:
        return None
    s = status.strip().lower().replace(" ", "_").replace("-", "_")
    mapping = {
        "active": "Active", "activo": "Active", "operational": "Active",
        "completed": "Completed", "completado": "Completed", "closed": "Completed",
        "delayed": "Delayed", "atrasado": "Delayed", "on_hold": "Delayed",
        "cancelled": "Cancelled", "cancelado": "Cancelled",
        "in_maintenance": "Maintenance", "under_maintenance": "Maintenance",
        "retired": "Retired", "reserved": "Retired",
    }
    return mapping.get(s, s.title())


def normalize_mtype(mtype: str | None) -> str | None:
    if not mtype:
        return None
    m = mtype.strip().lower()
    mapping = {
        "preventive": "Preventive", "preventivo": "Preventive",
        "corrective": "Corrective", "correctivo": "Corrective",
        "predictive": "Predictive", "predictivo": "Predictive",
    }
    return mapping.get(m, mtype.strip())


def safe_float(val) -> float:
    if val is None:
        return 0.0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def safe_int(val) -> int:
    if val is None:
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


def safe_str(val) -> str:
    if val is None:
        return ""
    return str(val).strip()
