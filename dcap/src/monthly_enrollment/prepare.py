import re
from collections import defaultdict


def summarize(rows, month):
    if not re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", month):
        raise ValueError("Use a month in YYYY-MM format")
    selected = [row for row in rows if row["report_month"] == month]
    if not selected:
        raise ValueError(f"No records for {month}")
    totals = defaultdict(int)
    for row in selected:
        totals[row["state"]] += row["enrollment_count"]
    return [{"state": state, "enrollment_count": total}
            for state, total in sorted(totals.items())]
