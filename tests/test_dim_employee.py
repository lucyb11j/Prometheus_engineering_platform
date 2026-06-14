import pytest


def test_employee_key_is_unique(cur):
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT employee_key) FROM curated.dim_employee")
    total, distinct = cur.fetchone()
    assert total == distinct, f"employee_key has {total - distinct} duplicates"


def test_employee_id_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_employee WHERE employee_id IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL employee_id"


def test_full_name_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_employee WHERE full_name IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL full_name"


def test_department_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_employee WHERE department IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL department"


def test_role_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_employee WHERE role IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL role"


def test_is_current_valid(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_employee WHERE is_current NOT IN (TRUE, FALSE)")
    assert cur.fetchone()[0] == 0, "Found invalid is_current values"


def test_only_one_current_per_employee(cur):
    cur.execute("""
        SELECT employee_id, COUNT(*) FROM curated.dim_employee
        WHERE is_current = TRUE GROUP BY employee_id HAVING COUNT(*) > 1
    """)
    assert cur.fetchone() is None, "Found multiple current records for same employee"


def test_salary_positive(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_employee WHERE salary < 0")
    assert cur.fetchone()[0] == 0, "Found negative salary"
