def transform_locations(rows: list[dict]) -> list[dict]:
    transformed = []
    for r in rows:
        transformed.append({
            "location_id": r["location_id"].strip(),
            "country": r["country"].strip(),
            "region": r["region"].strip(),
            "city": r["city"].strip(),
            "site_name": r["site_name"].strip(),
        })
    return transformed
