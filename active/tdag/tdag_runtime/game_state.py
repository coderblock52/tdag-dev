import json
from pathlib import Path

SAVE_PATH = Path("tdag_runtime/save/state.json")

def load_state():
    if SAVE_PATH.exists():
        with open(SAVE_PATH, "r") as f:
            return json.load(f)
    else:
        # Fallback to an empty or starter state
        return {"cultivators": []}

def save_state(state):
    with open(SAVE_PATH, "w") as f:
        json.dump(state, f, indent=2)