import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import psycopg2
from etl.config.database import config


@pytest.fixture(scope="session")
def conn():
    c = psycopg2.connect(config.DB.dsn)
    yield c
    c.close()


@pytest.fixture(scope="session")
def cur(conn):
    c = conn.cursor()
    yield c
    c.close()
