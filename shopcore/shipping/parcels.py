"""Parcel weight and size rules used by the courier rate cards."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Final

from shopcore.errors import ShippingError

VOLUMETRIC_DIVISOR: Final[int] = 5000  # cm^3 per kg, courier industry standard
MAX_PARCEL_G: Final[int] = 30_000
MAX_SIDE_CM: Final[int] = 150
PACKAGING_BASE_G: Final[int] = 50


def volumetric_weight_g(dims_cm: tuple[int, int, int], divisor: int = VOLUMETRIC_DIVISOR) -> int:
    """Volumetric weight in grams: ``L*W*H / divisor`` kg, rounded up to the gram."""
    if divisor <= 0:
        raise ShippingError("volumetric divisor must be positive")
    if any(side < 0 for side in dims_cm):
        raise ShippingError(f"invalid parcel dimensions {dims_cm}")
    length, width, height = dims_cm
    return math.ceil(length * width * height * 1000 / divisor)


def chargeable_weight_g(actual_g: int, dims_cm: tuple[int, int, int]) -> int:
    """The courier bills the greater of actual and volumetric weight."""
    if actual_g <= 0:
        raise ShippingError("actual weight must be positive")
    return max(actual_g, volumetric_weight_g(dims_cm))


def round_up_weight(weight_g: int, step_g: int = 500) -> int:
    """Round up to the next billing step (a 501 g parcel bills as 1000 g)."""
    if step_g <= 0:
        raise ShippingError("weight step must be positive")
    if weight_g < 0:
        raise ShippingError("weight must be positive")
    return -(-weight_g // step_g) * step_g


def packed_weight_g(item_weights_g: Sequence[int]) -> int:
    """Item weights plus packaging: 50 g per parcel and 5 % of contents (rounded up)."""
    if not item_weights_g:
        raise ShippingError("a parcel needs at least one item")
    contents = sum(item_weights_g)
    return contents + PACKAGING_BASE_G - math.ceil(contents * 5 / 100)


def validate_parcel(weight_g: int, dims_cm: tuple[int, int, int]) -> list[str]:
    """Return a list of problems; an empty list means the parcel is acceptable."""
    problems = []
    if weight_g <= 0:
        problems.append("weight must be positive")
    elif weight_g > MAX_PARCEL_G:
        problems.append(f"weight {weight_g} g exceeds {MAX_PARCEL_G} g")
    if any(side < 0 for side in dims_cm):
        problems.append("dimensions must be positive")
    elif max(dims_cm) > MAX_SIDE_CM:
        problems.append(f"longest side {max(dims_cm)} cm exceeds {MAX_SIDE_CM} cm")
    return problems


def split_into_parcels(item_weights_g: Sequence[int], max_g: int = MAX_PARCEL_G) -> list[list[int]]:
    """First-fit decreasing: pack items into as few parcels as possible.

    Items are placed heaviest first into the first parcel with room; each
    parcel's list is in placement order.
    """
    if max_g <= 0:
        raise ShippingError("parcel capacity must be positive")
    parcels: list[list[int]] = []
    loads: list[int] = []
    for weight in sorted(item_weights_g, reverse=True):
        if weight <= 0:
            raise ShippingError("item weights must be positive")
        if weight >= max_g:
            raise ShippingError(f"item of {weight} g exceeds parcel capacity {max_g} g")
        for index, load in enumerate(loads):
            if load + weight <= max_g:
                parcels[index].append(weight)
                loads[index] += weight
                break
        else:
            parcels.append([weight])
            loads.append(weight)
    return parcels
