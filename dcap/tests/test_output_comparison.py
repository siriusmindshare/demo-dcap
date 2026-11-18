import unittest
from src.common.compare_outputs import compare_months, index_totals
SETTINGS = dict(change_threshold_pct=10, decimal_places=2, rounding="ROUND_HALF_UP")
class ComparisonTests(unittest.TestCase):
    def test_exact_threshold_ok(self):
        self.assertEqual(compare_months({"CA":100},{"CA":110},SETTINGS)[0]["status"],"OK")
    def test_decline_review(self):
        self.assertEqual(compare_months({"CA":100},{"CA":80},SETTINGS)[0]["status"],"REVIEW")
    def test_zero(self):
        row=compare_months({"TX":0},{"TX":10},SETTINGS)[0]
        self.assertEqual((row["status"],row["change_pct"]),("ZERO BASELINE",""))
    def test_missing(self):
        self.assertEqual(compare_months({"CA":10},{},SETTINGS)[0]["status"],"MISSING MONTH")
    def test_duplicate_report_key(self):
        with self.assertRaises(ValueError): index_totals([dict(state="CA",enrollment_count="1")]*2)
