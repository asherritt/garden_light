import argparse
from datetime import datetime
import time
from typing import List
from garden_fill_light import *
from model import Step
from realys import gpio_cleanup, init_relays, set_relays
from sunrisesunset_api import get_phases 
from wled_api import set_cyc_light
from color import get_steps
import atexit

STEP_TIME = 2

def _on_exit():
    """Perform all necessary cleanup tasks."""
    print("Performing cleanup...")
    # Cleanup GPIO resources
    gpio_cleanup()
    # Add additional cleanup tasks here as needed
    print("Cleanup complete.")

def _get_steps_after_now(steps: List[Step]) -> List[Step]:
    """Slice the list of steps that occur after the current time."""
    # Get the current time as a time object
    # current_time = datetime.now().time()
    return steps
    # Filter steps that occur after the current time
    # steps_after_now = [
    #     step for step in steps
    #     if datetime.strptime(step.time, "%H:%M:%S").time() >= current_time
    # ]
    
    # return steps_after_now

def _process_step(step):
    print(f"Processing step {step}")
    set_light(step.fill_light)
    set_cyc_light(step.cyc)
    set_relays(step.lamps_on)

def _init_phases():
    phases = get_phases()
    steps = _get_steps_after_now(get_steps(phases))
    while steps:
        # Dequeue the first step
        current_step = steps.pop(0)
        _process_step(current_step)
        # Wait for one minute before processing the next step, if there are more steps
        if steps:
            print(f"current_step {current_step}")
            time.sleep(STEP_TIME) 
    _init_phases()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='Clear the display on exit')
    args = parser.parse_args()

    # on exit handler
    atexit.register(_on_exit)

    init_relays()

    # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # strip.begin()

    print("Press Ctrl-C to quit.")
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit.')

    _init_phases()
