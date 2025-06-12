#!/usr/bin/env python3
"""
Weighted Choice Utility for TDAG Simulation

Location: <root_directory>/helpers/weight_utils.py

Provides a flexible weighted_choice function that can:

Load base_weights from a JSON file path or accept a mapping directly

Accept override_weights to adjust specific keys or to restrict choices exclusively

Validate that overrides only apply to known items

Usage:
from helpers.weight_utils import weighted_choice

# Basic usage with mapping:
pick = weighted_choice(
    items=['a','b','c'],
    base_weights={'a':10,'b':20,'c':5},
    override_weights={'b':50},
    exclusive=False
)

# Usage with weights_path:
pick = weighted_choice(
    items=['x','y','z'],
    weights_path='reference/weights/file.json',
    override_weights={'y':30},
    exclusive=True
)

"""
import os
import json
import random
from typing import Mapping, Sequence, Optional, TypeVar
import bisect
import itertools

T = TypeVar('T')

def weighted_choice(
items: Sequence[T],
base_weights: Optional[Mapping[T, float]] = None,
weights_path: Optional[str] = None,
override_weights: Optional[Mapping[T, float]] = None,
exclusive: bool = False
) -> T:
    """
        Select one item from items according to weights.
        You must supply either `base_weights` mapping or `weights_path` to a JSON file
        containing a mapping of item -> weight.

        Args:
            items: sequence of items to choose from.
            base_weights: mapping of item to its base weight.
            weights_path: path to JSON file with base weight mapping.
            override_weights: mapping of item to override weight; keys must exist in base_weights.
            exclusive: if True, only items in override_weights are considered.

        Returns:
            A single item selected according to combined weights.

        Raises:
            ValueError: if neither base_weights nor weights_path provided,
                        or if override keys are not in base_weights,
                        or if no items remain when exclusive=True.
    """
    # Load base_weights from JSON file if path provided
    if base_weights is None:
        if not weights_path:
            raise ValueError("Must provide either base_weights or weights_path.")
        base_path = weights_path
        if not os.path.isabs(base_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(script_dir, '..'))
            base_path = os.path.join(project_root, base_path)
        with open(base_path, 'r', encoding='utf-8') as f:
            base_weights = json.load(f)

    # Validate override keys
    if override_weights:
        for key in override_weights:
            if key not in base_weights:
                raise ValueError(f"Override key '{key}' not found in base_weights.")

    # Determine final candidate list
    candidates = list(items)
    if exclusive and override_weights:
        candidates = [item for item in items if item in override_weights]
        if not candidates:
            raise ValueError("No candidates available after applying exclusive overrides.")

    # Build weights list
    weights = []
    for item in candidates:
        # Start with base or zero if missing
        w = base_weights.get(str(item), 0)
        # Apply override if exists
        if override_weights and item in override_weights:
            w = override_weights[item]
        weights.append(w)

    # Perform weighted random choice
    return random.choices(candidates, weights=weights, k=1)[0]

def weighted_randint(x_min, x_max, w_min=0.005, w_max=10.0):
    """
    Return a random integer between x_min and x_max inclusive,
    with weight w(x) = w_max - (w_max - w_min)*(x - x_min)/(x_max - x_min).
    """
    # 1) Build the discrete values and their weights
    values = list(range(x_min, x_max + 1))
    span   = x_max - x_min
    # linear weight for each integer
    weights = [
        w_max - (w_max - w_min) * (x - x_min) / span
        for x in values
    ]

    # 2) Build cumulative distribution
    cum_weights = list(itertools.accumulate(weights))
    total       = cum_weights[-1]

    # 3) Sample a uniform random number in [0, total)
    r = random.random() * total

    # 4) Find the bucket via binary search
    idx = bisect.bisect_right(cum_weights, r)
    return values[idx]