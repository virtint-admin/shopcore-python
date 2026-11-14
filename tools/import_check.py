"""Import every module of the ``shopcore`` package and load the seed data.

Used by ``make build``: exits non-zero if any module fails to import.
"""

from __future__ import annotations

import importlib
import pkgutil
import sys
import traceback


def main() -> int:
    import shopcore

    failed = 0
    names = ["shopcore"] + [
        m.name for m in pkgutil.walk_packages(shopcore.__path__, prefix="shopcore.")
    ]
    for name in names:
        try:
            importlib.import_module(name)
        except Exception:  # report every broken module, not just the first
            failed += 1
            print(f"import failed: {name}", file=sys.stderr)
            traceback.print_exc()
    if not failed:
        from shopcore.catalog.products import load_seed_products
        from shopcore.shipping.rates import load_seed_rate_card
        from shopcore.tax.rules import load_seed_rules

        load_seed_products()
        load_seed_rules()
        load_seed_rate_card()
    print(f"build: imported {len(names) - failed}/{len(names)} modules")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
