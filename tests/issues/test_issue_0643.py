"""Issue 0643. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.errors import PricingError
from shopcore.money.core import Money
from shopcore.pricing.bundles import Bundle, apply_bundles

CASES = [
    pytest.param(
        (
            [
                Bundle(
                    bundle_id="EARBUD_BOTTLE",
                    price=Money("3300.00", "INR"),
                    items={"ELC-0101": 1, "HOM-0201": 1},
                ),
                Bundle(
                    bundle_id="AUDIO",
                    price=Money("3999.00", "INR"),
                    items={"ELC-0101": 1, "ELC-0102": 1},
                ),
            ],
            {"ELC-0101": 1, "ELC-0102": 1, "HOM-0201": 1},
            {
                "ELC-0101": Money("2999.00", "INR"),
                "ELC-0102": Money("1499.00", "INR"),
                "HOM-0201": Money("649.00", "INR"),
            },
        ),
        {},
        (Money("499.00", "INR"), {"AUDIO": 1}),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Bundle(bundle_id="BOTTLE2", price=Money("1099.00", "INR"), items={"HOM-0201": 2}),
                Bundle(
                    bundle_id="AUDIO",
                    price=Money("3999.00", "INR"),
                    items={"ELC-0101": 1, "ELC-0102": 1},
                ),
            ],
            {"ELC-0101": 2, "ELC-0102": 1, "HOM-0201": 5},
            {
                "ELC-0101": Money("2999.00", "INR"),
                "ELC-0102": Money("1499.01", "INR"),
                "HOM-0201": Money("649.00", "INR"),
            },
        ),
        {},
        (Money("897.01", "INR"), {"AUDIO": 1, "BOTTLE2": 2}),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Bundle(
                    bundle_id="EARBUD_BOTTLE",
                    price=Money("3300.00", "INR"),
                    items={"ELC-0101": 1, "HOM-0201": 1},
                ),
                Bundle(
                    bundle_id="AUDIO",
                    price=Money("3999.00", "INR"),
                    items={"ELC-0101": 1, "ELC-0102": 1},
                ),
            ],
            {"ELC-0101": 1, "ELC-0102": 1, "HOM-0201": 1},
            {
                "ELC-0101": Money("2999.00", "INR"),
                "ELC-0102": Money("1499.00", "INR"),
                "HOM-0201": Money("1298.00", "INR"),
            },
        ),
        {},
        (Money("997.00", "INR"), {"EARBUD_BOTTLE": 1}),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Bundle(
                    bundle_id="EARBUD_BOTTLE",
                    price=Money("3300.00", "INR"),
                    items={"ELC-0101": 1, "HOM-0201": 2},
                ),
                Bundle(
                    bundle_id="AUDIO",
                    price=Money("3999.00", "INR"),
                    items={"ELC-0101": 1, "ELC-0102": 1},
                ),
            ],
            {"ELC-0101": 1, "ELC-0102": 1, "HOM-0201": 1},
            {
                "ELC-0101": Money("2999.00", "INR"),
                "ELC-0102": Money("1499.00", "INR"),
                "HOM-0201": Money("649.00", "INR"),
            },
        ),
        {},
        (Money("499.00", "INR"), {"AUDIO": 1}),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Bundle(
                    bundle_id="EARBUD_BOTTLE",
                    price=Money("3300.00", "INR"),
                    items={"ELC-0101": 1, "HOM-0201": 1},
                ),
                Bundle(
                    bundle_id="AUDIO",
                    price=Money("3999.00", "INR"),
                    items={"ELC-0101": 1, "ELC-0102": 1},
                ),
            ],
            {"ELC-0101": 1, "ELC-0102": 1, "HOM-0201": 0},
            {
                "ELC-0101": Money("2999.00", "INR"),
                "ELC-0102": Money("1499.00", "INR"),
                "HOM-0201": Money("649.00", "INR"),
            },
        ),
        {},
        (Money("499.00", "INR"), {"AUDIO": 1}),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            [
                Bundle(
                    bundle_id="AUDIO",
                    price=Money("3999.00", "INR"),
                    items={"ELC-0101": 1, "ELC-0102": 1},
                )
            ],
            {"HOM-0201": 1},
            {
                "ELC-0101": Money("2999.00", "INR"),
                "ELC-0102": Money("2998.00", "INR"),
                "HOM-0201": Money("649.00", "INR"),
            },
        ),
        {},
        (Money("0.00", "INR"), {}),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            [
                Bundle(bundle_id="BOTTLE2", price=Money("1099.00", "INR"), items={"HOM-0201": 2}),
                Bundle(
                    bundle_id="AUDIO",
                    price=Money("3999.00", "INR"),
                    items={"ELC-0101": 0, "ELC-0102": 1},
                ),
            ],
            {"ELC-0101": 2, "ELC-0102": 1, "HOM-0201": 5},
            {
                "ELC-0101": Money("2999.00", "INR"),
                "ELC-0102": Money("1499.00", "INR"),
                "HOM-0201": Money("649.00", "INR"),
            },
        ),
        {},
        ZeroDivisionError,
        None,
        id="case-7",
    ),
    pytest.param(
        (
            [],
            {},
            {
                "ELC-0101": Money("5998.00", "INR"),
                "ELC-0102": Money("1499.00", "INR"),
                "HOM-0201": Money("649.00", "INR"),
            },
        ),
        {},
        PricingError,
        None,
        id="case-8",
    ),
    pytest.param(
        (
            [],
            {},
            {
                "ELC-0101": Money("2999.00", "INR"),
                "ELC-0102": Money("1499.00", "INR"),
                "HOM-0201": Money("648.99", "INR"),
            },
        ),
        {},
        PricingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0643(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            apply_bundles(*args, **kwargs)
    else:
        assert apply_bundles(*args, **kwargs) == expected
    if after is not None:
        assert args == after
