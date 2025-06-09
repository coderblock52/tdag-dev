# helpers/generation_context.py
from dataclasses import dataclass, field
from typing import Dict
from typing import Dict, List, Optional
import argparse

@dataclass
class GenerationContext:
    override_demon_beast_weights: Dict[str, float]      = field(default_factory=dict)
    override_element_weights: Dict[str, float]          = field(default_factory=dict)
    override_soul_color_weights: Dict[str, float]     = field(default_factory=dict)
    override_soul_form_weights: Dict[str, float]       = field(default_factory=dict)
    override_soul_rank_major_weights: Dict[str, float]       = field(default_factory=dict)
    override_soul_rank_minor_weights: Dict[str, float]       = field(default_factory=dict)
    override_cultivator_class_weights: Dict[str, float] = field(default_factory=dict)
    override_bloodline_weights: Dict[str, float]       = field(default_factory=dict)
    override_cultivation_technique_weights: Dict[str, float] = field(default_factory=dict)
    realm: str = 'earthen'  # default realm, can be overridden
    # add other override maps here as needed

def parse_overrides(arg_list: Optional[List[str]]) -> Dict[str, Dict[str, float]]:
    """
    Parse a list of override strings of the form 'category:key=value'
    into a dict suitable for GenerationContext initialization.

    Args:
        arg_list: list of strings, each 'category:key=value'
    Returns:
        dict mapping GenerationContext field names to override dicts
    Raises:
        argparse.ArgumentTypeError for invalid formats or unknown categories
    example usage:
    python3 -m generators.bloodline_generator -O bl:Epic=10 -O bl:Common=10
    build with add_argument:
    parser.add_argument(
    '--override', '-O',
    action='append',
    metavar='CAT:KEY=WEIGHT',
    help="e.g. db:wolf=80 or el:ice=30"
    )
    ...
    args = parser.parse_args()
    overrides = parse_overrides(args.override)  # where --override flags are collected
    ctx = GenerationContext(**overrides)
    """
    from argparse import ArgumentTypeError

    overrides: Dict[str, Dict[str, float]] = {}
    # Map CLI category keys to GenerationContext field names
    field_map = {
        'db':   'override_demon_beast_weights',       # Demon Beast
        'el':   'override_element_weights',           # Element
        'sc':   'override_soul_color_weights',        # Soul Color
        'sf':   'override_soul_form_weights',         # Soul Form
        'srmj': 'override_soul_rank_major_weights',   # Soul Rank Major
        'srmn': 'override_soul_rank_minor_weights',   # Soul Rank Minor
        'cc':   'override_cultivator_class_weights',  # Cultivator Class
        'bl':   'override_bloodline_weights',         # Bloodline
        'ct':   'override_cultivation_technique_weights',  # Cultivation Technique
        'r':   'realm',  # Realm, not a weight but can be set
        # extend with additional categories
    }

    for item in arg_list or []:
        try:
            cat_key, val = item.split('=', 1)
            category, key = cat_key.split(':', 1)
            weight = float(val)
        except ValueError:
            raise ArgumentTypeError(
                f"Invalid override '{item}', must be category:key=value"
            )
        field_name = field_map.get(category)
        if not field_name:
            raise ArgumentTypeError(f"Unknown override category '{category}'")
        overrides.setdefault(field_name, {})[key] = weight

    return overrides
