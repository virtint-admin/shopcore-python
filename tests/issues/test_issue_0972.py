"""Issue 0972. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.tax.calc import TaxLine, line_tax
from shopcore.tax.rules import TaxRule

CASES = [
    pytest.param(
        (
            TaxLine(amount=Money("12.00", "GBP"), category="BKS"),
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("40"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
        ),
        {},
        Money("0.00", "GBP"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            TaxLine(amount=Money("12.01", "GBP"), category="BKS"),
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
        ),
        {},
        Money("0.00", "GBP"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            TaxLine(amount=Money("12.00", "GBP"), category="BKS"),
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("21"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
        ),
        {},
        Money("0.00", "GBP"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            TaxLine(amount=Money("12.00", "GBP"), category="BKS"),
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("1")},
            ),
        ),
        {},
        Money("0.00", "GBP"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            TaxLine(amount=Money("24.00", "GBP"), category="BKS"),
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
        ),
        {},
        Money("0.00", "GBP"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            TaxLine(amount=Money("11.99", "GBP"), category="BKS"),
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
        ),
        {},
        Money("0.00", "GBP"),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            TaxLine(amount=Money("200.00", "INR"), category="GRC"),
            TaxRule(
                region="IN-KA",
                name="GST",
                rate=Decimal("18"),
                inclusive=False,
                taxes_shipping=False,
                category_rates={"BKS": Decimal("-1"), "GRC": Decimal("5"), "APP": Decimal("12")},
            ),
        ),
        {},
        Money("10.00", "INR"),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            TaxLine(amount=Money("240.00", "GBP"), category=None),
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
        ),
        {},
        Money("40.00", "GBP"),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            TaxLine(amount=Money("120.00", "GBP"), category=None),
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("1"), "GRC": Decimal("0")},
            ),
        ),
        {},
        Money("20.00", "GBP"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0972(args, kwargs, expected, after):
    assert line_tax(*args, **kwargs) == expected
    if after is not None:
        assert args == after
