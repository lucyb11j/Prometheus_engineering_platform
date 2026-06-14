import pytest


def test_project_key_is_unique(cur):
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT project_key) FROM curated.dim_project")
    total, distinct = cur.fetchone()
    assert total == distinct, f"project_key has {total - distinct} duplicates"


def test_project_id_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_project WHERE project_id IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL project_id"


def test_budget_positive(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_project WHERE budget <= 0")
    assert cur.fetchone()[0] == 0, "Found non-positive budget"


def test_project_type_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_project WHERE project_type IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL project_type"


def test_status_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_project WHERE status IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL status"


def test_is_current_valid(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_project WHERE is_current NOT IN (TRUE, FALSE)")
    assert cur.fetchone()[0] == 0, "Found invalid is_current values"


def test_date_order(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_project WHERE effective_date > expiration_date")
    assert cur.fetchone()[0] == 0, "Found effective_date after expiration_date"


def test_only_one_current_per_project(cur):
    cur.execute("""
        SELECT project_id, COUNT(*) FROM curated.dim_project
        WHERE is_current = TRUE GROUP BY project_id HAVING COUNT(*) > 1
    """)
    assert cur.fetchone() is None, "Found multiple current records for same project"
