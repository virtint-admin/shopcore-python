"""Issue 0977. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.tax.calc import gross_from_net

CASES = [
    pytest.param(
        (Money("200.00", "USD"), Decimal("8.875")),
        {},
        Money("217.75", "USD"),
        None,
        id="case-1",
    ),
    pytest.param(
        (Money("0.11", "INR"), Decimal("18")),
        {},
        Money("0.13", "INR"),
        None,
        id="case-2",
    ),
    pytest.param(
        (Money("0.20", "INR"), Decimal("18")),
        {},
        Money("0.24", "INR"),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("0.09", "INR"), Decimal("18")),
        {},
        Money("0.11", "INR"),
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("400.00", "USD"), Decimal("8.875")),
        {},
        Money("435.50", "USD"),
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("200.00", "USD"), Decimal("8.874")),
        {},
        Money("217.75", "USD"),
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0977(args, kwargs, expected, after):
    assert gross_from_net(*args, **kwargs) == expected
    if after is not None:
        assert args == after
