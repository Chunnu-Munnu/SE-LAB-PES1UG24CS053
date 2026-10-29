"""Lab 6 - code (line) coverage tests for self_storage.py.

Run:
    coverage run -m pytest CodeCoverageTest_self_storage.py
    coverage report -m
"""
import pytest
from self_storage import rent_due, access_allowed, payment_status


# ---------- rent_due ----------
def test_within_deposit_months():
    assert rent_due("small", 1, False, False) == 0


def test_unknown_unit_size_raises():
    with pytest.raises(ValueError, match="unknown unit size"):
        rent_due("tiny", 3, False, False)


def test_negative_months_raises():
    with pytest.raises(ValueError, match="invalid months"):
        rent_due("small", -1, False, False)


def test_standard_unit_extra_month_normal_rate():
    # small covers 1 month, 1 extra month at 80
    assert rent_due("small", 2, False, False) == 80


def test_climate_unit_extra_month_climate_rate():
    # small covers 1 month, 1 extra month at 120
    assert rent_due("small", 2, True, False) == 120


def test_member_gets_extra_covered_month():
    # medium covers 2 + 1 member month, 1 extra month at 80
    assert rent_due("medium", 4, False, True) == 80


def test_long_stay_discount_standard():
    # small covers 1, extra 7 > 6 -> rate 70
    assert rent_due("small", 8, False, False) == 490


# ---------- access_allowed ----------
def test_access_allowed():
    assert access_allowed(12, 1, False) is True


def test_owner_access_with_visitors():
    assert access_allowed(3, 4, True) is True


def test_non_owner_outside_hours_denied():
    assert access_allowed(3, 1, False) is False


def test_non_owner_too_many_visitors_denied():
    assert access_allowed(12, 3, False) is False


# ---------- payment_status ----------
def test_payment_current():
    assert payment_status(10, False, False) == "current"


def test_payment_grace():
    assert payment_status(0, False, False) == "grace"


def test_payment_autopay_current():
    assert payment_status(0, True, False) == "current"
