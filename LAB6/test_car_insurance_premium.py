"""
Comprehensive Unit Test Suite for car_insurance_premium.py
Achieving 100% Line, Branch, and Boundary coverage.
"""

import unittest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


class TestInsuranceApplication(unittest.TestCase):
    """Test suite covering 100% of execution lines and decision branches."""

    # =========================================================================
    # 1. annual_premium() tests
    # =========================================================================

    def test_annual_premium_invalid_car_type(self):
        with self.assertRaises(ValueError) as ctx:
            annual_premium("truck", 30, 0, False)
        self.assertEqual(str(ctx.exception), "unknown car type")

    def test_annual_premium_driver_underage_boundary(self):
        with self.assertRaises(ValueError) as ctx:
            annual_premium("hatchback", 17, 0, False)
        self.assertEqual(str(ctx.exception), "driver too young")

    def test_annual_premium_young_driver_minimum_age_with_antitheft(self):
        self.assertEqual(annual_premium("hatchback", 18, 0, True), 9100)

    def test_annual_premium_young_driver_upper_boundary(self):
        self.assertEqual(annual_premium("hatchback", 24, 0, True), 9100)

    def test_annual_premium_senior_driver_boundary_high_claims_no_antitheft(self):
        self.assertEqual(annual_premium("sedan", 60, 3, False), 28000)

    def test_annual_premium_senior_driver_above_boundary(self):
        self.assertEqual(annual_premium("sedan", 75, 4, False), 28000)

    def test_annual_premium_middle_aged_driver_moderate_claims_no_antitheft(self):
        self.assertEqual(annual_premium("suv", 25, 1, False), 15000)

    def test_annual_premium_middle_aged_upper_boundary_two_claims(self):
        self.assertEqual(annual_premium("suv", 59, 2, False), 15000)

    # =========================================================================
    # 2. no_claim_bonus() tests
    # =========================================================================

    def test_no_claim_bonus_negative_years(self):
        with self.assertRaises(ValueError) as ctx:
            no_claim_bonus(-1)
        self.assertEqual(str(ctx.exception), "invalid years")

    def test_no_claim_bonus_tier_5_or_more_years(self):
        self.assertEqual(no_claim_bonus(5), 50)
        self.assertEqual(no_claim_bonus(7), 50)

    def test_no_claim_bonus_tier_3_to_4_years(self):
        self.assertEqual(no_claim_bonus(3), 35)
        self.assertEqual(no_claim_bonus(4), 35)

    def test_no_claim_bonus_tier_1_to_2_years(self):
        self.assertEqual(no_claim_bonus(1), 20)
        self.assertEqual(no_claim_bonus(2), 20)

    def test_no_claim_bonus_tier_zero_years(self):
        self.assertEqual(no_claim_bonus(0), 0)

    # =========================================================================
    # 3. claim_payout() tests
    # =========================================================================

    def test_claim_payout_negative_damage_cost(self):
        with self.assertRaises(ValueError) as ctx:
            claim_payout(-100, 10000, 500, False)
        self.assertEqual(str(ctx.exception), "invalid amount")

    def test_claim_payout_negative_deductible(self):
        with self.assertRaises(ValueError) as ctx:
            claim_payout(1000, 10000, -50, False)
        self.assertEqual(str(ctx.exception), "invalid amount")

    def test_claim_payout_total_loss(self):
        self.assertEqual(claim_payout(3000, 15000, 500, True), 15000)

    def test_claim_payout_damage_strictly_below_deductible(self):
        self.assertEqual(claim_payout(300, 15000, 500, False), 0)

    def test_claim_payout_damage_equal_to_deductible(self):
        self.assertEqual(claim_payout(500, 15000, 500, False), 0)

    def test_claim_payout_payout_exceeds_insured_value(self):
        self.assertEqual(claim_payout(18000, 15000, 1000, False), 15000)

    def test_claim_payout_payout_strictly_less_than_insured_value(self):
        self.assertEqual(claim_payout(6000, 15000, 1000, False), 5000)

    def test_claim_payout_payout_exactly_equals_insured_value(self):
        self.assertEqual(claim_payout(16000, 15000, 1000, False), 15000)


if __name__ == "__main__":
    unittest.main()
