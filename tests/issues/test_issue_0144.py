"""Issue 0144. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.catalog.variants import sort_sizes

CASES = [
    pytest.param(
        (["34", "L", "30"],),
        {},
        ["L", "30", "34"],
        None,
        id="case-1",
    ),
    pytest.param(
        (["30", "L", "34"],),
        {},
        ["L", "30", "34"],
        None,
        id="case-2",
    ),
    pytest.param(
        (["34", "L"],),
        {},
        ["L", "34"],
        None,
        id="case-3",
    ),
    pytest.param(
        (["XL", "S", "M", "XS"],),
        {},
        ["XS", "S", "M", "XL"],
        None,
        id="case-4",
    ),
    pytest.param(
        (["XL", "S", "M"],),
        {},
        ["S", "M", "XL"],
        None,
        id="case-5",
    ),
    pytest.param(
        (["XS", "M", "S", "XL"],),
        {},
        ["XS", "S", "M", "XL"],
        None,
        id="case-6",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0144(args, kwargs, expected, after):
    assert sort_sizes(*args, **kwargs) == expected
    if after is not None:
        assert args == after
