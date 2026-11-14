"""Issue 0882. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import ShippingError
from shopcore.shipping.parcels import chargeable_weight_g

CASES = [
    pytest.param(
        (180, (0, 25, 2)),
        {},
        ShippingError,
        None,
        id="case-1",
    ),
    pytest.param(
        (180, (30, 0, 2)),
        {},
        ShippingError,
        None,
        id="case-2",
    ),
    pytest.param(
        (5200, (10, 10, 0)),
        {},
        ShippingError,
        None,
        id="case-3",
    ),
    pytest.param(
        (650, (0, 30, 5)),
        {},
        ShippingError,
        None,
        id="case-4",
    ),
    pytest.param(
        (650, (40, 0, 5)),
        {},
        ShippingError,
        None,
        id="case-5",
    ),
    pytest.param(
        (200, (10, 10, 0)),
        {},
        ShippingError,
        None,
        id="case-6",
    ),
    pytest.param(
        (179, (30, 25, 2)),
        {},
        300,
        None,
        id="case-7",
    ),
    pytest.param(
        (1, (10, 10, 10)),
        {},
        200,
        None,
        id="case-8",
    ),
    pytest.param(
        (0, (10, 10, 9)),
        {},
        ShippingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0882(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            chargeable_weight_g(*args, **kwargs)
    else:
        assert chargeable_weight_g(*args, **kwargs) == expected
    if after is not None:
        assert args == after
