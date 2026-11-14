"""Issue 0729. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.price_rules import enforce_mrp

CASES = [
    pytest.param(
        (Money("650.00", "INR"), Money("599.00", "INR")),
        {},
        Money("599.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("650.00", "INR"), Money("598.99", "INR")),
        {},
        Money("598.99", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("498.99", "INR"), Money("599.00", "INR")),
        {},
        Money("498.99", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("499.00", "INR"), Money("1198.00", "INR")),
        {},
        Money("499.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("1198.00", "INR"), Money("599.00", "INR")),
        {},
        Money("599.00", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("599.00", "INR"), Money("1198.00", "INR")),
        {},
        Money("599.00", "INR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("599.00", "INR"), Money("599.00", "INR")),
        {},
        Money("599.00", "INR"),
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0729(args, kwargs, expected, after):
    assert enforce_mrp(*args, **kwargs) == expected
    if after is not None:
        assert args == after
