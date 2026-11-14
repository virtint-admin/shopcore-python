"""Issue 0931. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.shipping.rates import fuel_surcharge

CASES = [
    pytest.param(
        (Money("55.00", "INR"), Decimal("0")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("55.01", "INR"), Decimal("0")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("54.99", "INR"), Decimal("0")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("110.00", "INR"), Decimal("0")),
        {},
        Money("0.00", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("80.01", "INR"), Decimal("12.5")),
        {},
        Money("10.00", "INR"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("80.00", "INR"), Decimal("12.6")),
        {},
        Money("10.08", "INR"),
        None,
        id="case-6",
    ),
    pytest.param(
        (Money("110.00", "INR"), Decimal("7")),
        {},
        Money("7.70", "INR"),
        None,
        id="case-7",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0931(args, kwargs, expected, after):
    assert fuel_surcharge(*args, **kwargs) == expected
    if after is not None:
        assert args == after
