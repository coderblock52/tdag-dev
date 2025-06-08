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
import random
import argparse


def load_json(path: str) -> list:
    """Load JSON array from a file path."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_element(element_id: str = None) -> dict:
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
        elem = element_map.get(element_id)
        if not elem:
            raise ValueError(f"Unknown element ID: {element_id}")
        return elem

    # Random selection
    return random.choice(elements)


def main():
    parser = argparse.ArgumentParser(description="Generate an element object for TDAG.")
    parser.add_argument(
        '-e', '--element',
        help="Element ID to fetch (e.g., 'ice'). If omitted, a random element is chosen.",
        default=None
    )
    parser.add_argument(
        '-o', '--output',
        choices=['json', 'pretty'],
        default='pretty',
        help="Output format: 'json' for raw JSON, 'pretty' for indented."
    )
    args = parser.parse_args()

    try:
        elem = generate_element(element_id=args.element)
    except ValueError as err:
        print(f"Error: {err}")
        return

    if args.output == 'json':
        print(json.dumps(elem))
    else:
        print(json.dumps(elem, indent=2))


if __name__ == '__main__':
    main()
