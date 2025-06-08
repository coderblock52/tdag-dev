#!/usr/bin/env python3
"""
Demon Beast Element Name Generator for TDAG Simulation

This script provides a function to generate a name component for a demon beast based on its elemental attribute.
If no element is specified, it selects a random element from the mapping.

Usage:
    python demon_beast_element_name_generator.py [--element ELEMENT_ID]

Examples:
    python demon_beast_element_name_generator.py --element sacred-fire
    # Output: Emberlight

    python demon_beast_element_name_generator.py
    # Output: (random element name variant)
"""
import random
import argparse
import os

# Mapping of element IDs to name variants
ELEMENT_NAME_MAPPING = {
    "none": [""],
    "sacred-fire": ["Sacred Flame", "Scarlet", "Emberlight", "Flame"],
    "water":       ["Water", "Tidecaller", "Mistveil"],
    "wind":        ["Wind", "Skywhirl", "Tempest"],
    "lightning":   ["Lightning", "Thunderstrike", "Voltshade"],
    "ice":         ["Ice", "Frostclaw", "Glacier"],
    "toxic":       ["Toxic", "Venomfang", "Corruption"],
    "chaos":       ["Chaos", "Riftborn", "Entropy"],
    "void":        ["Void", "Nether", "Oblivion"],
    "abyss":       ["Abyssal", "Depth", "Black"],
    "snow-wind":   ["Snow-Wind", "White Gale", "Icespire"],
    "lightning-fire": ["Lightning-Fire", "Stormflame", "Crackling Blaze"],
    "wind-lightning": ["Wind-Lightning", "Voltstorm", "Skyburst"]
}

def generate_element_name(element_id):
    """
    Given an element ID, randomly select one name variant.
    Raises a KeyError if the element ID is unknown.
    """
    variants = ELEMENT_NAME_MAPPING.get(element_id)
    if variants is None:
        raise KeyError(f"Unknown element ID: {element_id}")
    return random.choice(variants)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a demon beast name component based on element ID."
    )
    parser.add_argument(
        '-e', '--element',
        required=False,
        help="Element ID to generate a name for (e.g., sacred-fire, water).",
        default=None
    )
    args = parser.parse_args()

    # Choose element: provided or random
    if args.element:
        element_id = args.element
    else:
        element_id = random.choice(list(ELEMENT_NAME_MAPPING.keys()))

    try:
        name = generate_element_name(element_id)
        print(name)
    except KeyError as e:
        print(f"Error: {e}")
        print("Valid element IDs:", ", ".join(ELEMENT_NAME_MAPPING.keys()))

if __name__ == '__main__':
    main()
