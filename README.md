# ShopCore (Python)

> **Learners:** start with [LEARNERS.md](LEARNERS.md), how to pick an issue, fix it and get it checked.

ShopCore is the back-office engine of a fictional Indian online store: money and
FX, the product catalogue, inventory across three warehouses (BLR, BOM, DEL),
pricing and coupons, GST and VAT, carts, orders, shipping, a double-entry ledger
and sales reports. The runtime is pure Python 3.12 standard library.

## Quick start

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
make build test lint coverage
```

`main` carries every open issue: in a full `make test` run the tests named in open
issues fail until someone fixes them, and everything else passes.

Every target writes to `reports/`: JUnit XML in `reports/junit/`, ruff findings in
`reports/lint.json`, Cobertura coverage in `reports/coverage.xml`.

Run a single test the same way the grader does:

```sh
make test TESTS="tests/tax/test_rules.py::test_apply_regional_tax_excludes_shipping"
```

## How pull requests are graded

Fork the repository, fix your assigned issue and open a pull request against `main`.
`.github/workflows/virtint-review.yml` then runs only the test(s) of your issue, with
`tests/`, CI files and the test configuration taken from `main`. A pull request that
changes those files is not graded. Passing pull requests are reviewed, recorded and
closed without merging, so the issue stays open for other learners.

