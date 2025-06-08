#!/usr/bin/env python3
"""
Soul Rank Generator for TDAG Simulation

Location: <root_directory>/generators/soul_rank_generator.py

Provides functionality to randomly select a soul rank (major and minor)
within a specified realm and calculate the corresponding soul force.
This logic is factored out as a standalone generator for reuse.

Functions:
- generate_soul_rank(realm: str = 'earthen',
                     major_weights: list = None,
                     minor_weights: list = None) -> dict
    Returns {'major': ..., 'minor': ..., 'soul_force': ...}

Usage (CLI):
    python soul_rank_generator.py [--realm REALM]
                                 [--major-weights w1 w2 ...]
                                 [--minor-weights w1 w2 ...]
                                 [-o json|pretty]
"""
import os
import json
import random
import argparse
from soul_force_generator import generate_soul_force


def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def weighted_choice(seq: list, weights: list = None):
    """Choose one item from seq with optional weights (even by default)."""
    if weights is None:
        weights = [1] * len(seq)
    return random.choices(seq, weights=weights, k=1)[0]


def generate_soul_rank(realm: str = 'earthen',
                       major_weights: list = None,
                       minor_weights: list = None) -> dict:
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
    realm_data = rank_data.get(realm, {})

    major_ranks = realm_data.get('major_ranks', [])
    minor_ranks = realm_data.get('minor_ranks', [])

    # Select ranks with optional weights
    major = weighted_choice(major_ranks, major_weights)
    minor = weighted_choice(minor_ranks, minor_weights)

    # Compute soul force
    soul_force = generate_soul_force(major_rank=major,
                                     minor_rank=minor,
                                     realm=realm)

    return {
        'major': major,
        'minor': minor,
        'soul_force': soul_force
    }


def main():
    parser = argparse.ArgumentParser(description="Generate soul rank and force for TDAG.")
    parser.add_argument('-r', '--realm', choices=['earthen','heavenly'], default='earthen',
                        help="Realm for soul rank (earthen or heavenly)")
    parser.add_argument('--major-weights', nargs='+', type=float,
                        help="Optional weights for each major rank in order")
    parser.add_argument('--minor-weights', nargs='+', type=float,
                        help="Optional weights for each minor rank in order")
    parser.add_argument('-o', '--output', choices=['json','pretty'], default='pretty',
                        help="Output format: 'json' or 'pretty'.")
    args = parser.parse_args()

    result = generate_soul_rank(realm=args.realm,
                                major_weights=args.major_weights,
                                minor_weights=args.minor_weights)
    if args.output == 'json':
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
