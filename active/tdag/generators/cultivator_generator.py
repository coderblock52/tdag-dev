#!/usr/bin/env python3
"""
Cultivator Generator for TDAG Simulation

Location: <root_directory>/generators/cultivator_generator.py

Generates a complete cultivator entity with:
- id
- soul (element + soul_form)
- soul_rank (major, minor)
- soul_force
- soul_color (color + rarity)
- body_rank (major rank)
- class (fighter|cultivator)
- bloodline (full object)
- active_cultivation_technique (technique id)
- cached_cultivation_speed
- cached_combat_power
- integrated_demon_spirit (None placeholder)

Usage (CLI):
    python cultivator_generator.py [-o json|pretty]
"""
import os
import json
import uuid
import argparse
from helpers.weight_utils import weighted_choice
from helpers.generation_context import GenerationContext, parse_overrides
from meta.utils import load_json, get_common_paths, validate_value

from generators.registry import register
@register('cultivator')
def generate_cultivator(ctx:GenerationContext=GenerationContext()) -> dict:
    from generators.soul_generator import generate_soul
    from generators.soul_rank_generator import generate_soul_rank
    from generators.soul_color_generator import generate_soul_color
    from generators.bloodline_generator import generate_bloodline
    from generators.cultivation_technique_generator import generate_cultivation_technique
    paths = get_common_paths()

    roll_weights_dir = paths.get('roll_weights')
    # 1) Soul (element + form)
    soul = generate_soul(ctx=ctx)

    # 2) Soul rank & force
    rank_info = generate_soul_rank(ctx=ctx)
    major = rank_info['major']
    minor = rank_info['minor']
    soul_force = rank_info['soul_force']

    # 3) Soul color
    color_info = generate_soul_color(ctx=ctx)
    soul_color = color_info['color']
    color_rarity = color_info['rarity']

    # 4) Body rank and class
    char_class = 'fighter' if soul_force < 100 else 'cultivator'
    if char_class == 'fighter':
        #randomize body rank
        body_map = load_json(os.path.join(roll_weights_dir, 'ranks', 'body_ranks.json'))
        weighted_choice(list(body_map.keys()),
                        base_weights=body_map,
                        override_weights=ctx.override_body_rank_weights,
                        exclusive=True)
    else:
        body_rank = major

    # 5) Bloodline generation (optional)
    bloodline = generate_bloodline(origin_beast_type=None, ctx=ctx)

    # 6) Active cultivation technique (optional)
    technique = generate_cultivation_technique(ctx=ctx)
    active_tech_id = technique.get('id') if technique else None

    # 7) Cached cultivation speed
    cultivation_base_speed = technique.get('base_cultivation_speed') if technique else None

    # 8) Cached combat power (snapshot of soul_force modified by element matching)
    # simple: use soul_force as base
    cached_combat_power = soul_force

    cultivator = {
        'id': str(uuid.uuid4()),
        'soul':{
            'soul_form': soul,
            'soul_rank': {'major': major, 'minor': minor},
            'soul_force': soul_force,
            'soul_color': {'color': soul_color, 'rarity': color_rarity},
        },
        'body_rank': body_rank,
        'char_class': char_class,
        'bloodline': bloodline,
        'active_cultivation_technique': active_tech_id,
        'cached_cultivation_speed': cultivation_base_speed,
        'cached_combat_power': cached_combat_power,
        'integrated_demon_spirit': None
    }
    return cultivator


def main():
    parser = argparse.ArgumentParser(description="Generate a cultivator for TDAG.")
    parser.add_argument(
        '-o', '--output',
        choices=['json', 'pretty'],
        default='pretty',
        help="Output format: 'json' or 'pretty'."
    )
    args = parser.parse_args()

    cultivator = generate_cultivator()
    if args.output == 'json':
        print(json.dumps(cultivator))
    else:
        print(json.dumps(cultivator, indent=2))


if __name__ == '__main__':
    main()
