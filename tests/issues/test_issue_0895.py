"""Issue 0895. Make this test pass by fixing the application code, not the test."""

import pytest

from shopcore.shipping.parcels import validate_parcel

CASES = [
    pytest.param(
        (0, (0, 10, 10)),
        {},
        ["weight must be positive", "dimensions must be positive"],
        None,
        id="case-1",
    ),
    pytest.param(
        (30000, (150, 10, 0)),
        {},
        ["dimensions must be positive"],
        None,
        id="case-2",
    ),
    pytest.param(
        (30001, (10, 0, 10)),
        {},
        ["weight 30001 g exceeds 30000 g", "dimensions must be positive"],
        None,
        id="case-3",
    ),
    pytest.param(
        (30001, (10, 10, 0)),
        {},
        ["weight 30001 g exceeds 30000 g", "dimensions must be positive"],
        None,
        id="case-4",
    ),
    pytest.param(
        (0, (0, 9, 10)),
        {},
        ["weight must be positive", "dimensions must be positive"],
        None,
        id="case-5",
    ),
    pytest.param(
        (-1, (0, 10, 10)),
        {},
        ["weight must be positive", "dimensions must be positive"],
        None,
        id="case-6",
    ),
    pytest.param(
        (1200, (40, 30, 5)),
        {},
        [],
        None,
        id="case-7",
    ),
    pytest.param(
        (30000, (150, 10, 10)),
        {},
        [],
        None,
        id="case-8",
    ),
    pytest.param(
        (499, (151, 10, 10)),
        {},
        ["longest side 151 cm exceeds 150 cm"],
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0895(args, kwargs, expected, after):
    assert validate_parcel(*args, **kwargs) == expected
    if after is not None:
        assert args == after
