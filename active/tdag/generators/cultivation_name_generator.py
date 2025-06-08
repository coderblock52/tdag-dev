#!/usr/bin/env python3
"""
Cultivation Technique Name Generator for TDAG Simulation

Location: <root_directory>/generators/cultivation_name_generator.py

Composes technique names based on:
- `element` ID → display name from `reference/elements/elements.json`
- `quality` → thematic roots from `reference/cultivation_technique/cultivation_quality_name_map.json`

Final format: "<Element Display> <Tech Root> Technique"

Usage (CLI):
    python cultivation_name_generator.py [-e ELEMENT_ID] [-q QUALITY] [-o json|pretty]
"""
import os
import json
import random
import argparse

def load_json(path: str) -> dict:
    """Load JSON data from the given file path."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_technique_name(element: str, quality: str) -> str:
    """
    Generate a cultivation technique name by combining an element display name
    with a quality-themed root, appending 'Technique'.

    Args:
        element: element ID (e.g., 'ice')
        quality: technique quality (e.g., 'great')
    Returns:
        Full technique name string.
    """
    # Resolve directories
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))

    
    ####
    # 1) Determine tech_root and get correct tech root name 
    if quality == 'good':
        # special case: pick a Demon Beast type instead
        db_path = os.path.join(
            root_dir,
            'reference',
            'demon_beast',
            'demon_beast_types.json'
        )
        db_types = load_json(db_path)
        # if file is a dict with "values" key, otherwise assume it's a list
        types_list = db_types.get('values', db_types)
        tech_root = random.choice(types_list)
    else:
        # Load quality name map
        qmap_path = os.path.join(
        root_dir,
        'reference',
        'cultivation_technique',
        'cultivation_quality_name_map.json'
    )
        quality_map = load_json(qmap_path)
        roots = quality_map.get(quality, [])
        tech_root = random.choice(roots) if roots else quality.capitalize()

    # 2) Load element display name
    elements_path = os.path.join(
        root_dir,
        'reference',
        'elements',
        'elements.json'
    )
    elements = load_json(elements_path)
    display_map = {e['id']: e['display_name'] for e in elements}
    element_display = display_map.get(
        element,
        element.replace('-', ' ').title()
    )

    # 3) Compose final name
    return f"{element_display} {tech_root} Technique" if element_display != 'None' else f"{tech_root} Technique"

def main():
    parser = argparse.ArgumentParser(description="Generate a cultivation technique name for TDAG.")
    parser.add_argument(
        '-e', '--element',
        help="Element ID (e.g., 'ice')",
        default=None
    )
    parser.add_argument(
        '-q', '--quality',
        help="Technique quality (poor..god)",
        default=None
    )
    parser.add_argument(
        '-o', '--output',
        choices=['json', 'pretty'],
        default='pretty',
        help="Output format: 'json' for raw JSON, 'pretty' for indented."
    )
    args = parser.parse_args()

    # Default fallbacks
    quality = args.quality or random.choice(
        load_json(os.path.join(
            os.path.abspath(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..'
            )),
            'validators',
            'valid_cultivation_technique_qualities.json'
        ))['values']
    )
    element = args.element or random.choice(
        [e['id'] for e in load_json(os.path.join(
            os.path.abspath(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..'
            )),
            'reference',
            'elements',
            'elements.json'
        ))]
    )

    name = generate_technique_name(element, quality)
    if args.output == 'json':
        print(json.dumps({'name': name}))
    else:
        print(name)

if __name__ == '__main__':
    main()
