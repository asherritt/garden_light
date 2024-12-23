from garden_fill_light import *
from sunrisesunset_api import fetch_sun_times 

def init():

    
    # 2. Update day phases
    # 3. Calculate steps
    # 4. Interpolate colors for each step and put in list
    # 5. Start sequence
    # 6. Reinvoke init once all done

    #  """Initialize phases, schedules, and color steps."""
    # global color_steps
    # print("Initializing phases, schedules, and color steps...")

    # 1. API load sunrise io data
    sun_times = fetch_sun_times()

    # Initialize day phases
    init_phases()
    init_wled(day_phases)
    # Initialize color steps for NeoPixel
    color_steps = init_color_steps(day_phases)


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

    start_index = current_minutes()
    try:
        while True:
            for i in range(strip.numPixels()):
                try:
                    strip.setPixelColor(i, color_steps[start_index + i])
                except IndexError:
                    start_index = 0
            strip.show()
            start_index += 1

            schedule.run_pending()

            if globals.final_phase_executed:
                globals.final_phase_executed = False
                initialize_all()

            time.sleep(15)
    except KeyboardInterrupt:
        if args.clear:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
        GPIO.cleanup()2