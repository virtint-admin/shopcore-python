"""Issue 0085. Make this test pass by fixing the application code, not the test."""

from decimal import Decimal

import pytest

from shopcore.catalog.products import Product, price_range
from shopcore.errors import CatalogError
from shopcore.money.core import Money

CASES = [
    pytest.param(
        ([],),
        {},
        CatalogError,
        None,
        id="case-1",
    ),
    pytest.param(
        (
            [
                Product(
                    sku="ELC-0101",
                    name="Thing",
                    category="ELC",
                    brand="Acme",
                    price=Money("5.00", "INR"),
                    mrp=Money("240.00", "INR"),
                    weight_g=100,
                    dims_cm=(10, 10, 10),
                    active=True,
                    tags=(),
                )
            ],
        ),
        {},
        (Money("5.00", "INR"), Money("5.00", "INR")),
        None,
        id="case-2",
    ),
    pytest.param(
        (
            [
                Product(
                    sku="ELC-0101",
                    name="Thing",
                    category="ELC",
                    brand="Acme",
                    price=Money("5.00", "INR"),
                    mrp=Money("120.00", "INR"),
                    weight_g=100,
                    dims_cm=(0, 10, 10),
                    active=True,
                    tags=(),
                )
            ],
        ),
        {},
        (Money("5.00", "INR"), Money("5.00", "INR")),
        None,
        id="case-3",
    ),
    pytest.param(
        (
            [
                Product(
                    sku="ELC-0101",
                    name="Thing",
                    category="ELC",
                    brand="Acme",
                    price=Money("5.00", "INR"),
                    mrp=Money("120.00", "INR"),
                    weight_g=100,
                    dims_cm=(10, 0, 10),
                    active=True,
                    tags=(),
                )
            ],
        ),
        {},
        (Money("5.00", "INR"), Money("5.00", "INR")),
        None,
        id="case-4",
    ),
    pytest.param(
        (
            [
                Product(
                    sku="ELC-0101",
                    name="Thing",
                    category="ELC",
                    brand="Acme",
                    price=Money("5.00", "INR"),
                    mrp=Money("120.00", "INR"),
                    weight_g=100,
                    dims_cm=(9, 10, 10),
                    active=True,
                    tags=(),
                )
            ],
        ),
        {},
        (Money("5.00", "INR"), Money("5.00", "INR")),
        None,
        id="case-5",
    ),
    pytest.param(
        (
            [
                Product(
                    sku="ELC-0101",
                    name="Thing",
                    category="ELC",
                    brand="Acme",
                    price=Money("5.00", "INR"),
                    mrp=Money("120.00", "INR"),
                    weight_g=0,
                    dims_cm=(10, 10, 10),
                    active=True,
                    tags=(),
                )
            ],
        ),
        {},
        (Money("5.00", "INR"), Money("5.00", "INR")),
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0085(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            price_range(*args, **kwargs)
    else:
        assert price_range(*args, **kwargs) == expected
    if after is not None:
        assert args == after
