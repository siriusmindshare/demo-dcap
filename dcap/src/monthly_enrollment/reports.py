from src.common.write_csv import write_csv


def write_report(output_dir, month, rows):
    return write_csv(output_dir / f"enrollment_{month}.csv",
                     ["state", "enrollment_count"], rows)
