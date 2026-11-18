# Demo comparison specification
Key: state. Prior and current values: enrollment_count. Signed difference: current minus prior. Percent: difference / prior * 100. Compare the absolute, unrounded percentage with the configured threshold using strict greater-than. Display rounds with Decimal ROUND_HALF_UP to the configured number of places.

Zero prior value: ZERO BASELINE, blank percentage (also when both counts are zero). Missing key in either month: MISSING MONTH. These require human interpretation. Report-generation success has exit code 0 even when review flags exist. Input, configuration or execution errors have exit code 1.

This is a month-to-month review, not SAS/Python equivalence certification. Confirm actual business keys, tolerances, precision and signoff before using real results.
