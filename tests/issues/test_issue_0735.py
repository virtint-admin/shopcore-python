"""Issue 0735. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.price_rules import compare_at_label

CASES = [
    pytest.param(
        (Money("499.01", "INR"), Money("599.00", "INR")),
        {},
        "Save 16%",
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("599.00", "INR"), Money("1198.00", "INR")),
        {},
        "Save 50%",
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("599.00", "INR"), Money("599.01", "INR")),
        {},
        "",
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("598.99", "INR"), Money("599.00", "INR")),
        {},
        "",
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("99.99", "INR"), Money("100.50", "INR")),
        {},
        "",
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("0.01", "INR")),
        {},
        "Save 100%",
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("0.00", "INR")),
        {},
        "",
        None,
        id="case-7",
    ),
    pytest.param(
        (Money("-0.01", "INR"), Money("0.00", "INR")),
        {},
        "",
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("0.00", "INR"), Money("-0.01", "INR")),
        {},
        "",
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0735(args, kwargs, expected, after):
    assert compare_at_label(*args, **kwargs) == expected
    if after is not None:
        assert args == after
