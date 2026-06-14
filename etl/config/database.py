import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    dbname: str = "analytics_db"
    user: str = "admin"
    password: str = "tu_password_secreto"
    min_conn: int = 2
    max_conn: int = 10

    def __post_init__(self):
        self.host = os.getenv("DB_HOST", self.host)
        self.port = int(os.getenv("DB_PORT", str(self.port)))
        self.dbname = os.getenv("DB_NAME", self.dbname)
        self.user = os.getenv("DB_USER", self.user)
        self.password = os.getenv("DB_PASSWORD", self.password)
        self.min_conn = int(os.getenv("DB_MIN_CONN", str(self.min_conn)))
        self.max_conn = int(os.getenv("DB_MAX_CONN", str(self.max_conn)))

    @property
    def dsn(self) -> str:
        return f"host={self.host} port={self.port} dbname={self.dbname} user={self.user} password={self.password}"

    @property
    def uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class Config:
    def __init__(self):
        self.DATASETS_DIR = os.getenv("DATASETS_DIR", "datasets")
        self.DB = DatabaseConfig()
        self.EXTRACT_BATCH_SIZE = 1000
        self.LOG_DIR = os.getenv("ETL_LOG_DIR", "etl/logs")
        self.SOURCE_FILES = {
            "projects": f"{self.DATASETS_DIR}/projects.csv",
            "locations": f"{self.DATASETS_DIR}/locations.csv",
            "vendors": f"{self.DATASETS_DIR}/vendors.csv",
            "employees": f"{self.DATASETS_DIR}/employees.csv",
            "equipment": f"{self.DATASETS_DIR}/equipment.csv",
            "costs": f"{self.DATASETS_DIR}/costs.csv",
            "schedule": f"{self.DATASETS_DIR}/schedule.csv",
            "maintenance": f"{self.DATASETS_DIR}/maintenance.csv",
            "risks": f"{self.DATASETS_DIR}/risks.csv",
            "workforce": f"{self.DATASETS_DIR}/workforce.csv",
        }


config = Config()
