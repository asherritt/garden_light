import RPi.GPIO as GPIO
from rpi_ws281x import *
import argparse
import schedule
import requests
import json
from datetime import datetime
from dataclasses import dataclass
import time
from color import init_color_steps
from wled_api import send_wled_preset_request

# LED strip configuration
LED_COUNT = 144
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 40
LED_INVERT = False
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_BRGW

# GPIO pin configuration for relays
PIN_RELAY_1 = 12
PIN_RELAY_2 = 16
PIN_RELAY_3 = 20
PIN_RELAY_4 = 21

# Location for sun times API
LAT, LNG = 34.0900, -118.036873

final_phase_executed = False

@dataclass
class DayPhase:
    name: str
    time: str
    color: tuple
    steps: int
    preset: int
    lamps_on: bool

day_phases = [
    DayPhase(name='midnight', color=(0, 8, 0, 0), time='12:00:00 AM', steps=0, preset=1, lamps_on=True),
    DayPhase(name='first_light', color=(0, 30, 0, 8), time=None, steps=0, preset=2, lamps_on=False),
    DayPhase(name='dawn', color=(90, 0, 15, 30), time=None, steps=0, preset=3, lamps_on=False),
    DayPhase(name='sunrise', color=(120, 0, 25, 45), time=None, steps=0, preset=4, lamps_on=False),
    DayPhase(name='solar_noon', color=(200, 255, 190, 255), time=None, steps=0, preset=5, lamps_on=False),
    DayPhase(name='golden_hour', color=(255, 0, 20, 90), time=None, steps=0, preset=6, lamps_on=False),
    DayPhase(name='sunset', color=(200, 0, 10, 125), time=None, steps=0, preset=7, lamps_on=False),
    DayPhase(name='dusk', color=(15, 40, 20, 10), time=None, steps=0, preset=8, lamps_on=True),
    DayPhase(name='last_light', color=(0, 10, 0, 0), time=None, steps=0, preset=9, lamps_on=True),
    DayPhase(name='midnight2', color=(0, 8, 0, 0), time='11:59:59 PM', steps=0, preset=1, lamps_on=True),
]

def fetch_sun_times():
    """Fetch sun times from the API."""
    print("Fetching sun times...")
    url = f"https://api.sunrisesunset.io/json?lat={LAT}&lng={LNG}&formatted=0"
    response = requests.get(url)
    data = response.json()
    print(data)
    return {
        "first_light": data['results']['first_light'],
        "dawn": data['results']['dawn'],
        "sunrise": data['results']['sunrise'],
        "solar_noon": data['results']['solar_noon'],
        "golden_hour": data['results']['golden_hour'],
        "sunset": data['results']['sunset'],
        "dusk": data['results']['dusk'],
        "last_light": data['results']['last_light'],
        "day_length": data['results']['day_length']
    }

def save_to_json(data):
    """Save sun times to a JSON file."""
    print("Saving sun times...")
    with open('./times.json', 'w') as f:
        json.dump(data, f)

def update_sun_times():
    """Fetch and update sun times."""
    print("Fetching new sun times...")
    sun_times = fetch_sun_times()
    save_to_json(sun_times)
    print("Sun times json updated.")

def init_phases():
    """Initialize day phases with times from JSON."""
    with open('./times.json', 'r') as f:
        sun_times = json.load(f)
    for k in sun_times.keys():
        phase = next((phase for phase in day_phases if phase.name == k), None)
        if phase:
            phase.time = sun_times[k]

    next_index = 1
    for i in range(len(day_phases)):
        next_time = datetime.strptime(day_phases[next_index].time, '%I:%M:%S %p')
        time_diff = next_time - datetime.strptime(day_phases[i].time, '%I:%M:%S %p')
        day_phases[i].steps = round(time_diff.total_seconds() / 60)
        next_index += 1
        next_index = 0 if next_index >= len(day_phases) else next_index
     
    print("day_phases created")
    print(day_phases)

def initialize_all():
    """Initialize phases, schedules, and color steps."""
    global color_steps
    print("Initializing phases, schedules, and color steps...")

    update_sun_times()
    # Fetch and save sun times if needed
    try:
        with open('./times.json', 'r') as f:
            json.load(f)
    except FileNotFoundError:
         print("times.json file is missing!")

    # Initialize day phases
    init_phases()
    schedule.clear()

    # Schedule WLED requests for each phase
    for phase in day_phases:
        print(f"schedule for {phase.time}")
        schedule.every().day.at(phase.time).do(handle_phase_execution, phase=phase)

    # Schedule periodic sun times update
    # schedule.every().day.at("10:30").do(update_sun_times)

    # Initialize color steps for NeoPixel
    color_steps = init_color_steps(day_phases)

def init_relays():
    """Initialize GPIO pins for relay control."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_RELAY_1, GPIO.OUT)
    GPIO.setup(PIN_RELAY_2, GPIO.OUT)
    GPIO.setup(PIN_RELAY_3, GPIO.OUT)
    GPIO.setup(PIN_RELAY_4, GPIO.OUT)
    GPIO.output(PIN_RELAY_1, GPIO.LOW)
    GPIO.output(PIN_RELAY_2, GPIO.LOW)
    GPIO.output(PIN_RELAY_3, GPIO.LOW)
    GPIO.output(PIN_RELAY_4, GPIO.LOW)

def toggle_relays(state):
    """Toggle the relays based on the `state`."""
    gpio_state = GPIO.HIGH if state else GPIO.LOW
    GPIO.output(PIN_RELAY_1, gpio_state)
    GPIO.output(PIN_RELAY_2, gpio_state)
    GPIO.output(PIN_RELAY_3, gpio_state)
    GPIO.output(PIN_RELAY_4, gpio_state)
    print(f"Relays turned {'ON' if state else 'OFF'}.")

def handle_phase_execution(phase):
    """Handle execution of a specific phase."""
    global final_phase_executed
    send_wled_preset_request(preset_number=phase.preset)
    toggle_relays(phase.lamps_on)
    if phase.name == "midnight2":
        print("Final phase executed. Preparing to reinitialize...")
        final_phase_executed = True

def current_minutes():
    """Return the current time in minutes since midnight."""
    now = datetime.now()
    return now.hour * 60 + now.minute

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='Clear the display on exit')
    args = parser.parse_args()

    init_relays()

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()

    print("Press Ctrl-C to quit.")
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit.')

    initialize_all()

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

            if final_phase_executed:
                final_phase_executed = False
                initialize_all()

            time.sleep(15)
    except KeyboardInterrupt:
        if args.clear:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
        GPIO.cleanup()
