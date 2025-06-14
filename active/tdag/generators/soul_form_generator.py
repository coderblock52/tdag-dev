#!/usr/bin/env python3
"""
Soul Form Generator for TDAG Simulation

Location: <root_directory>/generators/soul_form_generator.py

This script produces a soul-form object containing:
- element (string)
- quality (string)
- form_name (string)
- modifier (number)

It loads:
- validators/valid_soul_form_quality.json
- reference/soul/soul_form_modifiers.json
- reference/soul/soul_form_name_map.json
- generators/element_generator.py (for element fallback)
"""

import os
import json
import random
import argparse
from meta.utils import load_json, get_common_paths, validate_value
from helpers.weight_utils import weighted_choice
from helpers.generation_context import GenerationContext, parse_overrides
# need to implement generation context

def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

from generators.registry import register
@register('soul_form')
def generate_soul_form(element: str = None, quality: str = None, ctx:GenerationContext=GenerationContext()) -> dict:
    from generators.element_generator import generate_element
    # Resolve dirs
    paths = get_common_paths()
    reference_dir = paths['reference']

    # 1) Element fallback
    if not element:
        element = generate_element(ctx=ctx)

    # 2) Quality fallback (auto excludes highest tiers):
    quality = quality or weighted_choice(
        load_json(os.path.join(reference_dir, 'soul', 'soul_form_quality.json')),
        weights_path=os.path.join(reference_dir, 'roll_weights', 'soul_form_quality.json'),
        override_weights=ctx.override_soul_form_quality_weights,
        exclusive=True
    )


    # 3) Load modifier for this quality
    mods_map = load_json(os.path.join(reference_dir, 'soul', 'soul_form_modifiers.json'))
    quality_modifier = mods_map.get(quality)

    # 4) Load name-map and pick a name
    name_map = load_json(os.path.join(reference_dir, 'soul', 'soul_form_name_map.json'))
    element_map = name_map.get(element['id'], {})
    names = element_map.get(quality, [])
    form_name = random.choice(names)

    return {
        "element":    element,
        "quality":    quality,
        "form_name":  form_name,
        "modifier":   quality_modifier  
    }

def main():
    parser = argparse.ArgumentParser(description="Generate a soul-form for TDAG.")
    parser.add_argument('-e', '--element_id', help="Element ID (e.g. 'ice')", default=None)
    parser.add_argument('-q', '--quality', help="Soul-form quality", default=None)
    parser.add_argument(
    '--override', '-O',
    action='append',
    metavar='CAT:KEY=WEIGHT',
    help="e.g. db:wolf=80 or el:ice=30"
    )
    parser.add_argument('-o', '--output', choices=['json', 'pretty'], default='pretty', help="Output format")
    args = parser.parse_args()
    overrides = parse_overrides(args.override)  # where --override flags are collected
    ctx = GenerationContext(**overrides)

    soul_form = generate_soul_form(element_id=args.element_id, quality=args.quality)
    if args.output == 'json':
        print(json.dumps(soul_form))
    else:
        print(json.dumps(soul_form, indent=2))

if __name__ == '__main__':
    main()