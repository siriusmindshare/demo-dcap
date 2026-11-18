import re


def validate_rows(headers, rows, spec, rules):
    expected = set(spec["columns"])
    if expected - set(headers):
        raise ValueError(f"Missing columns: {sorted(expected - set(headers))}")
    if not rules["allow_extra_columns"] and set(headers) - expected:
        raise ValueError("Unexpected input columns")
    if not rows:
        raise ValueError("Input contains no records")
    seen = set()
    clean = []
    for number, raw in enumerate(rows, 2):
        row = dict(raw)
        for column in rules["required_nonblank"]:
            if not str(row.get(column, "")).strip():
                raise ValueError(f"Row {number}: {column} is blank")
        for column, kind in spec["columns"].items():
            value = row[column]
            if kind == "month" and not re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", value):
                raise ValueError(f"Row {number}: invalid month")
            if kind == "nonnegative_integer":
                if not re.fullmatch(r"[0-9]+", value):
                    raise ValueError(f"Row {number}: {column} must be a nonnegative integer")
                row[column] = int(value)
            elif kind not in ("month", "string"):
                raise ValueError(f"Unsupported configured type: {kind}")
        if row["state"] not in rules["allowed_states"]:
            raise ValueError(f"Row {number}: state is not allowed by the demo rules")
        key = tuple(row[column] for column in spec["keys"])
        if key in seen:
            raise ValueError(f"Row {number}: duplicate key {key}")
        seen.add(key)
        clean.append(row)
    return clean
