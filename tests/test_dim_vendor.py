import pytest


def test_vendor_key_is_unique(cur):
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT vendor_key) FROM curated.dim_vendor")
    total, distinct = cur.fetchone()
    assert total == distinct, f"vendor_key has {total - distinct} duplicates"


def test_vendor_id_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_vendor WHERE vendor_id IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL vendor_id"


def test_vendor_id_unique(cur):
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT vendor_id) FROM curated.dim_vendor")
    total, distinct = cur.fetchone()
    assert total == distinct, f"vendor_id has {total - distinct} duplicates"


def test_vendor_name_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_vendor WHERE vendor_name IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL vendor_name"


def test_category_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_vendor WHERE category IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL category"


def test_country_not_null(cur):
    cur.execute("SELECT COUNT(*) FROM curated.dim_vendor WHERE country IS NULL")
    assert cur.fetchone()[0] == 0, "Found NULL country"
