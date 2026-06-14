def transform_vendors(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "vendor_id": r["vendor_id"].strip(),
            "vendor_name": r["vendor_name"].strip(),
            "category": r["category"].strip(),
            "country": r["country"].strip(),
        })
    return transformed
