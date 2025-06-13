#!/usr/bin/env python3
"""
Demon Beast Object Generator for TDAG Simulation

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
from meta.utils import load_json, get_common_paths, validate_value
#todo:
# - implement bloodline generation being determined by current soul force
# - potentially implement certain demon beast types being more likely under certain conditions

from generators.registry import register
@register('demon_beast')
def generate_demon_beast(realm:str = 'earthen',
                         ctx: GenerationContext = GenerationContext()
                         ) -> dict:
    from soul_rank_generator import generate_soul_rank
    from element_generator import generate_element
    from bloodline_generator import generate_bloodline

    # Directories
    paths = get_common_paths()
    reference_dir = paths['reference']

    # 1. Demon beast type
    demon_beast_types_list = load_json(os.path.join(reference_dir, 'demon_beast', 'demon_beast_types.json'))
    demon_beast_type = weighted_choice(
        demon_beast_types_list,
        weights_path=os.path.join(reference_dir, 'roll_weights', 'demon_beast_types.json'),
        override_weights= ctx.override_demon_beast_weights,
        exclusive=True
    )

    # 2. Soul rank (earthen only)
    soul_rank_data = generate_soul_rank(ctx=ctx)

    # 3. Element attribute and name variant

    element_name_mapping = load_json(os.path.join(reference_dir, 'element_names_map.json'))
    element = generate_element(ctx=ctx, soul_force = soul_rank_data['soul_force'])
    element_id = element['id']
    element_name = random.choice(element_name_mapping[element_id])

    # 4. Bloodline generation
    bloodline = generate_bloodline(origin_beast_type=demon_beast_type, ctx=ctx)

    # 5. Construct full flavor name
    full_name = f"{element_name} {demon_beast_type}" if element_name else demon_beast_type

    # Assemble demon beast object
    demon_beast = {
        'name': full_name,
        'demon_beast_type': demon_beast_type,
        'stats': {'soul_force': soul_rank_data['soul_force'],
                  'cached_combat_power': 0  # Placeholder
                  },
        'soul': {
            'soul_rank': {'major': soul_rank_data['major'], 'minor': soul_rank_data['minor']},
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

if __name__ == '__main__':
    main()