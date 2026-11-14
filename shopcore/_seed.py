"""Access to the seed data files bundled in ``shopcore/data``."""

from __future__ import annotations

import csv
import io
import json
from importlib import resources
from typing import Any


def _read_seed_text(name: str) -> str:
    return (resources.files("shopcore") / "data" / name).read_text(encoding="utf-8")


def _read_seed_csv(name: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(_read_seed_text(name))))


def _read_seed_json(name: str) -> Any:
    return json.loads(_read_seed_text(name))
