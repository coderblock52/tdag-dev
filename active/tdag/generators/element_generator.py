#!/usr/bin/env python3
"""
Element Object Generator for TDAG Simulation

Location: <root_directory>/generators/element_generator.py

Loads the element definitions from `reference/elements/elements.json` and returns
an element object, either randomly or by specified ID.

Provides:
- generate_element(element_id: str = None) -> dict

Usage:
    python element_generator.py [--element ELEMENT_ID] [-o json|pretty]
"""
import os
import json
import argparse
from helpers.generation_context import GenerationContext, parse_overrides
from helpers.weight_utils import weighted_choice
# todo: need to implement forcing an element to exist if the soul force provided is over 10,000


def load_json(path: str) -> list:
    """Load JSON array from a file path."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_element(element_id: str = None,
                     soul_force: int = None,
                     ctx:GenerationContext = GenerationContext()) -> dict:
    """
    Returns an element object:
    - If element_id is provided, returns that element (or raises ValueError).
    - If not, picks one at random from the reference list.
    """
    # Resolve reference path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    ref_path = os.path.join(root_dir, 'reference', 'elements', 'elements.json')

    elements = load_json(ref_path)
    element_map = {e['id']: e for e in elements}

    if element_id:
        elem = element_map.get(element_id.lower())
        if not elem:
            raise ValueError(f"Unknown element ID: {element_id}")
        return elem

    # Random selection
    # exclusive if a weight dict is provided, otherwise it's not exclusive
    # but if a soul force is provided, we need to setup the weight to be None:0.0 if soul_force is 10,000 or more
    if ctx.override_element_weights:
        exclusive = True
    else:
        exclusive = False
    if soul_force:
        if soul_force >= 10000:
            # Force an element to exist if soul force is gold or above
            ctx.override_element_weights['None'] = 0.0
        elif soul_force < 1000:
            # If soul force is below silver, no element is allowed
            ctx.override_element_weights = {'None':1.0}
            exclusive = True

    element_id = weighted_choice(
        list(element_map.keys()),
        weights_path=os.path.join(root_dir, 'reference', 'roll_weights', 'elements.json'),
        override_weights=ctx.override_element_weights,
        exclusive=exclusive
    )
    return element_map[element_id.lower()]


def main():
    parser = argparse.ArgumentParser(description="Generate an element object for TDAG.")
    parser.add_argument(
        '-e', '--element',
        help="Element ID to fetch (e.g., 'ice'). If omitted, a random element is chosen.",
        default=None
    )
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
        help="Output format: 'json' for raw JSON, 'pretty' for indented."
    )
    args = parser.parse_args()
    overrides = parse_overrides(args.override)  # where --override flags are collected
    ctx = GenerationContext(**overrides)

    elem = generate_element(element_id=args.element, ctx=ctx)
    if args.output == 'json':
        print(json.dumps(elem))
    else:
        print(json.dumps(elem, indent=2))


if __name__ == '__main__':
    main()
