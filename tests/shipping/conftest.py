import pytest

from shopcore.shipping.rates import Rate, load_seed_rate_card


@pytest.fixture
def card() -> dict[tuple[str, str], Rate]:
    return load_seed_rate_card()
