import pytest


def test_fact_schedule_has_rows(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_schedule")
    assert cur.fetchone()[0] > 0, "fact_schedule is empty"


def test_date_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_schedule WHERE date_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL date_key"


def test_project_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_schedule WHERE project_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL project_key"


def test_progress_in_range(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_schedule
        WHERE planned_progress < 0 OR planned_progress > 100
           OR actual_progress < 0 OR actual_progress > 100
    """)
    assert cur.fetchone()[0] == 0, "Found progress values outside [0, 100]"


def test_spi_calculated(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_schedule
        WHERE spi IS NOT NULL AND planned_progress > 0
          AND ABS(spi - (actual_progress / planned_progress)) > 0.0001
    """)
    assert cur.fetchone()[0] == 0, "Found mismatched spi"


def test_referential_integrity_project(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_schedule fs
        LEFT JOIN curated.dim_project dp ON fs.project_key = dp.project_key
        WHERE dp.project_key IS NULL
    """)
    assert cur.fetchone()[0] == 0, "Found orphan project_key in fact_schedule"
