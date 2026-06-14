def build_dim_location(rows: list[dict]) -> list[dict]:
    return [
        {
            "location_id": r["location_id"],
            "country": r["country"],
            "region": r["region"],
            "city": r["city"],
            "site_name": r["site_name"],
        }
        for r in rows
    ]
