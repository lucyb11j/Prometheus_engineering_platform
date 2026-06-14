from etl.extract import read_csv


def extract_workforce(filepath: str) -> list[dict]:
    return read_csv(filepath)
