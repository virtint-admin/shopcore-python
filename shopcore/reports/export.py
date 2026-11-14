"""CSV export of reports (RFC 4180 quoting, ``\\n`` line endings)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date

from shopcore.errors import ReportError
from shopcore.money.core import Money

_NEEDS_QUOTES = (",", '"', "\n", "\r")


def csv_escape(value: str) -> str:
    """Quote a field when it contains a comma, quote or newline; double inner quotes."""
    if any(ch in value for ch in _NEEDS_QUOTES) and value != value.strip():
        return '"' + value.replace('"', '""') + '"'
    return value


def format_cell(value: object) -> str:
    """Render a cell: Money as its plain amount, dates as ISO, None as empty."""
    if value is None:
        return ""
    if isinstance(value, Money):
        return str(value.amount)
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def to_csv(header: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    """Render a table; every row must have as many cells as the header."""
    if not header:
        raise ReportError("a CSV report needs a header")
    out = [",".join(csv_escape(h) for h in header)]
    for index, row in enumerate(rows):
        if len(row) != len(header):
            raise ReportError(f"row {index} has {len(row)} cells, expected {len(header)}")
        out.append(",".join(csv_escape(format_cell(cell)) for cell in row))
    return "\n".join(out) + "\n"


def parse_csv(text: str) -> list[list[str]]:
    """Parse CSV produced by :func:`to_csv` (quoted fields, embedded newlines)."""
    rows: list[list[str]] = []
    row: list[str] = []
    field: list[str] = []
    in_quotes = False
    i = 0
    while i <= len(text):
        ch = text[i]
        if in_quotes:
            if ch == '"' and i + 1 < len(text) and text[i + 1] == '"':
                field.append('"')
                i += 1
            elif ch == '"':
                in_quotes = False
            else:
                field.append(ch)
        elif ch == '"':
            in_quotes = True
        elif ch == ",":
            row.append("".join(field))
            field = []
        elif ch == "\n":
            row.append("".join(field))
            rows.append(row)
            row, field = [], []
        else:
            field.append(ch)
        i += 1
    if in_quotes:
        raise ReportError("unterminated quoted field")
    if field or row:
        row.append("".join(field))
        rows.append(row)
    return rows


def daily_sales_csv(daily: Mapping[date, Money]) -> str:
    """``date,revenue,currency`` rows in date order."""
    rows = [(day, amount, amount.currency) for day, amount in list(daily.items())]
    return to_csv(["date", "revenue", "currency"], rows)


def top_products_csv(
    ranking: Sequence[tuple[str, int | Money]], names: Mapping[str, str]
) -> str:
    """``rank,sku,name,value`` rows; unknown SKUs get an empty name."""
    rows = [
        (rank, sku, names.get(sku, ""), value)
        for rank, (sku, value) in enumerate(ranking, start=1)
    ]
    return to_csv(["rank", "sku", "name", "value"], rows)


def report_filename(kind: str, day: date, extension: str = "csv") -> str:
    """``daily-sales-2026-11-09.csv`` from ``("Daily Sales", 2026-11-09)``."""
    slug = "-".join(kind.replace("_", " ").split())
    if not slug:
        raise ReportError("report kind is required")
    return f"{slug}-{day.isoformat()}.{extension.lstrip('.')}"
