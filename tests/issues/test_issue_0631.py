"""Issue 0631. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.money.core import Money
from shopcore.pricing.bundles import Bundle, is_bundle_complete

CASES = [
    pytest.param(
        (
            Bundle(
                bundle_id="AUDIO",
                price=Money("3999.00", "INR"),
                items={"ELC-0101": 1, "ELC-0102": 1},
            ),
            {"ELC-0101": 1, "ELC-0102": 1},
        ),
        {},
        True,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Bundle(bundle_id="BOTTLE2", price=Money("1099.00", "INR"), items={"HOM-0201": 2}),
            {"HOM-0201": 2},
        ),
        {},
        True,
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Bundle(
                bundle_id="AUDIO",
                price=Money("3999.00", "INR"),
                items={"ELC-0101": 1, "ELC-0102": 1},
            ),
            {"ELC-0101": 1, "ELC-0102": 2},
        ),
        {},
        True,
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Bundle(
                bundle_id="AUDIO",
                price=Money("3999.01", "INR"),
                items={"ELC-0101": 1, "ELC-0102": 1},
            ),
            {"ELC-0101": 1, "ELC-0102": 1},
        ),
        {},
        True,
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Bundle(bundle_id="BOTTLE2", price=Money("1099.00", "INR"), items={"HOM-0201": 2}),
            {"HOM-0201": 3},
        ),
        {},
        True,
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Bundle(bundle_id="BOTTLE2", price=Money("1099.01", "INR"), items={"HOM-0201": 2}),
            {"HOM-0201": 2},
        ),
        {},
        True,
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Bundle(bundle_id="BOTTLE2", price=Money("1099.00", "INR"), items={"HOM-0201": 1}),
            {"HOM-0201": 2},
        ),
        {},
        True,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Bundle(bundle_id="BOTTLE2", price=Money("1099.01", "INR"), items={"HOM-0201": 2}),
            {"HOM-0201": 1},
        ),
        {},
        False,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Bundle(bundle_id="BOTTLE2", price=Money("2198.00", "INR"), items={"HOM-0201": 2}),
            {"HOM-0201": 1},
        ),
        {},
        False,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0631(args, kwargs, expected, after):
    assert is_bundle_complete(*args, **kwargs) == expected
    if after is not None:
        assert args == after
