import pytest


def test_fact_cost_has_rows(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_cost")
    assert cur.fetchone()[0] > 0, "fact_cost is empty"


def test_date_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_cost WHERE date_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL date_key"


def test_project_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_cost WHERE project_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL project_key"


def test_planned_cost_positive(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_cost WHERE planned_cost <= 0")
    assert cur.fetchone()[0] == 0, "Found non-positive planned_cost"


def test_actual_cost_valid(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_cost WHERE actual_cost < 0")
    assert cur.fetchone()[0] == 0, "Found negative actual_cost"


def test_cost_variance_calculated(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_cost
        WHERE cost_variance IS NOT NULL
          AND ABS(cost_variance - (actual_cost - planned_cost)) > 0.01
    """)
    assert cur.fetchone()[0] == 0, "Found mismatched cost_variance"


def test_referential_integrity_project(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_cost fc
        LEFT JOIN curated.dim_project dp ON fc.project_key = dp.project_key
        WHERE dp.project_key IS NULL
    """)
    assert cur.fetchone()[0] == 0, "Found orphan project_key in fact_cost"
