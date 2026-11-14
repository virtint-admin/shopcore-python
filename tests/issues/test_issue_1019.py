"""Issue 1019. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.tax.rules import TaxRule, rate_for_category

CASES = [
    pytest.param(
        (
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
            "bks",
        ),
        {},
        Decimal("0"),
        None,
        id="case-1",
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
            "bks",
        ),
        {},
        Decimal("0"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("20"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("1")},
            ),
            "bks",
        ),
        {},
        Decimal("0"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("40"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
            "bks",
        ),
        {},
        Decimal("0"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("21"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
            "bks",
        ),
        {},
        Decimal("0"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            TaxRule(
                region="GB",
                name="VAT",
                rate=Decimal("19"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("0")},
            ),
            "bks",
        ),
        {},
        Decimal("0"),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            TaxRule(
                region="IN-KA",
                name="GST",
                rate=Decimal("18"),
                inclusive=False,
                taxes_shipping=False,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("4"), "APP": Decimal("12")},
            ),
            "ELC",
        ),
        {},
        Decimal("18"),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            TaxRule(
                region="IN-KA",
                name="GST",
                rate=Decimal("18"),
                inclusive=False,
                taxes_shipping=False,
                category_rates={"BKS": Decimal("0"), "GRC": Decimal("5"), "APP": Decimal("11")},
            ),
            "ELC",
        ),
        {},
        Decimal("18"),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            TaxRule(
                region="DE",
                name="MwSt",
                rate=Decimal("18"),
                inclusive=True,
                taxes_shipping=True,
                category_rates={"BKS": Decimal("7"), "GRC": Decimal("7")},
            ),
            None,
        ),
        {},
        Decimal("18"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_1019(args, kwargs, expected, after):
    assert rate_for_category(*args, **kwargs) == expected
    if after is not None:
        assert args == after
