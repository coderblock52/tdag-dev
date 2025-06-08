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

def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_soul_form(element: str = None, quality: str = None) -> dict:
    # Resolve dirs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    validators_dir = os.path.join(root_dir, 'validators')
    ref_soul_dir = os.path.join(root_dir, 'reference', 'soul')

    # 1) Element fallback
    if not element:
        from element_generator import generate_element
        element = generate_element()

    # 2) Quality fallback (auto excludes highest tiers)
    qual_vals = load_json(os.path.join(validators_dir, 'valid_soul_form_quality.json'))['values']
    if not quality:
        # exclude top two tiers (assumes ordered list)
        auto_quals = qual_vals[:len(qual_vals)-2]
        quality = random.choice(auto_quals)
    elif quality not in qual_vals:
        raise ValueError(f"Unknown soul form quality: {quality}")

    # 3) Load modifier for this quality
    mods_map = load_json(os.path.join(ref_soul_dir, 'soul_form_modifiers.json'))
    quality_entry = mods_map.get(quality)
    if not quality_entry:
        raise ValueError(f"Missing modifier entry for quality '{quality}'")
    modifier = quality_entry['modifier']

    # 4) Load name-map and pick a name
    name_map = load_json(os.path.join(ref_soul_dir, 'soul_form_name_map.json'))
    element_map = name_map.get(element['id'], {})
    names = element_map.get(quality, [])
    if names:
        form_name = random.choice(names)
    else:
        # Fallback pattern if no names defined
        form_name = f"{quality.capitalize()} {element.replace('-', ' ').title()} Form"

    return {
        "element":    element,
        "quality":    quality,
        "form_name":  form_name,
        "modifier":   modifier
    }

def main():
    parser = argparse.ArgumentParser(description="Generate a soul-form for TDAG.")
    parser.add_argument('-e', '--element_id', help="Element ID (e.g. 'ice')", default=None)
    parser.add_argument('-q', '--quality', help="Soul-form quality", default=None)
    parser.add_argument('-o', '--output', choices=['json','pretty'], default='pretty',
                        help="Output format")
    args = parser.parse_args()

    soul_form = generate_soul_form(element_id=args.element_id, quality=args.quality)
    if args.output == 'json':
        print(json.dumps(soul_form))
    else:
        print(json.dumps(soul_form, indent=2))

if __name__ == '__main__':
    main()