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

from element_generator import generate_element
from soul_generator import generate_soul
from soul_rank_generator import generate_soul_rank
from soul_color_generator import generate_soul_color
from bloodline_generator import generate_bloodline
from cultivation_technique_generator import generate_cultivation_technique
# todo: need to use generation context


def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_cultivator() -> dict:
    # 1) Soul (element + form)
    soul = generate_soul()

    # 2) Soul rank & force
    rank_info = generate_soul_rank()
    major = rank_info['major']
    minor = rank_info['minor']
    soul_force = rank_info['soul_force']

    # 3) Soul color
    color_info = generate_soul_color()
    soul_color = color_info['color']
    color_rarity = color_info['rarity']

    # 4) Body rank and class
    body_rank = major
    cls = 'fighter' if soul_force < 100 else 'cultivator'

    # 5) Bloodline generation (optional)
    bloodline = generate_bloodline(origin_beast_type=None)

    # 6) Active cultivation technique (optional)
    technique = generate_cultivation_technique()
    active_tech_id = technique.get('id') if technique else None

    # 7) Cached cultivation speed
    cultivation_base_speed = technique.get('base_cultivation_speed') if technique else None

    # 8) Cached combat power (snapshot of soul_force modified by element matching)
    # simple: use soul_force as base
    cached_combat_power = soul_force

    cultivator = {
        'id': str(uuid.uuid4()),
        'soul': soul,
        'soul_rank': {'major': major, 'minor': minor},
        'soul_force': soul_force,
        'soul_color': {'color': soul_color, 'rarity': color_rarity},
        'body_rank': body_rank,
        'class': cls,
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
