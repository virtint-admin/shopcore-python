"""Shared fixtures. Every fixture is deterministic: fixed clocks, seed data only."""

from datetime import UTC, datetime

import pytest

from shopcore.catalog.products import Product, load_seed_products
from shopcore.tax.rules import TaxRule, load_seed_rules

# A fixed "now" used across the suite: Monday 9 Nov 2026, 10:00 UTC (15:30 IST).
NOW = datetime(2026, 11, 9, 10, 0, tzinfo=UTC)


@pytest.fixture
def now() -> datetime:
    return NOW


@pytest.fixture
def products() -> list[Product]:
    return load_seed_products()


@pytest.fixture
def tax_rules() -> dict[str, TaxRule]:
    return load_seed_rules()
