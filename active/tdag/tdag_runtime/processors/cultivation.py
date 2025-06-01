def process(state):
    for cultivator in state.get("cultivators", []):
        gain = calculate_cultivation_gain(cultivator)
        cultivator["soul_force"] = cultivator.get("soul_force", 0) + gain
        print(f"{cultivator['name']} gains {gain} soul force.")

def calculate_cultivation_gain(cultivator):
    base = 10
    modifiers = cultivator.get("modifiers", {}).get("cultivation_speed", 1.0)
    return int(base * modifiers)