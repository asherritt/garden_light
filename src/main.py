import argparse
from datetime import datetime
import time
from typing import List
from garden_fill_light import *
from model import Step
from sunrisesunset_api import get_phases 
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

def init():
    # 4. Interpolate colors for each step and put in list
    # 5. Start sequence
    # 6. Reinvoke init once all done

    #  """Initialize phases, schedules, and color steps."""
    # global color_steps
    # print("Initializing phases, schedules, and color steps...")

    phases = get_phases()

    steps = _get_steps_after_now(get_steps(phases))

    while steps:
        # Dequeue the first step
        current_step = steps.pop(0)
        
        # Process the current step (you can replace this with your own logic)
        print(f"Processing step at time {current_step}")
        
        # Wait for one minute before processing the next step, if there are more steps
        if steps:
            print("Waiting for the next step...")
            time.sleep(5) 

    init()
    # Initialize color steps for NeoPixel
    # color_steps = init_color_steps(day_phases)
    
def _process_step(step):
    # 1. set strip color
    # 2. send wled request
    # 3. Check relays


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

    # start_index = current_minutes()
    # try:
    #     while True:
    #         for i in range(strip.numPixels()):
    #             try:
    #                 strip.setPixelColor(i, color_steps[start_index + i])
    #             except IndexError:
    #                 start_index = 0
    #         strip.show()
    #         start_index += 1

    #         schedule.run_pending()

    #         if globals.final_phase_executed:
    #             globals.final_phase_executed = False
    #             initialize_all()

    #         time.sleep(15)
    # except KeyboardInterrupt:
    #     if args.clear:
    #         for i in range(strip.numPixels()):
    #             strip.setPixelColor(i, Color(0, 0, 0))
    #         strip.show()
    #     GPIO.cleanup()
