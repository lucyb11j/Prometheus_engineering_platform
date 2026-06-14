from etl.extract import read_csv


def extract_risks(filepath: str) -> list[dict]:
    return read_csv(filepath)
