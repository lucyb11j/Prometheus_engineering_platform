from etl.transform.trusted.utils import safe_str, VALID_CATEGORIES


def transform_vendor(rows: list[dict]) -> list[dict]:
    result = []
    for r in rows:
        vid = safe_str(r.get("vendor_id"))
        name = safe_str(r.get("vendor_name"))
        if not vid or not name:
            continue

        cat = safe_str(r.get("category")).title()
        country = safe_str(r.get("country")).title()
        cat_valid = cat in VALID_CATEGORIES

        result.append({
            "vendor_id": vid,
            "vendor_name": name,
            "category": cat,
            "country": country,
            "category_valid": cat_valid,
        })
    return result
