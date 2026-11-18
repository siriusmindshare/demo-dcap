from decimal import Decimal, ROUND_HALF_UP


def compare_months(prior, current, settings):
    threshold = Decimal(str(settings["change_threshold_pct"]))
    places = settings["decimal_places"]
    if not threshold.is_finite() or threshold < 0:
        raise ValueError("Threshold must be finite and nonnegative")
    if type(places) is not int or not 0 <= places <= 6:
        raise ValueError("decimal_places must be an integer from 0 to 6")
    if settings["rounding"] != "ROUND_HALF_UP":
        raise ValueError("This demo supports ROUND_HALF_UP only")
    quantum = Decimal(1).scaleb(-places)
    result = []
    for key in sorted(set(prior) | set(current)):
        old, new = prior.get(key), current.get(key)
        row = dict(state=key, prior_count=old if old is not None else "",
                   current_count=new if new is not None else "",
                   change="", change_pct="", status="MISSING MONTH")
        if old is not None and new is not None:
            row["change"] = new - old
            if old == 0:
                row["status"] = "ZERO BASELINE"
            else:
                percent = Decimal(new - old) / Decimal(old) * 100
                row["change_pct"] = str(percent.quantize(quantum, rounding=ROUND_HALF_UP))
                row["status"] = "REVIEW" if abs(percent) > threshold else "OK"
        result.append(row)
    if not result:
        raise ValueError("Both monthly reports are empty")
    return result


def index_totals(rows):
    indexed = {}
    for row in rows:
        state = row["state"]
        if not state or state in indexed:
            raise ValueError("Blank or duplicate state in report")
        value = row["enrollment_count"]
        if not str(value).isdigit():
            raise ValueError("Report count must be a nonnegative integer")
        indexed[state] = int(value)
    return indexed
