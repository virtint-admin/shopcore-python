"""Issue 0904. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import ShippingError
from shopcore.shipping.parcels import split_into_parcels

CASES = [
    pytest.param(
        ([1000],),
        {"max_g": 1000},
        [[1000]],
        None,
        id="case-1",
    ),
    pytest.param(
        ([1001],),
        {"max_g": 1001},
        [[1001]],
        None,
        id="case-2",
    ),
    pytest.param(
        ([5199, 1100, 400, 650, 5100],),
        {"max_g": 6000},
        [[5199, 650], [5100, 400], [1100]],
        None,
        id="case-3",
    ),
    pytest.param(
        ([0, 300, 200],),
        {},
        ShippingError,
        None,
        id="case-4",
    ),
    pytest.param(
        ([500, 500],),
        {"max_g": 1000},
        [[500, 500]],
        None,
        id="case-5",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0904(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            split_into_parcels(*args, **kwargs)
    else:
        assert split_into_parcels(*args, **kwargs) == expected
    if after is not None:
        assert args == after
