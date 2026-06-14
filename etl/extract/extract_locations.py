from etl.extract import read_csv


def extract_locations(filepath: str) -> list[dict]:
    return read_csv(filepath)
