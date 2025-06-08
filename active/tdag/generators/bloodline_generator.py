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
import random
import argparse

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_bloodline(origin_beast_type=None, bloodline_tiers=None):
    # Resolve directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    validators_dir = os.path.join(root_dir, 'validators')
    reference_soul_dir = os.path.join(root_dir, 'reference', 'soul')

    # Load valid bloodline tiers
    tiers_data = load_json(os.path.join(validators_dir, 'valid_bloodline_tiers.json'))
    bloodline_tiers = tiers_data.get('values', tiers_data)

    # Load modifier mapping by tier
    modifier_map = load_json(os.path.join(reference_soul_dir, 'bloodline_modifier_by_tier.json'))

    # Random selections
    if not origin_beast_type:
        # Load valid demon beast types
        beast_types_data = load_json(os.path.join(validators_dir, 'valid_demon_beast_types.json'))
        demon_beast_types = beast_types_data.get('values', beast_types_data)
        origin_beast_type = random.choice(demon_beast_types)
    tier = random.choice(bloodline_tiers)

    # Construct bloodline fields
    name = f"{tier} {origin_beast_type} Bloodline" if tier else f"{origin_beast_type} Bloodline"
    modifier_value = modifier_map.get(tier)
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
        '-o', '--output',
        choices=['json', 'pretty'],
        default='pretty',
        help="Output format: 'json' for raw JSON, 'pretty' for formatted display."
    )
    args = parser.parse_args()

    bloodline = generate_bloodline()
    if args.output == 'json':
        print(json.dumps(bloodline))
    else:
        print(json.dumps(bloodline, indent=2))

if __name__ == '__main__':
    main()
