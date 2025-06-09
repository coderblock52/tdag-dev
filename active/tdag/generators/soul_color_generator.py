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
# need to use generation context


def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_soul_color() -> dict:
    """
    Randomly select a soul color and its rarity.
    Returns a dict with 'color' and 'rarity'.
    """
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    validators_dir = os.path.join(root_dir, 'validators')
    ref_soul_dir = os.path.join(root_dir, 'reference', 'soul')

    # Load valid colors (to validate file) - not strictly needed for gen
    valid = load_json(os.path.join(validators_dir, 'valid_soul_colors.json'))['values']

    # Load rarity groups
    color_map = load_json(os.path.join(ref_soul_dir, 'soul_color.json'))
    rarities = list(color_map.keys())  # ['common','uncommon','rare']
    # Weights matching idea: common=70, uncommon=25, rare=5
    weights = [70, 25, 5]
    # Pick rarity
    rarity = random.choices(rarities, weights=weights, k=1)[0]
    # Pick color within rarity tier
    colors = color_map.get(rarity, [])
    if not colors:
        raise RuntimeError(f"No colors defined for rarity '{rarity}'")
    color = random.choice(colors)
    if color not in valid:
        raise RuntimeError(f"Generated invalid soul color: {color}")
    return {'color': color, 'rarity': rarity}


def apply_soul_color_modifier(base_speed: float, technique_quality: str, soul_color: str) -> float:
    """
    Adjust base_speed based on the soul_color interaction with technique_quality:
    - common: no bonus
    - uncommon: poor/good → treat quality one tier higher (cap at 'great')
    - rare: as uncommon; additionally, if technique is 'great', apply +0.5 multiplier bonus

    Returns the modified cultivation speed.
    """
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    validators_dir = os.path.join(root_dir, 'validators')
    ref_ct_dir = os.path.join(root_dir, 'reference', 'cultivation_technique')
    ref_soul_dir = os.path.join(root_dir, 'reference', 'soul')

    # Load quality tiers and base speeds
    qualities = load_json(os.path.join(validators_dir, 'valid_cultivation_technique_qualities.json'))['values']
    speeds = load_json(os.path.join(ref_ct_dir, 'base_cultivation_speeds.json'))

    # Load color rarity map
    color_map = load_json(os.path.join(ref_soul_dir, 'soul_color.json'))
    # Determine rarity for the given color
    rarity = None
    for r, cols in color_map.items():
        if soul_color == cols[0] or soul_color in cols:
            rarity = r
            break
    if rarity is None:
        raise ValueError(f"Unknown soul color: {soul_color}")

    # Helper to bump quality one tier (used by uncommon and rare)
    def bump(q: str) -> str:
        idx = qualities.index(q)
        # cap bump at 'great'
        cap = qualities.index('great')
        return qualities[min(idx + 1, cap)]

    # Apply logic
    if rarity == 'common':
        return base_speed
    if rarity == 'uncommon':
        if technique_quality in ['poor', 'good']:
            new_q = bump(technique_quality)
            return speeds[new_q]
        return base_speed
    if rarity == 'rare':
        if technique_quality in ['poor', 'good']:
            new_q = bump(technique_quality)
            return speeds[new_q]
        if technique_quality == 'great':
            # +0.5 bonus to multiplier: e.g. 1.0 → 1.5
            return base_speed * 1.5
        return base_speed
    return base_speed


def main():
    parser = argparse.ArgumentParser(description="Generate soul color and test its modifier on a technique speed.")
    parser.add_argument('--test-speed', type=float, default=1.0,
                        help="Base cultivation speed to test.")
    parser.add_argument('-q', '--quality', default='poor',
                        help="Technique quality (poor..god)")
    parser.add_argument('-c', '--color', default=None,
                        help="Optional soul color ID to use instead of random.")
    parser.add_argument('-o', '--output', choices=['json','pretty'], default='pretty')
    args = parser.parse_args()

    sc = args.color or generate_soul_color()['color']
    test_speed = args.test_speed
    mod_speed = apply_soul_color_modifier(test_speed, args.quality, sc)
    result = {
        'soul_color': sc,
        'quality': args.quality,
        'base_speed': test_speed,
        'modified_speed': mod_speed
    }
    if args.output == 'json':
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
