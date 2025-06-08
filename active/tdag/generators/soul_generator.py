#!/usr/bin/env python3
"""
Soul Generator for TDAG Simulation

Location: <root_directory>/generators/soul_generator.py

Generates a soul object for cultivators, combining:
- An elemental affinity (using element_generator)
- A soul form (using soul_form_generator)

Fields returned:
- element: full element object ({id, display_name, match_bonus, ...})
- soul_form: object ({element, quality, form_name, modifier})

Usage:
    python soul_generator.py [-e ELEMENT_ID] [-q QUALITY] [-r REALM] [-o json|pretty]
"""
import argparse
import json

from element_generator import generate_element
from soul_form_generator import generate_soul_form


def generate_soul(element = None,
                  quality: str = None,
                  realm: str = 'earthen') -> dict:
    """
    Build a soul object:
    - element_id: optional, picks random if None
    - quality: optional, picks random (auto-excludes top tiers) if None
    - realm: passed through to soul_form_generator if needed
    """
    # 1) Element selection
    if not element:
      element = generate_element()

    # 2) Soul form generation
    #    Pass element id and quality to control form name and modifier
    soul_form = generate_soul_form(element, quality=quality)

    return {
        'element':    element,
        'soul_form':  soul_form
    }


def main():
    parser = argparse.ArgumentParser(description="Generate a soul for TDAG cultivators.")
    parser.add_argument('-e', '--element', help="Element ID (e.g., 'ice')", default=None)
    parser.add_argument('-q', '--quality', help="Soul-form quality", default=None)
    parser.add_argument('-r', '--realm', help="Soul realm (earthen or heavenly)", default='earthen')
    parser.add_argument('-o', '--output', choices=['json','pretty'], default='pretty',
                        help="Output format: 'json' for raw output, 'pretty' for indented.")
    args = parser.parse_args()

    soul = generate_soul(element=args.element,
                         quality=args.quality,
                         realm=args.realm)

    if args.output == 'json':
        print(json.dumps(soul))
    else:
        print(json.dumps(soul, indent=2))


if __name__ == '__main__':
    main()