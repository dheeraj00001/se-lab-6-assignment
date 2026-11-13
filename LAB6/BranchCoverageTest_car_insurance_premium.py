"""
Branch Coverage Test Suite for car_insurance_premium.py
Focus: Achieving 100% Branch and Decision Coverage, covering all edge cases,
boundary conditions, and True/False paths of every control structure.
"""

import unittest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


class TestBranchCoverageCarInsurance(unittest.TestCase):
    """Test suite covering 100% of decision branches, boundaries, and logic paths."""

    # =========================================================================
    # 1. ANNUAL_PREMIUM() BRANCH & BOUNDARY TESTS
    # =========================================================================

    def test_annual_premium_invalid_car_type(self):
        """Branch: car_type not in BASE_PREMIUM -> True."""
        with self.assertRaises(ValueError) as ctx:
            annual_premium("truck", 30, 0, False)
        self.assertEqual(str(ctx.exception), "unknown car type")

    def test_annual_premium_driver_underage_boundary(self):
        """Branch: driver_age < 18 -> True (boundary: 17)."""
        with self.assertRaises(ValueError) as ctx:
            annual_premium("hatchback", 17, 0, False)
        self.assertEqual(str(ctx.exception), "driver too young")

    def test_annual_premium_young_driver_minimum_age_with_antitheft(self):
        """
        Branches:
        - driver_age < 25 -> True (lower boundary: 18)
        - claims_last_3_years == 0 -> True
        - has_anti_theft -> True
        Calculation: (8000 + 4000) = 12000 -> 12000 - 2400 = 9600 -> 9600 - 500 = 9100
        """
        self.assertEqual(annual_premium("hatchback", 18, 0, True), 9100)

    def test_annual_premium_young_driver_upper_boundary(self):
        """
        Branch: driver_age < 25 -> True (upper boundary: 24).
        Calculation: (8000 + 4000) = 12000 -> 12000 - 2400 = 9600 -> 9600 - 500 = 9100
        """
        self.assertEqual(annual_premium("hatchback", 24, 0, True), 9100)

    def test_annual_premium_senior_driver_boundary_high_claims_no_antitheft(self):
        """
        Branches:
        - driver_age < 25 -> False
        - driver_age >= 60 -> True (boundary: 60)
        - claims_last_3_years == 0 -> False
        - claims_last_3_years > 2 -> True (boundary: 3)
        - has_anti_theft -> False
        Calculation: (12000 + 2000) = 14000 -> 14000 * 2 = 28000
        """
        self.assertEqual(annual_premium("sedan", 60, 3, False), 28000)

    def test_annual_premium_senior_driver_above_boundary(self):
        """
        Branch: driver_age >= 60 -> True (age 75).
        Calculation: (12000 + 2000) = 14000 -> 14000 * 2 = 28000
        """
        self.assertEqual(annual_premium("sedan", 75, 4, False), 28000)

    def test_annual_premium_middle_aged_driver_moderate_claims_no_antitheft(self):
        """
        Branches covered (all False / fall-through paths):
        - driver_age < 25 -> False (boundary: 25)
        - driver_age >= 60 -> False (boundary: 25)  [covers branch 12->14]
        - claims_last_3_years == 0 -> False
        - claims_last_3_years > 2 -> False (1 claim) [covers branch 16->18]
        - has_anti_theft -> False                     [covers branch 18->20]
        Calculation: Base SUV = 15000 (no adjustments)
        """
        self.assertEqual(annual_premium("suv", 25, 1, False), 15000)

    def test_annual_premium_middle_aged_upper_boundary_two_claims(self):
        """
        Branches covered:
        - driver_age < 25 -> False, driver_age >= 60 -> False (boundary: 59)
        - claims_last_3_years == 0 -> False, claims > 2 -> False (boundary: 2 claims)
        - has_anti_theft -> False
        Calculation: Base SUV = 15000
        """
        self.assertEqual(annual_premium("suv", 59, 2, False), 15000)

    # =========================================================================
    # 2. NO_CLAIM_BONUS() BRANCH & BOUNDARY TESTS
    # =========================================================================

    def test_no_claim_bonus_negative_years(self):
        """Branch: claim_free_years < 0 -> True."""
        with self.assertRaises(ValueError) as ctx:
            no_claim_bonus(-1)
        self.assertEqual(str(ctx.exception), "invalid years")

    def test_no_claim_bonus_tier_5_or_more_years(self):
        """Branch: claim_free_years >= 5 -> True (boundary: 5 and beyond: 7)."""
        self.assertEqual(no_claim_bonus(5), 50)
        self.assertEqual(no_claim_bonus(7), 50)

    def test_no_claim_bonus_tier_3_to_4_years(self):
        """Branch: >= 5 (False) -> >= 3 (True) (boundaries: 3 and 4)."""
        self.assertEqual(no_claim_bonus(3), 35)
        self.assertEqual(no_claim_bonus(4), 35)

    def test_no_claim_bonus_tier_1_to_2_years(self):
        """Branch: >= 3 (False) -> >= 1 (True) (boundaries: 1 and 2)."""
        self.assertEqual(no_claim_bonus(1), 20)
        self.assertEqual(no_claim_bonus(2), 20)

    def test_no_claim_bonus_zero_years(self):
        """Branch: all conditions False -> returns 0 (boundary: 0)."""
        self.assertEqual(no_claim_bonus(0), 0)

    # =========================================================================
    # 3. CLAIM_PAYOUT() BRANCH & BOUNDARY TESTS
    # =========================================================================

    def test_claim_payout_negative_damage_cost(self):
        """Branch: damage_cost < 0 (True) or deductible < 0."""
        with self.assertRaises(ValueError) as ctx:
            claim_payout(-100, 10000, 500, False)
        self.assertEqual(str(ctx.exception), "invalid amount")

    def test_claim_payout_negative_deductible(self):
        """Branch: damage_cost < 0 (False) or deductible < 0 (True)."""
        with self.assertRaises(ValueError) as ctx:
            claim_payout(1000, 10000, -50, False)
        self.assertEqual(str(ctx.exception), "invalid amount")

    def test_claim_payout_total_loss(self):
        """Branch: is_total_loss -> True (returns insured_value)."""
        self.assertEqual(claim_payout(3000, 15000, 500, True), 15000)

    def test_claim_payout_damage_strictly_below_deductible(self):
        """Branch: is_total_loss (False) -> damage_cost <= deductible (True: <)."""
        self.assertEqual(claim_payout(300, 15000, 500, False), 0)

    def test_claim_payout_damage_equal_to_deductible(self):
        """Branch: damage_cost <= deductible (True: == boundary)."""
        self.assertEqual(claim_payout(500, 15000, 500, False), 0)

    def test_claim_payout_payout_exceeds_insured_value(self):
        """
        Branch: payout > insured_value -> True.
        Calculation: 18000 - 1000 = 17000 > 15000 -> returns 15000.
        """
        self.assertEqual(claim_payout(18000, 15000, 1000, False), 15000)

    def test_claim_payout_payout_strictly_less_than_insured_value(self):
        """
        Branch: payout > insured_value -> False.
        Calculation: 6000 - 1000 = 5000 <= 15000 -> returns 5000.
        """
        self.assertEqual(claim_payout(6000, 15000, 1000, False), 5000)

    def test_claim_payout_payout_exactly_equals_insured_value(self):
        """
        Branch: payout > insured_value -> False (boundary: payout == insured_value).
        Calculation: 16000 - 1000 = 15000 <= 15000 -> returns 15000.
        """
        self.assertEqual(claim_payout(16000, 15000, 1000, False), 15000)


if __name__ == "__main__":
    unittest.main()
