# ShopCore (Python) - grading interface (used by .github/workflows/virtint-review.yml).
#
#   make build                       byte-compile + import check
#   make test                        full suite  -> reports/junit/pytest.xml
#   make test TESTS="<id>;<id>"      only these pytest node ids
#   make lint                        ruff        -> reports/lint.json
#   make coverage                    full suite  -> reports/coverage.xml (Cobertura)
#
# pytest's own exit code (0 pass, 1 failures, >=2 infra) is also written to
# reports/exit-code, because GNU make itself always exits 2 when a recipe fails.

PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
REPORTS := reports
export PYTHONPATH := $(CURDIR)
# Never trust timestamp-validated .pyc files: an edit that keeps size and mtime-second
# (e.g. == -> !=) would otherwise run stale bytecode.
export PYTHONDONTWRITEBYTECODE := 1
JUNIT := $(REPORTS)/junit/pytest.xml
TESTS ?=
TEST_IDS := $(foreach t,$(subst ;, ,$(TESTS)),'$(t)')
PYTEST := $(PYTHON) -m pytest -q -p no:cacheprovider --junitxml=$(JUNIT) -o junit_family=xunit2

.PHONY: build test lint coverage typecheck functions check-functions clean

build:
	$(PYTHON) -m compileall -q --invalidation-mode checked-hash shopcore
	$(PYTHON) tools/import_check.py

test:
	@mkdir -p $(REPORTS)/junit && rm -f $(REPORTS)/junit/*.xml $(REPORTS)/exit-code
	@$(PYTEST) $(TEST_IDS); code=$$?; echo $$code > $(REPORTS)/exit-code; exit $$code

lint:
	$(PYTHON) tools/lint_report.py $(REPORTS)/lint.json shopcore

coverage:
	@mkdir -p $(REPORTS)/junit && rm -f $(REPORTS)/junit/*.xml $(REPORTS)/exit-code $(REPORTS)/coverage.xml
	@$(PYTEST) --cov=shopcore --cov-report=term --cov-report=xml:$(REPORTS)/coverage.xml; \
		code=$$?; echo $$code > $(REPORTS)/exit-code; exit $$code

typecheck:
	$(PYTHON) -m mypy

functions:
	$(PYTHON) tools/index_functions.py

check-functions:
	$(PYTHON) tools/index_functions.py --check

clean:
	rm -rf $(REPORTS) .mypy_cache .ruff_cache .pytest_cache
	find . -name __pycache__ -type d -not -path './.venv/*' -prune -exec rm -rf {} +
