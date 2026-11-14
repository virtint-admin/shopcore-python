"""Issue 0484. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.money.fx import convert
from shopcore.money.rounding import RoundingMode

CASES = [
    pytest.param(
        (
            Money("999.99", "INR"),
            "USD",
            {
                ("USD", "INR"): Decimal("83.25"),
                ("EUR", "USD"): Decimal("1.08"),
                ("USD", "JPY"): Decimal("150.10"),
            },
        ),
        {},
        Money("12.01", "USD"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Money("1000.00", "INR"),
            "USD",
            {
                ("USD", "INR"): Decimal("166.50"),
                ("EUR", "USD"): Decimal("1.08"),
                ("USD", "JPY"): Decimal("150.10"),
            },
        ),
        {},
        Money("6.01", "USD"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Money("9.99", "EUR"),
            "JPY",
            {
                ("USD", "INR"): Decimal("83.25"),
                ("EUR", "USD"): Decimal("1.08"),
                ("USD", "JPY"): Decimal("150.10"),
            },
        ),
        {},
        Money("1619", "JPY"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Money("10.00", "EUR"),
            "JPY",
            {
                ("USD", "INR"): Decimal("83.25"),
                ("EUR", "USD"): Decimal("1.08"),
                ("USD", "JPY"): Decimal("300.20"),
            },
        ),
        {},
        Money("3242", "JPY"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Money("0.02", "USD"),
            "INR",
            {
                ("USD", "INR"): Decimal("83.25"),
                ("EUR", "USD"): Decimal("1.08"),
                ("USD", "JPY"): Decimal("150.10"),
            },
            RoundingMode.DOWN,
        ),
        {},
        Money("1.66", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Money("0.01", "USD"),
            "INR",
            {
                ("USD", "INR"): Decimal("83.25"),
                ("EUR", "USD"): Decimal("2.16"),
                ("USD", "JPY"): Decimal("150.10"),
            },
            RoundingMode.DOWN,
        ),
        {},
        Money("0.83", "INR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Money("5.01", "USD"),
            "usd",
            {
                ("USD", "INR"): Decimal("83.25"),
                ("EUR", "USD"): Decimal("1.08"),
                ("USD", "JPY"): Decimal("150.10"),
            },
        ),
        {},
        Money("5.01", "USD"),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Money("5.00", "USD"),
            "usd",
            {
                ("USD", "INR"): Decimal("83.26"),
                ("EUR", "USD"): Decimal("1.08"),
                ("USD", "JPY"): Decimal("150.10"),
            },
        ),
        {},
        Money("5.00", "USD"),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Money("5.00", "USD"),
            "usd",
            {
                ("USD", "INR"): Decimal("83.25"),
                ("EUR", "USD"): Decimal("1.07"),
                ("USD", "JPY"): Decimal("150.10"),
            },
        ),
        {},
        Money("5.00", "USD"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0484(args, kwargs, expected, after):
    assert convert(*args, **kwargs) == expected
    if after is not None:
        assert args == after
