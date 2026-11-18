import unittest
from src.common.compare_outputs import compare_months
SETTINGS = dict(change_threshold_pct=10, decimal_places=2, rounding="ROUND_HALF_UP")
class PrecisionTests(unittest.TestCase):
    def test_half_up(self):
        result = compare_months({"CA": 100000}, {"CA": 101005}, SETTINGS)
        self.assertEqual(result[0]["change_pct"], "1.01")
    def test_unrounded_threshold(self):
        result = compare_months({"CA": 100000}, {"CA": 110004}, SETTINGS)
        self.assertEqual(result[0]["change_pct"], "10.00")
        self.assertEqual(result[0]["status"], "REVIEW")
