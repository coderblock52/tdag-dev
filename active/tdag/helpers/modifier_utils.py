#!/usr/bin/env python3
"""
Modifier Utilities for TDAG Simulation

Location: <root_directory>/helpers/modifier_utils.py

Provides functions to consistently combine multiple modifiers
in both additive and multiplicative fashions.

Functions:
- combine_modifiers(base_value: float, *modifiers: float) -> float
    Apply each modifier multiplicatively: result = base * ∏(1 + m)

- apply_modifiers(base_value: float,
                  multiplicative: list[float] = None,
                  additive: list[float] = None) -> float
    First applies all multiplicative modifiers, then adds all additive modifiers.

Usage:
    from helpers.modifier_utils import combine_modifiers, apply_modifiers

    # Multiplicative stacking:
    power = combine_modifiers(100.0, 0.1, 0.2)  # 100 * 1.1 * 1.2

    # Mixed stacking:
    result = apply_modifiers(
        base_value=200.0,
        multiplicative=[0.1, 0.05],  # two +10% and +5% buffs
        additive=[20.0]               # flat +20 bonus
    )  # ((200*1.1*1.05) + 20)
"""
from typing import List, Optional


def combine_modifiers(base_value: float, *modifiers: float) -> float:
    """
    Apply a series of multiplicative modifiers to a base value.
    Each modifier m is applied as result *= (1 + m).

    Args:
        base_value: The starting numeric value.
        modifiers: A variable-length list of modifier floats (e.g. 0.1 for +10%).

    Returns:
        The modified value after all multipliers applied.
    """
    result = base_value
    for m in modifiers:
        result *= (1 + m)
    return result


def apply_modifiers(
    base_value: float,
    multiplicative: Optional[List[float]] = None,
    additive: Optional[List[float]] = None
) -> float:
    """
    Apply multiplicative and additive modifiers to a base value.

    Multiplicative modifiers are applied first (as percentages), then additive modifiers are summed.

    Args:
        base_value: The starting numeric value.
        multiplicative: List of floats to apply multiplicatively (e.g. 0.1 for +10%).
        additive:       List of floats to apply additively (flat bonuses).

    Returns:
        The resulting value after all modifiers.
    """
    result = base_value
    if multiplicative:
        for m in multiplicative:
            result *= (1 + m)
    if additive:
        for a in additive:
            result += a
    return result
