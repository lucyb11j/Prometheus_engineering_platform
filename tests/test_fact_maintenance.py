import pytest


def test_fact_maintenance_has_rows(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_maintenance")
    assert cur.fetchone()[0] > 0, "fact_maintenance is empty"


def test_date_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_maintenance WHERE date_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL date_key"


def test_equipment_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_maintenance WHERE equipment_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL equipment_key"


def test_maintenance_type_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_maintenance WHERE maintenance_type IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL maintenance_type"


def test_downtime_hours_positive(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_maintenance WHERE downtime_hours <= 0")
    assert cur.fetchone()[0] == 0, "Found non-positive downtime_hours"


def test_maintenance_cost_positive(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_maintenance WHERE maintenance_cost <= 0")
    assert cur.fetchone()[0] == 0, "Found non-positive maintenance_cost"


def test_referential_integrity_equipment(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_maintenance fm
        LEFT JOIN curated.dim_equipment de ON fm.equipment_key = de.equipment_key
        WHERE de.equipment_key IS NULL
    """)
    assert cur.fetchone()[0] == 0, "Found orphan equipment_key in fact_maintenance"
