#!/usr/bin/env python3
"""
Soul Color System for TDAG Simulation

Location: <root_directory>/generators/soul_color_generator.py

Provides:
- generate_soul_color(): picks a soul color based on rarity-weighted logic
- apply_soul_color_modifier(base_speed, technique_quality, soul_color): adjusts a base cultivation
  speed according to soul color rarity and technique quality rules.

Loading:
- validators/valid_soul_colors.json
- reference/soul/soul_color.json
- validators/valid_cultivation_technique_qualities.json
- reference/cultivation_technique/base_cultivation_speeds.json
"""
import os
import json
import random
import argparse
from helpers.generation_context import GenerationContext, parse_overrides
from helpers.weight_utils import weighted_choice
from meta.utils import load_json, get_common_paths


def generate_soul_color(ctx:GenerationContext=GenerationContext()) -> dict:
    """
    Randomly select a soul color and its rarity.
    Returns a dict with 'color' and 'rarity'.
    """
    # Paths
    paths = get_common_paths()
    reference_dir = paths['reference']
    # Load soul color quality options
    color_quality_map = load_json(os.path.join(reference_dir, 'roll_weights', 'soul_color_qualities.json'))

    # Load rarity groups
    color_map = load_json(os.path.join(reference_dir, 'soul', 'soul_color.json'))
    # Pick rarity
    rarity = weighted_choice(
        list(color_quality_map.keys()),
        weights_path=os.path.join(reference_dir, 'roll_weights', 'soul_color_qualities.json'),
        override_weights=ctx.override_soul_color_weights,
        exclusive=True)
    print(rarity)
    # Pick color within rarity tier
    colors = color_map.get(rarity, [])
    if not colors:
        raise RuntimeError(f"No colors defined for rarity '{rarity}'")
    color = random.choice(colors)
    return {'color': color, 'rarity': rarity}

def main():
    parser = argparse.ArgumentParser(description="Generate soul color and test its modifier on a technique speed.")
    parser.add_argument('--test-speed', type=float, default=1.0,
                        help="Base cultivation speed to test.")
    parser.add_argument('-q', '--quality', default='poor',
                        help="Technique quality (poor..god)")
    parser.add_argument('-c', '--color', default=None,
                        help="Optional soul color ID to use instead of random.")
    parser.add_argument(
    '--override', '-O',
    action='append',
    metavar='CAT:KEY=WEIGHT',
    help="e.g. db:wolf=80 or el:ice=30"
    )
    parser.add_argument('-o', '--output', choices=['json','pretty'], default='pretty')
    args = parser.parse_args()
    args = parser.parse_args()
    overrides = parse_overrides(args.override)  # where --override flags are collected
    ctx = GenerationContext(**overrides)

    sc = args.color or generate_soul_color(ctx)
    test_speed = args.test_speed
    result = {
        'soul_color': sc,
    }
    if args.output == 'json':
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
