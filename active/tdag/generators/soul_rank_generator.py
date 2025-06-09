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
from .soul_force_generator import generate_soul_force
from helpers.generation_context import GenerationContext, parse_overrides
from helpers.weight_utils import weighted_choice


def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    validators_dir = os.path.join(root_dir, 'validators')

    # Load soul rank structure
    val_path = os.path.join(validators_dir, 'valid_soul_rank_structure.json')
    rank_data = load_json(val_path).get('values', {})
    realm_data = rank_data.get(ctx.realm, {})

    if ctx.realm == 'earthen':
        major_rank_weight_path = os.path.join(root_dir, 'reference', 'roll_weights', 'ranks', 'soul_major_ranks_earthen.json')
        minor_rank_weight_path = os.path.join(root_dir, 'reference', 'roll_weights', 'ranks', 'soul_minor_ranks_earthen.json')
    elif ctx.realm == 'heavenly':
        major_rank_weight_path = os.path.join(root_dir, 'reference', 'roll_weights', 'ranks', 'soul_major_ranks_heavenly.json')
        minor_rank_weight_path = os.path.join(root_dir, 'reference', 'roll_weights', 'ranks', 'soul_minor_ranks_heavenly.json')
    major_ranks = realm_data.get('major_ranks', [])
    minor_ranks = realm_data.get('minor_ranks', [])

    # Select ranks with optional weights
    major = weighted_choice(major_ranks,
                            weights_path=major_rank_weight_path,
                            override_weights=ctx.override_soul_rank_major_weights,
                            exclusive=True
                           )
    minor = weighted_choice(minor_ranks,
                            weights_path=minor_rank_weight_path,
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
