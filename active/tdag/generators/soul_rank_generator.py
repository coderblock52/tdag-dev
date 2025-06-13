#!/usr/bin/env python3
"""
Soul Rank Generator for TDAG Simulation

Location: <root_directory>/generators/soul_rank_generator.py

Provides functionality to randomly select a soul rank (major and minor)
within a specified realm and calculate the corresponding soul force.
This logic is factored out as a standalone generator for reuse.

"""
import os
import json
import random
import argparse
from soul_force_generator import generate_soul_force
from helpers.generation_context import GenerationContext, parse_overrides
from helpers.weight_utils import weighted_choice
from meta.utils import load_json, get_common_paths, validate_value
# need to refactor downstream soul force generators and soul rank generators to be able to be 'none' and have a soul force of 0.0

def generate_soul_rank(ctx:GenerationContext=GenerationContext()) -> dict:
    """
    Randomly select a major and minor soul rank in the given realm,
    then compute soul force via soul_force_generator.

    Args:
        realm: 'earthen' or 'heavenly'
        major_weights: optional list of weights for major ranks
        minor_weights: optional list of weights for minor ranks

    Returns:
        dict with keys 'major', 'minor', 'soul_force'
    """
    # Resolve project directories
    paths = get_common_paths()
    reference_dir = paths['reference']

    # Load soul rank list for given realm
    major_rank_list = load_json(os.path.join(reference_dir, 'soul', 'soul_force_ranks.json')).get(ctx.realm, {}).keys()
    minor_rank_list = load_json(os.path.join(reference_dir, 'soul', 'soul_force_minor_ranks.json')).get(ctx.realm, {})

    # Select ranks with optional weights
    major = weighted_choice(major_rank_list,
                            weights_path=os.path.join(reference_dir, 'roll_weights', 'ranks', f'soul_major_ranks_{ctx.realm}.json'),
                            override_weights=ctx.override_soul_rank_major_weights,
                            exclusive=True
                           )
    minor = weighted_choice(minor_rank_list,
                            weights_path=os.path.join(reference_dir, 'roll_weights', 'ranks', f'soul_minor_ranks_{ctx.realm}.json'),
                            override_weights=ctx.override_soul_rank_minor_weights,
                            exclusive=True
                           )

    # Compute soul force
    soul_force = generate_soul_force(major_rank=major,
                                     minor_rank=minor,
                                     realm=ctx.realm)

    return {
        'major': major,
        'minor': minor,
        'soul_force': soul_force
    }


def main():
    parser = argparse.ArgumentParser(description="Generate soul rank and force for TDAG.")
    parser.add_argument(
    '--override', '-O',
    action='append',
    metavar='CAT:KEY=WEIGHT',
    help="e.g. db:wolf=80 or el:ice=30"
    )
    parser.add_argument('-o', '--output', choices=['json','pretty'], default='pretty',
                        help="Output format: 'json' or 'pretty'.")
    args = parser.parse_args()
    overrides = parse_overrides(args.override)  # where --override flags are collected
    ctx = GenerationContext(**overrides)

    result = generate_soul_rank(ctx=ctx)
    if args.output == 'json':
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
