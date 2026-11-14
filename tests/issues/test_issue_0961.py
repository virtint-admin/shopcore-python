"""Issue 0961. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import ShippingError
from shopcore.shipping.zones import shipping_zone

CASES = [
    pytest.param(
        ("560001", "560034"),
        {},
        "LOCAL",
        None,
        id="case-1",
    ),
    pytest.param(
        ("560001", "575001"),
        {},
        "REGIONAL",
        None,
        id="case-2",
    ),
    pytest.param(
        ("560001", "110001"),
        {},
        "NATIONAL",
        None,
        id="case-3",
    ),
    pytest.param(
        ("781001", "781005"),
        {},
        "REMOTE",
        None,
        id="case-4",
    ),
    pytest.param(
        ("560001", "12345"),
        {},
        ShippingError,
        None,
        id="case-5",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0961(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            shipping_zone(*args, **kwargs)
    else:
        assert shipping_zone(*args, **kwargs) == expected
    if after is not None:
        assert args == after
