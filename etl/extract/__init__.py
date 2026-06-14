import csv
from typing import Any


def read_csv(filepath: str) -> list[dict[str, Any]]:
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


from etl.extract.extract_projects import extract_projects
from etl.extract.extract_costs import extract_costs
from etl.extract.extract_schedule import extract_schedule
from etl.extract.extract_maintenance import extract_maintenance
from etl.extract.extract_risks import extract_risks
from etl.extract.extract_vendors import extract_vendors
from etl.extract.extract_employees import extract_employees
from etl.extract.extract_equipment import extract_equipment
from etl.extract.extract_locations import extract_locations
from etl.extract.extract_workforce import extract_workforce
