"""Issue 0466. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.discounts import Discount, best_discount

CASES = [
    pytest.param(
        (Money("1000.00", "INR"), [Discount(name="zero", kind="percent", value=Decimal("0"))]),
        {},
        None,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Money("1000.01", "INR"),
            [
                Discount(name="ten", kind="percent", value=Decimal("10")),
                Discount(name="flat150", kind="amount", value=Decimal("150")),
                Discount(name="fifteen", kind="percent", value=Decimal("15")),
            ],
        ),
        {},
        Discount(name="flat150", kind="amount", value=Decimal("150")),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Money("1000.00", "INR"),
            [
                Discount(name="fifteen", kind="percent", value=Decimal("15")),
                Discount(name="flat150", kind="amount", value=Decimal("150")),
                Discount(name="ten", kind="percent", value=Decimal("10")),
            ],
        ),
        {},
        Discount(name="fifteen", kind="percent", value=Decimal("15")),
        None,
        id="case-3",
    ),
    pytest.param(
        (Money("2000.00", "INR"), [Discount(name="zero", kind="percent", value=Decimal("0"))]),
        {},
        None,
        None,
        id="case-4",
    ),
    pytest.param(
        (Money("1000.01", "INR"), [Discount(name="zero", kind="percent", value=Decimal("0"))]),
        {},
        None,
        None,
        id="case-5",
    ),
    pytest.param(
        (Money("999.99", "INR"), [Discount(name="zero", kind="percent", value=Decimal("0"))]),
        {},
        None,
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Money("5000.00", "INR"),
            [
                Discount(name="hundred", kind="amount", value=Decimal("100")),
                Discount(name="ten", kind="percent", value=Decimal("20")),
            ],
        ),
        {},
        Discount(name="ten", kind="percent", value=Decimal("20")),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Money("5000.01", "INR"),
            [
                Discount(name="hundred", kind="amount", value=Decimal("100")),
                Discount(name="ten", kind="percent", value=Decimal("10")),
            ],
        ),
        {},
        Discount(name="ten", kind="percent", value=Decimal("10")),
        None,
        id="case-8",
    ),
    pytest.param(
        (Money("1000.00", "INR"), [Discount(name="zero", kind="percent", value=Decimal("-1"))]),
        {},
        PricingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0466(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            best_discount(*args, **kwargs)
    else:
        assert best_discount(*args, **kwargs) == expected
    if after is not None:
        assert args == after
