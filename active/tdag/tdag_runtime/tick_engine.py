import time
from game_state import load_state, save_state
from processors import cultivation, event_triggers

TICK_INTERVAL_SECONDS = 5  # for demo; in real, use 60 or 3600 (hour)

def run_simulation():
    state = load_state()
    tick_count = 0

    try:
        while True:
            tick_count += 1
            print(f"Tick {tick_count} started.")

            # Apply game systems
            cultivation.process(state)
            event_triggers.process(state)

            # Save snapshot every 10 ticks
            if tick_count % 10 == 0:
                save_state(state)

            time.sleep(TICK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("Simulation stopped. Saving state...")
        save_state(state)