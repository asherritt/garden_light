import argparse
from datetime import datetime
import time
from typing import List
from garden_fill_light import *
from model import Step
from sunrisesunset_api import get_phases 
from wled_api import set_cyc_light
from color import get_steps

def _get_steps_after_now(steps: List[Step]) -> List[Step]:
    """Slice the list of steps that occur after the current time."""
    # Get the current time as a time object
    current_time = datetime.now().time()

    # Filter steps that occur after the current time
    steps_after_now = [
        step for step in steps
        if datetime.strptime(step.time, "%H:%M:%S").time() >= current_time
    ]
    
    return steps_after_now

def _process_step(step):
    print(f"Processing step {step}")
    set_light(step.fill_light)
    set_cyc_light(step.cyc)
    # 3. Check relays

def init():
    phases = get_phases()
    steps = _get_steps_after_now(get_steps(phases))
    while steps:
        # Dequeue the first step
        current_step = steps.pop(0)
        _process_step(current_step)
        # Wait for one minute before processing the next step, if there are more steps
        if steps:
            print(f"current_step {current_step}")
            time.sleep(60) 
    init()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='Clear the display on exit')
    args = parser.parse_args()

    # init_relays()

    # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # strip.begin()

    print("Press Ctrl-C to quit.")
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit.')

    init()
