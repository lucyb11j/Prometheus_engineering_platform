def build_dim_vendor(rows: list[dict]) -> list[dict]:
    return [
        {
            "vendor_id": r["vendor_id"],
            "vendor_name": r["vendor_name"],
            "category": r["category"],
            "country": r["country"],
        }
        for r in rows
    ]
