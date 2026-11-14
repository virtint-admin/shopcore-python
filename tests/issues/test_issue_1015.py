"""Issue 1015. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.tax.rules import TaxRule, tax_rate_label

CASES = [
    pytest.param(
        (
            TaxRule(
                region="IN-KA",
                name="GST",
                rate=Decimal("36"),
                inclusive=False,
                taxes_shipping=False,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("5"), "APP": Decimal("12")},
            ),
        ),
        {},
        "GST 36%",
        None,
        id="case-1",
    ),
    pytest.param(
        (
            TaxRule(
                region="US-NY",
                name="Sales tax",
                rate=Decimal("8.874"),
                inclusive=False,
                taxes_shipping=True,
                category_rates={"GRC": Decimal("0")},
            ),
        ),
        {},
        "Sales tax 8.874%",
        None,
        id="case-2",
    ),
    pytest.param(
        (
            TaxRule(
                region="US-NY",
                name="Sales tax",
                rate=Decimal("17.750"),
                inclusive=False,
                taxes_shipping=True,
                category_rates={"GRC": Decimal("0")},
            ),
        ),
        {},
        "Sales tax 17.75%",
        None,
        id="case-3",
    ),
    pytest.param(
        (
            TaxRule(
                region="DE",
                name="MwSt",
                rate=Decimal("38"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("7"), "GRC": Decimal("7")},
            ),
            "BKS",
        ),
        {},
        "MwSt 7%",
        None,
        id="case-4",
    ),
    pytest.param(
        (
            TaxRule(
                region="DE",
                name="MwSt",
                rate=Decimal("19"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("7"), "GRC": Decimal("8")},
            ),
            "BKS",
        ),
        {},
        "MwSt 7%",
        None,
        id="case-5",
    ),
    pytest.param(
        (
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("-1")},
            ),
            "GRC",
        ),
        {},
        "VAT -1%",
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_1015(args, kwargs, expected, after):
    assert tax_rate_label(*args, **kwargs) == expected
    if after is not None:
        assert args == after
