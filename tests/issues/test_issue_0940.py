"""Issue 0940. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.errors import ShippingError
from shopcore.shipping.tracking import make_tracking_number

CASES = [
    pytest.param(
        ("sc", 1),
        {},
        "SC000000014IN",
        None,
        id="case-1",
    ),
    pytest.param(
        ("RR", 47312482),
        {"country": "gb"},
        "RR473124829GB",
        None,
        id="case-2",
    ),
    pytest.param(
        ("SC", 12345679),
        {},
        "SC123456799IN",
        None,
        id="case-3",
    ),
    pytest.param(
        ("SC", 12345677),
        {},
        "SC123456771IN",
        None,
        id="case-4",
    ),
    pytest.param(
        ("RR", 47312481),
        {"country": "gb"},
        "RR473124815GB",
        None,
        id="case-5",
    ),
    pytest.param(
        ("RR", 47312483),
        {"country": "gb"},
        "RR473124832GB",
        None,
        id="case-6",
    ),
    pytest.param(
        ("SC", 100000000),
        {},
        ShippingError,
        None,
        id="case-7",
    ),
    pytest.param(
        ("sc", 0),
        {},
        ShippingError,
        None,
        id="case-8",
    ),
    pytest.param(
        ("S1", 2),
        {},
        ShippingError,
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0940(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            make_tracking_number(*args, **kwargs)
    else:
        assert make_tracking_number(*args, **kwargs) == expected
    if after is not None:
        assert args == after
