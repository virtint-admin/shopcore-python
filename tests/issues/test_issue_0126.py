"""Issue 0126. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.catalog.products import Product, validate_product
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Product(
                sku="ELC-0102",
                name="USB-C Charger 65W",
                category="ELC",
                brand="Voltix",
                price=Money("1499.00", "INR"),
                mrp=Money("1999.00", "INR"),
                weight_g=150,
                dims_cm=(8, 6, 3),
                active=True,
                tags=("charger", "usb-c"),
            ),
        ),
        {},
        [],
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Wireless Earbuds",
                category="ELC",
                brand="Sonica",
                price=Money("2999.00", "INR"),
                mrp=Money("4999.00", "INR"),
                weight_g=120,
                dims_cm=(10, 0, 4),
                active=True,
                tags=("audio", "bluetooth"),
            ),
        ),
        {},
        ["dimensions must be positive"],
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Product(
                sku="HOM-0201",
                name="Steel Water Bottle",
                category="HOM",
                brand="Hydra",
                price=Money("649.00", "INR"),
                mrp=Money("799.00", "INR"),
                weight_g=351,
                dims_cm=(8, 8, 27),
                active=True,
                tags=("kitchen", "bottle"),
            ),
        ),
        {},
        [],
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Product(
                sku="GRC-0402",
                name="Cold Pressed Coconut Oil 1L",
                category="GRC",
                brand="Kerala Groves",
                price=Money("420.00", "INR"),
                mrp=Money("450.00", "INR"),
                weight_g=1000,
                dims_cm=(10, 9, 25),
                active=True,
                tags=("oil", "cooking"),
            ),
        ),
        {},
        [],
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Product(
                sku="GRC-0403",
                name="Basmati Rice 5kg",
                category="GRC",
                brand="Doon Fields",
                price=Money("899.00", "INR"),
                mrp=Money("1900.00", "INR"),
                weight_g=5100,
                dims_cm=(40, 25, 10),
                active=True,
                tags=("rice", "staples"),
            ),
        ),
        {},
        [],
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="TOY",
                brand="Acme",
                price=Money("100.00", "INR"),
                mrp=Money("120.00", "INR"),
                weight_g=100,
                dims_cm=(10, 10, 0),
                active=True,
                tags=(),
            ),
        ),
        {},
        ["category does not match sku", "dimensions must be positive"],
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Product(
                sku="APP-0002-BLU-32",
                name="Slim Denim Jeans",
                category="APP",
                brand="Indigo Mill",
                price=Money("1899.00", "INR"),
                mrp=Money("2499.00", "INR"),
                weight_g=650,
                dims_cm=(40, 31, 5),
                active=True,
                tags=("denim", "jeans"),
            ),
        ),
        {},
        [],
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Product(
                sku="APP-0003-GRN-S",
                name="Linen Kurta",
                category="APP",
                brand="Kora",
                price=Money("1298.99", "INR"),
                mrp=Money("1299.00", "INR"),
                weight_g=300,
                dims_cm=(35, 28, 3),
                active=True,
                tags=("linen", "kurta", "festive"),
            ),
        ),
        {},
        [],
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Product(
                sku="APP-0003-GRN-S",
                name="Linen Kurta",
                category="APP",
                brand="Kora",
                price=Money("1299.00", "INR"),
                mrp=Money("1299.00", "INR"),
                weight_g=300,
                dims_cm=(34, 28, 3),
                active=True,
                tags=("linen", "kurta", "festive"),
            ),
        ),
        {},
        [],
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0126(args, kwargs, expected, after):
    assert validate_product(*args, **kwargs) == expected
    if after is not None:
        assert args == after
