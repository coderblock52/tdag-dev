import os
from meta.utils import load_json, get_common_paths

# todo: will refactor this when managing calculations for cultivation speed
def apply_soul_color_modifier(base_speed: float, technique_quality: str, soul_color: str) -> float:
    """
    Adjust base_speed based on the soul_color interaction with technique_quality:
    - common: no bonus
    - uncommon: poor/good → treat quality one tier higher (cap at 'great')
    - rare: as uncommon; additionally, if technique is 'great', apply +0.5 multiplier bonus

    Returns the modified cultivation speed.
    """
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, '..'))
    validators_dir = os.path.join(root_dir, 'validators')
    ref_ct_dir = os.path.join(root_dir, 'reference', 'cultivation_technique')
    ref_soul_dir = os.path.join(root_dir, 'reference', 'soul')


    # Load quality tiers and base speeds
    qualities = load_json(os.path.join(validators_dir, 'valid_cultivation_technique_qualities.json'))['values']
    speeds = load_json(os.path.join(ref_ct_dir, 'base_cultivation_speeds.json'))

    # Load color rarity map
    color_map = load_json(os.path.join(ref_soul_dir, 'soul_color.json'))
    # Determine rarity for the given color
    rarity = None
    for r, cols in color_map.items():
        if soul_color == cols[0] or soul_color in cols:
            rarity = r
            break
    if rarity is None:
        raise ValueError(f"Unknown soul color: {soul_color}")

    # Helper to bump quality one tier (used by uncommon and rare)
    def bump(q: str) -> str:
        idx = qualities.index(q)
        # cap bump at 'great'
        cap = qualities.index('great')
        return qualities[min(idx + 1, cap)]

    # Apply logic
    if rarity == 'common':
        return base_speed
    if rarity == 'uncommon':
        if technique_quality in ['poor', 'good']:
            new_q = bump(technique_quality)
            return speeds[new_q]
        return base_speed
    if rarity == 'rare':
        if technique_quality in ['poor', 'good']:
            new_q = bump(technique_quality)
            return speeds[new_q]
        if technique_quality == 'great':
            # +0.5 bonus to multiplier: e.g. 1.0 → 1.5
            return base_speed * 1.5
        return base_speed
    return base_speed
