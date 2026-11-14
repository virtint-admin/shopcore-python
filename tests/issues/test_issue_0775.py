"""Issue 0775. Make this test pass by fixing the application code, not the test."""

import datetime

import pytest

from shopcore.errors import ReportError
from shopcore.reports.export import report_filename

CASES = [
    pytest.param(
        ("Daily Sales", datetime.date(2026, 11, 9)),
        {},
        "daily-sales-2026-11-09.csv",
        None,
        id="case-1",
    ),
    pytest.param(
        ("  Tax   by Region ", datetime.date(2026, 11, 9)),
        {},
        "tax-by-region-2026-11-09.csv",
        None,
        id="case-2",
    ),
    pytest.param(
        ("Daily Sales", datetime.date(2026, 11, 10)),
        {},
        "daily-sales-2026-11-10.csv",
        None,
        id="case-3",
    ),
    pytest.param(
        ("Daily Sales", datetime.date(2026, 11, 8)),
        {},
        "daily-sales-2026-11-08.csv",
        None,
        id="case-4",
    ),
    pytest.param(
        ("  Tax   by Region ", datetime.date(2026, 11, 8)),
        {},
        "tax-by-region-2026-11-08.csv",
        None,
        id="case-5",
    ),
    pytest.param(
        ("  Tax   by Region ", datetime.date(2026, 11, 10)),
        {},
        "tax-by-region-2026-11-10.csv",
        None,
        id="case-6",
    ),
    pytest.param(
        ("top_products", datetime.date(2026, 11, 9), ".json"),
        {},
        "top-products-2026-11-09.json",
        None,
        id="case-7",
    ),
    pytest.param(
        ("   ", datetime.date(2026, 11, 9)),
        {},
        ReportError,
        None,
        id="case-8",
    ),
    pytest.param(
        ("top_products", datetime.date(2026, 11, 8), ".json"),
        {},
        "top-products-2026-11-08.json",
        None,
        id="case-9",
    ),
]


@pytest.mark.parametrize(("args", "kwargs", "expected", "after"), CASES)
def test_issue_0775(args, kwargs, expected, after):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            report_filename(*args, **kwargs)
    else:
        assert report_filename(*args, **kwargs) == expected
    if after is not None:
        assert args == after
