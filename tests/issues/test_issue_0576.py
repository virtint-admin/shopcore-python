"""Issue 0576. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.orders.refunds import restocking_fee

CASES = [
    pytest.param(
        (Money("2999.00", "INR"),),
        {"opened": True},
        Money("299.90", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.05", "INR"),),
        {"opened": True},
        Money("0.01", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("1998.00", "INR"),),
        {"opened": False},
        Money("0.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("998.99", "INR"),),
        {"opened": False},
        Money("0.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("0.10", "INR"),),
        {"opened": True},
        Money("0.01", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("9", "JPY"),),
        {"opened": True},
        Money("1", "JPY"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("0.04", "INR"),),
        {"opened": True},
        Money("0.00", "INR"),
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0576(args, kwargs, expected, after):
    assert restocking_fee(*args, **kwargs) == expected
    if after is not None:
        assert args == after
