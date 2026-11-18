import csv
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[2]


def read_yaml(path):
    with Path(path).open(encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return value


def resolve_path(value):
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_settings(paths_file="config/paths.local.yaml"):
    paths = read_yaml(resolve_path(paths_file))
    datasets = read_yaml(ROOT / "config/datasets.yaml")
    rules = read_yaml(ROOT / "config/validation_rules.yaml")
    return paths, datasets, rules


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        headers = reader.fieldnames or []
        if len(headers) != len(set(headers)):
            raise ValueError("Duplicate CSV header")
        rows = list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            raise ValueError("CSV row has a different field count from the header")
        return headers, rows
