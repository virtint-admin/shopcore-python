from datetime import UTC, datetime

import pytest

from shopcore.cart.cart import Cart, add_item, new_cart
from shopcore.catalog.products import Product, index_by_sku, load_seed_products

T0 = datetime(2026, 11, 9, 10, 0, tzinfo=UTC)


@pytest.fixture
def catalog() -> dict[str, Product]:
    return index_by_sku(load_seed_products())


@pytest.fixture
def cart(catalog: dict[str, Product]) -> Cart:
    """Earbuds x1 (2999), Pragmatic Coder x2 (699), Assam Tea x1 (325): subtotal 4722.00."""
    c = new_cart("C1", "INR", T0, customer_id="U1")
    add_item(c, catalog["ELC-0101"], 1, T0)
    add_item(c, catalog["BKS-0301"], 2, T0)
    add_item(c, catalog["GRC-0401"], 1, T0)
    return c
