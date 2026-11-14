"""Issue 0697. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.discounts import cap_discount

CASES = [
    pytest.param(
        (Money("1000.00", "INR"), Money("0.00", "INR"), Decimal("100")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("1000.01", "INR"), Money("0.00", "INR"), Decimal("100")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("2000.00", "INR"), Money("0.00", "INR"), Decimal("100")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("1000.00", "INR"), Money("-0.01", "INR"), Decimal("100")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("1000.00", "INR"), Money("0.01", "INR"), Decimal("100")),
        {},
        Money("0.01", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("999.99", "INR"), Money("0.00", "INR"), Decimal("100")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("1000.00", "INR"), Money("800.00", "INR"), Decimal("30")),
        {},
        Money("800.00", "INR"),
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("1000.01", "INR"), Money("800.00", "INR"), Decimal("30")),
        {},
        Money("800.00", "INR"),
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("1000.00", "INR"), Money("0.00", "INR"), Decimal("99")),
        {},
        Money("10.00", "INR"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0697(args, kwargs, expected, after):
    assert cap_discount(*args, **kwargs) == expected
    if after is not None:
        assert args == after
