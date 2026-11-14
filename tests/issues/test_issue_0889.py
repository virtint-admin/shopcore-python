"""Issue 0889. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import ShippingError
from shopcore.shipping.parcels import packed_weight_g

CASES = [
    pytest.param(
        ([1000],),
        {},
        1100,
        None,
        id="case-1",
    ),
    pytest.param(
        ([999],),
        {},
        1099,
        None,
        id="case-2",
    ),
    pytest.param(
        ([180, 0],),
        {},
        239,
        None,
        id="case-3",
    ),
    pytest.param(
        ([181, 190],),
        {},
        440,
        None,
        id="case-4",
    ),
    pytest.param(
        ([179, 190],),
        {},
        438,
        None,
        id="case-5",
    ),
    pytest.param(
        ([0, 190],),
        {},
        250,
        None,
        id="case-6",
    ),
    pytest.param(
        ([],),
        {},
        ShippingError,
        None,
        id="case-7",
    ),
    pytest.param(
        ([0],),
        {},
        50,
        None,
        id="case-8",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0889(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            packed_weight_g(*args, **kwargs)
    else:
        assert packed_weight_g(*args, **kwargs) == expected
    if after is not None:
        assert args == after
