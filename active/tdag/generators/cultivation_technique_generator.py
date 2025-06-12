#!/usr/bin/env python3
import os, json, random, uuid, argparse
from helpers.generation_context import GenerationContext, parse_overrides
from helpers.weight_utils import weighted_choice
from meta.utils import load_json, get_common_paths

def generate_cultivation_technique(quality=None, element=None,
                                   ctx: GenerationContext = GenerationContext()) -> dict:
    from generators.cultivation_technique_name_generator import generate_technique_name
    from element_generator import generate_element

    paths = get_common_paths()
    validators_dir = paths['validators']
    reference_dir = paths['reference']
    qualities_list = load_json(os.path.join(validators_dir, 'valid_cultivation_technique_qualities.json'))['values']
    speeds = load_json(os.path.join(reference_dir, 'cultivation_technique', 'base_cultivation_speeds.json'))

    # Quality selection
    q = quality or weighted_choice(qualities_list, 
                                  weights_path=os.path.join(reference_dir, 'roll_weights', 'cultivation_technique_qualities.json'),
                                  override_weights=ctx.override_cultivation_technique_quality_weights,
                                  exclusive=True)

    # Element selection
    elem = element or generate_element(ctx=ctx)['id']

    tech = {
        "id": str(uuid.uuid4()),
        "quality": q,
        "base_cultivation_speed": speeds[q],
        "element": elem,
        "name": generate_technique_name(elem, q),
        "soul_form_bonus": None
    }
    return tech

def main():
    parser = argparse.ArgumentParser(description="Generate a cultivation technique.")
    parser.add_argument('-q', '--quality', default=None, help="Technique quality")
    parser.add_argument('-e', '--element', default=None, help="Element ID")
    parser.add_argument('-o', '--output', choices=['json','pretty'], default='pretty')
    parser.add_argument('-O', '--overrides', type=str, default=None, help="JSON string of overrides for generation context")
    args = parser.parse_args()
    overrides = parse_overrides(args.overrides)  # where --override flags are collected
    ctx = GenerationContext(**overrides)
    tech = generate_cultivation_technique(quality=args.quality, element=args.element, ctx=ctx)
    out = json.dumps(tech) if args.output == 'json' else json.dumps(tech, indent=2)
    print(out)

if __name__ == '__main__':
    main()
