"""
Code Coverage Test Suite for car_insurance_premium.py
Focus: Achieving 100% Statement/Line Coverage.
"""

import unittest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


class TestCodeCoverageCarInsurance(unittest.TestCase):
    """Test suite designed to achieve 100% statement (line) coverage."""

    # --- annual_premium() tests ---
    def test_annual_premium_invalid_car_type(self):
        with self.assertRaises(ValueError) as ctx:
            annual_premium("truck", 30, 0, False)
        self.assertEqual(str(ctx.exception), "unknown car type")

    def test_annual_premium_driver_too_young(self):
        with self.assertRaises(ValueError) as ctx:
            annual_premium("hatchback", 17, 0, False)
        self.assertEqual(str(ctx.exception), "driver too young")

    def test_annual_premium_young_driver_no_claims_anti_theft(self):
        # 8000 + 4000 = 12000 -> 12000 - 2400 = 9600 -> 9600 - 500 = 9100
        result = annual_premium("hatchback", 20, 0, True)
        self.assertEqual(result, 9100)

    def test_annual_premium_senior_driver_high_claims_anti_theft(self):
        # 12000 + 2000 = 14000 -> 14000 * 2 = 28000 -> 28000 - 500 = 27500
        result = annual_premium("sedan", 65, 4, True)
        self.assertEqual(result, 27500)

    # --- no_claim_bonus() tests ---
    def test_no_claim_bonus_invalid_years(self):
        with self.assertRaises(ValueError) as ctx:
            no_claim_bonus(-1)
        self.assertEqual(str(ctx.exception), "invalid years")

    def test_no_claim_bonus_tier_5_years(self):
        self.assertEqual(no_claim_bonus(5), 50)

    def test_no_claim_bonus_tier_3_years(self):
        self.assertEqual(no_claim_bonus(3), 35)

    def test_no_claim_bonus_tier_1_year(self):
        self.assertEqual(no_claim_bonus(1), 20)

    def test_no_claim_bonus_tier_zero_years(self):
        self.assertEqual(no_claim_bonus(0), 0)

    # --- claim_payout() tests ---
    def test_claim_payout_negative_damage(self):
        with self.assertRaises(ValueError) as ctx:
            claim_payout(-500, 10000, 500, False)
        self.assertEqual(str(ctx.exception), "invalid amount")

    def test_claim_payout_total_loss(self):
        self.assertEqual(claim_payout(5000, 10000, 500, True), 10000)

    def test_claim_payout_below_deductible(self):
        self.assertEqual(claim_payout(400, 10000, 500, False), 0)

    def test_claim_payout_exceeds_insured_value(self):
        self.assertEqual(claim_payout(15000, 10000, 1000, False), 10000)

    def test_claim_payout_partial_payout(self):
        self.assertEqual(claim_payout(6000, 10000, 1000, False), 5000)


if __name__ == "__main__":
    unittest.main()
