# Architecture

```
shopcore/
  money/      Money (exact Decimal, per-currency minor units), rounding modes,
              allocation, formatting, FX rate tables
  catalog/    Product records (seed: data/products.csv), SKU grammar, EAN-13,
              colour/size variants
  inventory/  Stock per (warehouse, SKU), reservations with expiry, reorder
              points, inter-warehouse transfers
  pricing/    Percent/amount discounts, coupons, quantity tiers, bundles,
              margin and MRP rules
  tax/        Regional rules (seed: data/tax_rules.json), inclusive vs
              exclusive prices, GST split (CGST+SGST vs IGST), GSTIN checksum
  cart/       Cart lines and limits, totals, merge on login, repricing
  orders/     Order model, state machine, payment, cancellation, returns,
              refunds, order queries
  shipping/   Parcel weight/volume, PIN-code zones, rate cards (seed:
              data/shipping_rates.json), delivery estimates, S10 tracking ids
  ledger/     Chart of accounts, balanced journal entries, balances, trial
              balance, income statement, bank reconciliation
  reports/    Daily/weekly sales, top products, tax by region, CSV export
```

Conventions shared by every module:

* **Money is never a float.** Amounts are `Money(Decimal, currency)`; mixing
  currencies raises `MoneyError`. Rounding is explicit (`RoundingMode`), half-up
  unless documented otherwise.
* **Time is an argument.** No function reads the clock. Datetimes are
  timezone-aware; store-local dates (order numbers, reports, return windows,
  dispatch cut-off) use IST (`Asia/Kolkata`).
* **Errors are domain errors.** Each module raises its own subclass of
  `shopcore.errors.ShopCoreError`.
* **Seed data is bundled** in `shopcore/data/` and loaded with `importlib.resources`.

Dependencies flow one way: `money` <- `catalog` <- `tax`/`pricing`/`inventory`
<- `cart`/`orders` <- `shipping`/`ledger`/`reports`.

Tests mirror the source tree (`shopcore/tax/rules.py` -> `tests/tax/test_rules.py`)
and are named `test_<function>_<case>`, so a failing test points to exactly one
function. `tools/index_functions.py` writes `.virtint/functions.json`, the map from
each public function to its source span and tests.
