"""Issue 0105. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.catalog.products import Product, discount_from_mrp_percent
from shopcore.money.core import Money

CASES = [
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="ELC",
                brand="Acme",
                price=Money("0.00", "INR"),
                mrp=Money("0.00", "INR"),
                weight_g=100,
                dims_cm=(10, 10, 10),
                active=True,
                tags=(),
            ),
        ),
        {},
        Decimal("0.00"),
        None,
        id="case-1",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="ELC",
                brand="Acme",
                price=Money("0.01", "INR"),
                mrp=Money("0.00", "INR"),
                weight_g=100,
                dims_cm=(10, 10, 10),
                active=True,
                tags=(),
            ),
        ),
        {},
        Decimal("0.00"),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="ELC",
                brand="Acme",
                price=Money("0.00", "INR"),
                mrp=Money("0.00", "INR"),
                weight_g=100,
                dims_cm=(10, 10, 9),
                active=True,
                tags=(),
            ),
        ),
        {},
        Decimal("0.00"),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="ELC",
                brand="Acme",
                price=Money("0.00", "INR"),
                mrp=Money("0.00", "INR"),
                weight_g=100,
                dims_cm=(10, 9, 10),
                active=True,
                tags=(),
            ),
        ),
        {},
        Decimal("0.00"),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="ELC",
                brand="Acme",
                price=Money("0.00", "INR"),
                mrp=Money("0.00", "INR"),
                weight_g=100,
                dims_cm=(9, 10, 10),
                active=True,
                tags=(),
            ),
        ),
        {},
        Decimal("0.00"),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="ELC",
                brand="Acme",
                price=Money("0.00", "INR"),
                mrp=Money("0.00", "INR"),
                weight_g=100,
                dims_cm=(10, 10, 11),
                active=True,
                tags=(),
            ),
        ),
        {},
        Decimal("0.00"),
        None,
        id="case-6",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="ELC",
                brand="Acme",
                price=Money("120.00", "INR"),
                mrp=Money("120.00", "INR"),
                weight_g=100,
                dims_cm=(10, 10, 10),
                active=True,
                tags=(),
            ),
        ),
        {},
        Decimal("0.00"),
        None,
        id="case-7",
    ),
    pytest.param(
        (
            Product(
                sku="APP-0001-BLK-M",
                name="Classic Crew Tee",
                category="APP",
                brand="Kora",
                price=Money("499.00", "INR"),
                mrp=Money("599.00", "INR"),
                weight_g=180,
                dims_cm=(30, 24, 2),
                active=True,
                tags=("cotton", "tee", "basics"),
            ),
        ),
        {},
        Decimal("16.69"),
        None,
        id="case-8",
    ),
    pytest.param(
        (
            Product(
                sku="ELC-0101",
                name="Thing",
                category="ELC",
                brand="Acme",
                price=Money("120.00", "INR"),
                mrp=Money("240.00", "INR"),
                weight_g=100,
                dims_cm=(10, 10, 10),
                active=True,
                tags=(),
            ),
        ),
        {},
        Decimal("50.00"),
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0105(args, kwargs, expected, after):
    assert discount_from_mrp_percent(*args, **kwargs) == expected
    if after is not None:
        assert args == after
