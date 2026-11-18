import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.common.read_inputs import load_settings, resolve_path, read_csv
from src.common.validate_inputs import validate_rows
from src.monthly_enrollment.prepare import summarize
from src.monthly_enrollment.reports import write_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", required=True)
    parser.add_argument("--paths", default="config/paths.local.yaml")
    args = parser.parse_args()
    paths, datasets, rules = load_settings(args.paths)
    spec = datasets["monthly_enrollment"]
    headers, raw = read_csv(resolve_path(paths["input_dir"]) / spec["filename"])
    rows = validate_rows(headers, raw, spec, rules["monthly_enrollment"])
    output = write_report(resolve_path(paths["output_dir"]), args.month, summarize(rows, args.month))
    print(f"Validated {len(rows)} source records. Wrote {output}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
