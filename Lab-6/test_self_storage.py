import pytest
from self_storage import rent_due, access_allowed, payment_status

# Example test cases:
def test_within_deposit_months():
    assert rent_due("small", 1, False, False) == 0

def test_access_allowed():
    assert access_allowed(12, 1, False) is True

# Write the rest of the test cases so that the code is 90-100% covered.
