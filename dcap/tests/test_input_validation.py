import unittest
from src.common.validate_inputs import validate_rows
from src.common.read_inputs import ROOT, read_yaml, read_csv
from src.monthly_enrollment.prepare import summarize

class InputTests(unittest.TestCase):
    def setUp(self):
        self.spec = read_yaml(ROOT / "config/datasets.yaml")["monthly_enrollment"]
        self.rules = read_yaml(ROOT / "config/validation_rules.yaml")["monthly_enrollment"]
        self.headers, self.rows = read_csv(ROOT / "tests/fixtures/enrollment.csv")
    def test_summary(self):
        rows = validate_rows(self.headers, self.rows, self.spec, self.rules)
        self.assertEqual(summarize(rows, "2026-10"), [dict(state="CA",enrollment_count=115),dict(state="NY",enrollment_count=210),dict(state="TX",enrollment_count=10)])
    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            validate_rows(self.headers, self.rows + [self.rows[0]], self.spec, self.rules)
    def test_negative(self):
        self.rows[0]["enrollment_count"] = "-1"
        with self.assertRaises(ValueError): validate_rows(self.headers, self.rows, self.spec, self.rules)
    def test_missing_column(self):
        with self.assertRaisesRegex(ValueError, "Missing columns"):
            validate_rows(self.headers[:-1], self.rows, self.spec, self.rules)
    def test_invalid_month(self):
        self.rows[0]["report_month"] = "2026-13"
        with self.assertRaises(ValueError): validate_rows(self.headers, self.rows, self.spec, self.rules)
