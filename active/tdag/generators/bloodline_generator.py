#!/usr/bin/env python3
"""
Bloodline Generator for Demon Beasts (TDAG Simulation)

Location: <root_directory>/generators/bloodline_generator.py

This script loads:
- validators/valid_demon_beast_types.json
- validators/valid_bloodline_tiers.json
- reference/soul/bloodline_modifier_by_tier.json

And produces a full bloodline object:
- origin_beast_type
- tier
- name
- modifier_value
- description

Usage:
    python bloodline_generator.py [-o json|pretty]
"""
import json
import os
import argparse
from meta.utils import load_json, get_common_paths, validate_value
from helpers.weight_utils import weighted_choice
from helpers.generation_context import GenerationContext, parse_overrides

def generate_bloodline(origin_beast_type=None, 
                       force_bloodline_tier:str=None, # optional override for specific calls
                       ctx: GenerationContext = GenerationContext(),
                       ) -> dict:
    paths = get_common_paths()
    root_dir = paths['root']
    reference_dir = paths['reference']

    # Load valid bloodline tiers
    bloodline_modifier_map = load_json(os.path.join(reference_dir, 'soul', 'bloodline_modifier_by_tier.json'))

    tier = force_bloodline_tier or weighted_choice(list(bloodline_modifier_map.keys()), 
                            weights_path=os.path.join(root_dir, 'reference', 'roll_weights', 'bloodline_tiers.json'), 
                            override_weights=ctx.override_bloodline_weights,
                            exclusive=True)
    validate_value(tier, bloodline_modifier_map.keys())

    # Random selections
    if not origin_beast_type:
        # Load valid demon beast types
        demon_beast_types_list = load_json(os.path.join(reference_dir, 'demon_beast', 'demon_beast_types.json'))
        origin_beast_type = weighted_choice(
            list(demon_beast_types_list),
            weights_path=os.path.join(reference_dir, 'roll_weights', 'demon_beast_types.json'),
            override_weights=ctx.override_demon_beast_weights,
            exclusive=True
        )
    validate_value(origin_beast_type, demon_beast_types_list)

    # Construct bloodline fields
    name = f"{tier} {origin_beast_type} Bloodline" if tier else f"{origin_beast_type} Bloodline"
    modifier_value = bloodline_modifier_map.get(tier)
    tier_name = tier if tier!= 'None' else 'Worthless'
    description = f"A(n) {tier_name.lower()} bloodline derived from {origin_beast_type}."

    return {
        "origin_beast_type": origin_beast_type,
        "tier": tier,
        "name": name,
        "modifier_value": modifier_value,
        "description": description
    }

def main():
    parser = argparse.ArgumentParser(description="Generate a random bloodline for a demon beast.")
    parser.add_argument(
        '-obt', '--origin_beast_type',
        help="Demon Beast Type (e.g., 'wolf', 'tiger')",
        required=False,
        default=None
    )
    parser.add_argument('-blt','--force_bloodline_tier',
                        required=False,
                        default=None,
                        help="Force a specific bloodline tier (e.g., 'poor', 'good', 'god').")
    parser.add_argument(
        '--override', '-O',
        action='append',
        metavar='CAT:KEY=WEIGHT',
        help="e.g. db:wolf=80 or el:ice=30"
    )
    parser.add_argument(
        '-o', '--output',
        choices=['json', 'pretty'],
        default='pretty',
        help="Output format: 'json' for raw JSON, 'pretty' for formatted display."
    )
    args = parser.parse_args()
    overrides = parse_overrides(args.override)  # where --override flags are collected
    ctx = GenerationContext(**overrides)

    bloodline = generate_bloodline(
        origin_beast_type=args.origin_beast_type,
        force_bloodline_tier=args.force_bloodline_tier,
        ctx=ctx
    )
    if args.output == 'json':
        print(json.dumps(bloodline))
    else:
        print(json.dumps(bloodline, indent=2))

if __name__ == '__main__':
    main()
