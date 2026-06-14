import pytest


def test_fact_risk_has_rows(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_risk")
    assert cur.fetchone()[0] > 0, "fact_risk is empty"


def test_date_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_risk WHERE date_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL date_key"


def test_project_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_risk WHERE project_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL project_key"


def test_risk_key_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_risk WHERE risk_key IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL risk_key"


def test_probability_in_range(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_risk WHERE probability < 0 OR probability > 1")
    assert cur.fetchone()[0] == 0, "Found probability outside [0, 1]"


def test_severity_in_range(cur):
    cur.execute("SELECT COUNT(*) FROM curated.fact_risk WHERE severity_score < 1 OR severity_score > 10")
    assert cur.fetchone()[0] == 0, "Found severity_score outside [1, 10]"


def test_risk_score_calculated(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_risk
        WHERE ABS(risk_score - (probability * severity_score)) > 0.01
    """)
    assert cur.fetchone()[0] == 0, "Found mismatched risk_score"


def test_referential_integrity_project(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_risk fr
        LEFT JOIN curated.dim_project dp ON fr.project_key = dp.project_key
        WHERE dp.project_key IS NULL
    """)
    assert cur.fetchone()[0] == 0, "Found orphan project_key in fact_risk"


def test_referential_integrity_risk(cur):
    cur.execute("""
        SELECT COUNT(*) FROM curated.fact_risk fr
        LEFT JOIN curated.dim_risk dr ON fr.risk_key = dr.risk_key
        WHERE dr.risk_key IS NULL
    """)
    assert cur.fetchone()[0] == 0, "Found orphan risk_key in fact_risk"
