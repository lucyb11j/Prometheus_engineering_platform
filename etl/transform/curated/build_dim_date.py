from datetime import date, timedelta


def build_dim_date(start: str = "2020-01-01", end: str = "2035-12-31") -> list[dict]:
    start_dt = date.fromisoformat(start)
    end_dt = date.fromisoformat(end)
    rows = []
    d = start_dt
    while d <= end_dt:
        rows.append({
            "date_key": int(d.strftime("%Y%m%d")),
            "full_date": d,
            "year": d.year,
            "quarter": (d.month - 1) // 3 + 1,
            "month": d.month,
            "month_name": d.strftime("%B"),
            "week": d.isocalendar()[1],
            "day": d.day,
            "day_name": d.strftime("%A"),
        })
        d += timedelta(days=1)
    return rows
