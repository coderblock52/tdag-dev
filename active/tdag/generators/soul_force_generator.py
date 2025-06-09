#!/usr/bin/env python3
"""
Soul Force Generator for TDAG Simulation

This script resides in `<root_directory>/generators/soul_force_generator.py`.
It loads:
- `reference/soul/soul_force_ranges.json` for base thresholds
- `validators/valid_soul_rank_structure.json` for valid ranks

Provides:
- generate_soul_force(major_rank, minor_rank, realm='earthen')
  Returns a random integer soul force within the range determined by the given ranks.

Usage:
    python soul_force_generator.py --major Bronze --minor 3 [--realm earthen] [-o json|pretty]
"""
import os
import json
import random
import argparse
import bisect
import itertools
# do not need generation context here


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

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

def generate_soul_force(major_rank:str, minor_rank:int, realm:str='earthen'):
    # Resolve directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))

    # Load range definitions
    ranges_path = os.path.join(root_dir, 'reference', 'soul', 'soul_force_ranges.json')
    ranges_data = load_json(ranges_path)
    base_unit = ranges_data.get('base_unit', 100)
    realm_map = ranges_data.get(realm)
    if realm_map is None:
        raise ValueError(f"Unknown realm: {realm}")

    multiplier = realm_map.get(major_rank)
    if multiplier is None:
        raise ValueError(f"Unknown major rank '{major_rank}' in realm '{realm}'")
    base_value = base_unit * multiplier

    # Validate minor_rank
    validator_path = os.path.join(root_dir, 'validators', 'valid_soul_rank_structure.json')
    validator = load_json(validator_path)
    minors = validator['values'].get(realm, {}).get('minor_ranks', [])
    if minor_rank not in minors:
        raise ValueError(f"Invalid minor rank {minor_rank} for realm '{realm}'")

    # Determine range
    min_val = minor_rank * base_value if minor_rank > 1 else 1
    if minor_rank == minors[-1]:  # If it's the last minor rank
        # If it's the last minor rank, use the next major rank's base value
        max_val = base_value * 10
    else:
        max_val = (minor_rank + 1) * base_value

    # adjust weight of distrubution to favor lower values
    return weighted_randint(min_val, max_val, w_min=0.25, w_max=1.0)

def main():
    parser = argparse.ArgumentParser(description="Generate a soul force value based on rank.")
    parser.add_argument('--major', required=False, help="Major rank (e.g., Bronze, Silver)")
    parser.add_argument('--minor', type=int, required=False, help="Minor rank number")
    parser.add_argument('--realm', choices=['earthen', 'heavenly'], default='earthen', help="Rank realm")
    parser.add_argument('-o', '--output', choices=['json', 'pretty'], default='pretty', help="Output format")
    args = parser.parse_args()

    value = generate_soul_force(args.major, args.minor, args.realm)
    if args.output == 'json':
        print(json.dumps({"soul_force": value}))
    else:
        print(value)

if __name__ == '__main__':
    main()
