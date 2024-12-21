import requests
import json
from datetime import datetime
from rpi_ws281x import *
import argparse
import schedule
import numpy as np
import pytweening
import time
from dataclasses import dataclass
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
    url = f"https://api.sunrisesunset.io/json?lat={LAT}&lng={LNG}&formatted=0"
    response = requests.get(url)
    data = response.json()
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
    with open('./times.json', 'w') as f:
        json.dump(data, f)

def update_sun_times():
    """Fetch and update sun times."""
    print("Fetching new sun times...")
    sun_times = fetch_sun_times()
    save_to_json(sun_times)
    print("Sun times updated.")
    initialize_all()  # Reinitialize with new times

def initialize_all():
    """Initialize phases, schedules, and color steps."""
    global color_steps
    print("Initializing phases, schedules, and color steps...")

    # Fetch and save sun times if the file doesn't exist
    try:
        with open('./times.json', 'r') as f:
            json.load(f)
    except FileNotFoundError:
        update_sun_times()

    # Initialize day phases
    init_phases()
    schedule.clear()

    # Schedule WLED requests for each phase
    for phase in day_phases:
        if phase.time:
            schedule.every().day.at(phase.time).do(handle_phase_execution, phase=phase)

    # Schedule periodic sun times update
    schedule.every().day.at("12:00:00 AM").do(update_sun_times)

    # Initialize color steps for NeoPixel
    color_steps = init_color_steps(day_phases)

# Remaining code (NeoPixel updates, GPIO handling, etc.) stays the same