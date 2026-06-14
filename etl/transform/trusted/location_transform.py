from etl.transform.trusted.utils import safe_str


def transform_location(rows: list[dict]) -> list[dict]:
    result = []
    for r in rows:
        lid = safe_str(r.get("location_id"))
        country = safe_str(r.get("country"))
        city = safe_str(r.get("city"))
        if not lid or not country or not city:
            continue

        result.append({
            "location_id": lid,
            "country": country.title(),
            "region": safe_str(r.get("region")).title(),
            "city": city.title(),
            "site_name": safe_str(r.get("site_name")),
        })
    return result
