#!/usr/bin/env python3
import os, json, random, uuid, argparse
from element_generator import generate_element
from cultivation_name_generator import generate_technique_name

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_cultivation_technique(quality=None, element=None):
    root = os.path.abspath(os.path.join(__file__, '..', '..'))
    vals = load_json(os.path.join(root, 'validators', 'valid_cultivation_technique_qualities.json'))['values']
    speeds = load_json(os.path.join(root, 'reference', 'cultivation_technique', 'base_cultivation_speeds.json'))

    # Quality selection
    weights = [60, 30, 7, 2, 0]
    if quality and quality not in vals:
        raise ValueError(f"Unknown quality: {quality}")
    q = quality or random.choices(vals, weights=weights)[0]

    # Element selection
    elem = element or generate_element()['id']

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
    args = parser.parse_args()
    tech = generate_cultivation_technique(args.quality, args.element)
    out = json.dumps(tech) if args.output == 'json' else json.dumps(tech, indent=2)
    print(out)

if __name__ == '__main__':
    main()
