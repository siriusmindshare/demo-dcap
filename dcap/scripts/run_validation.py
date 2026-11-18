import argparse
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.common.read_inputs import load_settings, resolve_path, read_csv
from src.common.compare_outputs import compare_months, index_totals
from src.common.write_csv import write_csv


def main():
    parser = argparse.ArgumentParser(description="Compare two generated monthly reports")
    parser.add_argument("--prior-month", required=True)
    parser.add_argument("--current-month", required=True)
    parser.add_argument("--paths", default="config/paths.local.yaml")
    args = parser.parse_args()
    for month in (args.prior_month, args.current_month):
        if not re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", month):
            raise ValueError("Use YYYY-MM for both months")
    if args.prior_month >= args.current_month:
        raise ValueError("Prior month must precede current month")
    paths, _, rules = load_settings(args.paths)
    output_dir = resolve_path(paths["output_dir"])
    counts = []
    for month in (args.prior_month, args.current_month):
        headers, rows = read_csv(output_dir / f"enrollment_{month}.csv")
        if set(headers) != {"state", "enrollment_count"}:
            raise ValueError("Unexpected report columns")
        counts.append(index_totals(rows))
    result = compare_months(*counts, rules["comparison"])
    output = write_csv(output_dir / f"change_{args.current_month}.csv",
                       ["state", "prior_count", "current_count", "change", "change_pct", "status"], result)
    print(f"Wrote {output}")
    for row in result:
        print(f"{row['state']}: {row['status']} ({row['change_pct']}%)")
    print("Review flags require investigation; this command does not approve publication.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
