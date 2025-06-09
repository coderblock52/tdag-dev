#!/usr/bin/env python3
"""
Demon Beast Object Generator for TDAG Simulation

This script resides in <root_directory>/generators/demon_beast_generator.py and
produces a complete demon beast object conforming to your schema.

It dynamically loads:

validators/valid_demon_beast_types.json for beast types

validators/valid_soul_rank_structure.json for soul ranks

validators/valid_bloodline_tiers.json for bloodline tiers (fallback)

reference/demon_beast_element_names.json for element name mapping

reference/soul/bloodline_modifier_by_tier.json for bloodline modifiers

<script_dir>/bloodline_generator.py for full bloodline object generation

Generated fields:

name: flavor name combining element variant and beast type

soul_rank: {major, minor}

demon_beast_type

stats.soul_force

soul.element

soul.bloodline: bloodline name

bloodline_object: full bloodline object with metadata

Usage:
python demon_beast_generator.py [-o json|pretty]
"""
import os
import json
import random
import argparse
import importlib.util
import random
from helpers.weight_utils import weighted_choice
from helpers.generation_context import GenerationContext, parse_overrides
#todo:
# - implement bloodline generation being determined by current soul force
# - potentially implement certain demon beast types being more likely under certain conditions


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def generate_demon_beast(realm:str = 'earthen',
                         ctx: GenerationContext = GenerationContext()
                         ) -> dict:
    from .soul_rank_generator import generate_soul_rank
    from .element_generator import generate_element
    from .bloodline_generator import generate_bloodline

    # Directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    validators_dir = os.path.join(root_dir, 'validators')
    reference_dir = os.path.join(root_dir, 'reference')


    # 1. Demon beast type
    beast_types_data = load_json(os.path.join(validators_dir, 'valid_demon_beast_types.json'))
    demon_beast_types = beast_types_data.get('values', beast_types_data)
    demon_beast_type = weighted_choice(
        list(demon_beast_types),
        weights_path=os.path.join(reference_dir, 'roll_weights', 'demon_beast_types.json'),
        override_weights= ctx.override_demon_beast_weights,
        exclusive=True
    )

    # 2. Soul rank (earthen only)
    soul_rank_data = generate_soul_rank(ctx=ctx)

    # 3. Element attribute and name variant

    element_name_mapping = load_json(os.path.join(reference_dir, 'element_names_map.json'))
    element = generate_element(ctx=ctx, soul_force = soul_rank_data['soul_force'])  # returns {'id', 'display_name', ...}
    element_id = element['id']
    element_name = random.choice(element_name_mapping[element_id])

    # 4. Bloodline generation
    bloodline = generate_bloodline(origin_beast_type=demon_beast_type, ctx=ctx)

    # 5. Construct full flavor name
    full_name = f"{element_name} {demon_beast_type}" if element_name else demon_beast_type

    # Assemble demon beast object
    demon_beast = {
        'name': full_name,
        'soul_rank': {'major': soul_rank_data['major'], 'minor': soul_rank_data['minor']},
        'demon_beast_type': demon_beast_type,
        'stats': {'soul_force': soul_rank_data['soul_force'],
                  'cached_combat_power': 0  # Placeholder
                  },
        'soul': {
            'element': element,
        },
        'bloodline': bloodline
    }
    return demon_beast

def main():
    parser = argparse.ArgumentParser(description='Generate a complete demon beast object for TDAG.')
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
    help="Output format: 'json' for raw, 'pretty' for indented."
    )
    args = parser.parse_args()
    overrides = parse_overrides(args.override)  # where --override flags are collected
    ctx = GenerationContext(**overrides)


    beast = generate_demon_beast(ctx=ctx)
    if args.output == 'json':
        print(json.dumps(beast))
    else:
        print(json.dumps(beast, indent=2))

main()