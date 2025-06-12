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

from meta.utils import load_json, get_common_paths, validate_value
from helpers.weight_utils import weighted_randint
from helpers.generation_context import GenerationContext, parse_overrides


def generate_soul_force(major_rank:str, minor_rank:int, realm:str='earthen', ctx:GenerationContext=GenerationContext()) -> int:
    # Resolve directories
    paths = get_common_paths()
    reference_dir = paths['reference']
    validators_dir = paths['validators']

    # Load range definitions
    ranks_path = os.path.join(reference_dir, 'soul', 'soul_force_ranks.json')
    ranks_data = load_json(ranks_path)
    base_unit = ranks_data.get('base_unit', 100)
    realm_map = ranks_data.get(realm)
    if realm_map is None:
        raise ValueError(f"Unknown realm: {realm}")

    multiplier = realm_map.get(major_rank)
    if multiplier is None:
        raise ValueError(f"Unknown major rank '{major_rank}' in realm '{realm}'")
    base_value = base_unit * multiplier

    # Validate minor_rank
    rank_validator_path = os.path.join(validators_dir, 'valid_soul_rank_structure.json')
    rank_validator = load_json(rank_validator_path)
    minor_ranks = rank_validator['values'].get(realm, {}).get('minor_ranks', [])
    validate_value(minor_rank, minor_ranks)


    # Determine range
    min_val = minor_rank * base_value if minor_rank > 1 else 1
    if minor_rank == minor_ranks[-1]:  # If it's the last minor rank
        # If it's the last minor rank, use the next major rank's base value
        max_val = base_value * 10
    else:
        max_val = (minor_rank + 1) * base_value

    # adjust weight of distrubution to favor lower values
    return weighted_randint(min_val, max_val, ctx.override_randint_weights['w_min'], ctx.override_randint_weights['w_max'])

def main():
    parser = argparse.ArgumentParser(description="Generate a soul force value based on rank.")
    parser.add_argument('--major', required=False, help="Major rank (e.g., Bronze, Silver)")
    parser.add_argument('--minor', type=int, required=False, help="Minor rank number")
    parser.add_argument('--realm', choices=['earthen', 'heavenly'], default='earthen', help="Rank realm")
    parser.add_argument(
    '--override', '-O',
    action='append',
    metavar='CAT:KEY=WEIGHT',
    help="e.g. db:wolf=80 or el:ice=30"
    )
    parser.add_argument('-o', '--output', choices=['json', 'pretty'], default='pretty', help="Output format")
    args = parser.parse_args()
    overrides = parse_overrides(args.override)  # where --override flags are collected
    ctx = GenerationContext(**overrides)

    value = generate_soul_force(args.major, args.minor, args.realm, ctx)
    if args.output == 'json':
        print(json.dumps({"soul_force": value}))
    else:
        print(value)

if __name__ == '__main__':
    main()
