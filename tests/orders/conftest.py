from collections.abc import Callable

import pytest

from shopcore.orders.model import Order

from .builders import build_order


@pytest.fixture
def order() -> Order:
    return build_order()


@pytest.fixture
def make_order() -> Callable[..., Order]:
    return build_order
