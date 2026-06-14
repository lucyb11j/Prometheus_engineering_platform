import os
from dataclasses import dataclass, field

@dataclass
class DatabaseConfig:
    host: str = field(default_factory=lambda: os.getenv("DB_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("DB_PORT", "5432")))
    dbname: str = field(default_factory=lambda: os.getenv("DB_NAME", "engineering_platform"))
    user: str = field(default_factory=lambda: os.getenv("DB_USER", "postgres"))
    password: str = field(default_factory=lambda: os.getenv("DB_PASSWORD", "postgres"))
    min_conn: int = field(default_factory=lambda: int(os.getenv("DB_MIN_CONN", "2")))
    max_conn: int = field(default_factory=lambda: int(os.getenv("DB_MAX_CONN", "10")))

    @property
    def dsn(self) -> str:
        return f"host={self.host} port={self.port} dbname={self.dbname} user={self.user} password={self.password}"

    @property
    def uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class Config:
    DATASETS_DIR: str = os.getenv("DATASETS_DIR", "datasets")
    DB: DatabaseConfig = DatabaseConfig()

    EXTRACT_BATCH_SIZE: int = 1000
    LOG_DIR: str = os.getenv("ETL_LOG_DIR", "etl/logs")

    SOURCE_FILES: dict[str, str] = field(default_factory=lambda: {
        "projects": "datasets/projects.csv",
        "locations": "datasets/locations.csv",
        "vendors": "datasets/vendors.csv",
        "employees": "datasets/employees.csv",
        "equipment": "datasets/equipment.csv",
        "costs": "datasets/costs.csv",
        "schedule": "datasets/schedule.csv",
        "maintenance": "datasets/maintenance.csv",
        "risks": "datasets/risks.csv",
    })

    def __post_init__(self):
        if isinstance(self.SOURCE_FILES, dict):
            return
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
        }


config = Config()
