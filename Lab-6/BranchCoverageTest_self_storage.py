"""Lab 6 - branch coverage tests for self_storage.py.

Every decision in the module is driven both True and False, including each
side of the compound condition `is_member and unit_size != "large"`.

Run:
    coverage run --branch -m pytest BranchCoverageTest_self_storage.py
    coverage report -m
"""
import pytest
from self_storage import rent_due, access_allowed, payment_status


# ---------- rent_due: input validation ----------
def test_unknown_unit_size_raises():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("tiny", 3, False, False)


def test_negative_months_raises():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)


def test_zero_months_is_valid_and_free():
    assert rent_due("small", 0, False, False) == 0


# ---------- rent_due: deposit / membership ----------
@pytest.mark.parametrize("size,months", [("small", 1), ("medium", 2), ("large", 3)])
def test_months_equal_to_deposit_cover_are_free(size, months):
    assert rent_due(size, months, False, False) == 0


def test_member_small_gets_bonus_month():
    # covered 1 + 1 = 2 months, so 2 months are free
    assert rent_due("small", 2, False, True) == 0
    assert rent_due("small", 3, False, True) == 80


def test_member_medium_gets_bonus_month():
    assert rent_due("medium", 3, False, True) == 0


def test_member_large_gets_no_bonus_month():
    # is_member True but unit_size == "large": covered stays 3
    assert rent_due("large", 4, False, True) == 80


def test_non_member_large_same_as_member_large():
    assert rent_due("large", 4, False, False) == 80


def test_non_member_small_no_bonus_month():
    # is_member False: covered stays 1
    assert rent_due("small", 2, False, False) == 80


# ---------- rent_due: climate and long-stay rate ----------
def test_standard_rate():
    assert rent_due("small", 2, False, False) == 80


def test_climate_rate():
    assert rent_due("small", 2, True, False) == 120


def test_six_extra_months_no_discount_standard():
    # extra == 6 is not > 6
    assert rent_due("small", 7, False, False) == 480


def test_six_extra_months_no_discount_climate():
    assert rent_due("small", 7, True, False) == 720


def test_seven_extra_months_discount_standard():
    # extra 7 > 6 -> rate 70
    assert rent_due("small", 8, False, False) == 490


def test_seven_extra_months_discount_climate():
    # extra 7 > 6 -> rate 120 - 10 - 5 = 105
    assert rent_due("small", 8, True, False) == 735


# ---------- access_allowed ----------
def test_owner_up_to_four_visitors():
    assert access_allowed(3, 4, True) is True


def test_owner_more_than_four_visitors_denied():
    assert access_allowed(12, 5, True) is False


def test_non_owner_before_opening_denied():
    assert access_allowed(5, 1, False) is False


def test_non_owner_after_closing_denied():
    assert access_allowed(23, 1, False) is False


@pytest.mark.parametrize("hour", [6, 12, 22])
def test_non_owner_inside_hours_allowed(hour):
    assert access_allowed(hour, 1, False) is True


def test_non_owner_two_visitors_allowed():
    assert access_allowed(12, 2, False) is True


def test_non_owner_three_visitors_denied():
    assert access_allowed(12, 3, False) is False


# ---------- payment_status ----------
# cutoff: autopay -> 0 else 5; prior late adds 10.
# "current" if days >= cutoff, "grace" if days >= cutoff - 15, else "lien".
@pytest.mark.parametrize(
    "days,autopay,late,expected",
    [
        # manual pay, no prior late: cutoff 5
        (5, False, False, "current"),
        (4, False, False, "grace"),
        (-10, False, False, "grace"),
        (-11, False, False, "lien"),
        # autopay, no prior late: cutoff 0
        (0, True, False, "current"),
        (-1, True, False, "grace"),
        (-15, True, False, "grace"),
        (-16, True, False, "lien"),
        # manual pay, prior late: cutoff 15
        (15, False, True, "current"),
        (14, False, True, "grace"),
        (0, False, True, "grace"),
        (-1, False, True, "lien"),
        # autopay, prior late: cutoff 10
        (10, True, True, "current"),
        (9, True, True, "grace"),
        (-5, True, True, "grace"),
        (-6, True, True, "lien"),
    ],
)
def test_payment_status(days, autopay, late, expected):
    assert payment_status(days, autopay, late) == expected
