import argparse
from datetime import datetime
from typing import List
from garden_fill_light import *
from model import Step
from sunrisesunset_api import get_phases 
from color import get_steps

def _get_steps_up_to_now(steps: List[Step]) -> List[Step]:
    """Slice the list of steps up to the current time."""
    # Get the current time
    current_time = datetime.now().time()
    
    print(f"current_time: {current_time}")

    # Filter steps that are less than or equal to the current time
    steps_up_to_now = [
        step
        for step in steps
        if datetime.strptime(step.time, "%H:%M:%S").time() >= current_time
    ]
    
    return steps_up_to_now

def init():
    # 4. Interpolate colors for each step and put in list
    # 5. Start sequence
    # 6. Reinvoke init once all done

    #  """Initialize phases, schedules, and color steps."""
    # global color_steps
    # print("Initializing phases, schedules, and color steps...")

    phases = get_phases()

    steps = _get_steps_up_to_now(get_steps(phases))

    print(f"steps: {len(steps)}")

    # Initialize color steps for NeoPixel
    # color_steps = init_color_steps(day_phases)


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
