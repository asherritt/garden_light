#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from rpi_ws281x import *
import argparse
import requests
import schedule
import numpy as np
import pytweening
import itertools
import json
from datetime import datetime, time,timedelta
from dataclasses import dataclass
import time  # Imports the time module to use time.sleep()
from datetime import time as datetime_time  # Import time from datetime with an alias

@dataclass
class DayPhase:
    name: str
    time: datetime
    color: tuple
    steps: int
    preset: int

# LED strip configuration:
LED_COUNT      = 144     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 40      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP = ws.SK6812_STRIP_BRGW # or ws.SK6812W_STRIP if your LEDs are ordered as WRGB

WLED_IP = "192.168.1.169"

day_phases = [
    DayPhase(name='midnight', color=(0, 8, 0, 0), time='12:00:00 AM', steps=0, preset=1, lamps_on: True),
    DayPhase(name='first_light', color=(0, 30, 0, 8), time=None, steps=0,  preset=2, lamps_on: False),
    DayPhase(name='dawn', color=(90, 0, 15, 30), time=None, steps=0, preset=3), lamps_on: False,
    DayPhase(name='sunrise', color=(120, 0, 25, 45), time=None, steps=0, preset=4, lamps_on: False),
    DayPhase(name='solar_noon', color=(200, 255, 190, 255), time=None, steps=0, preset=5, lamps_on: False),
    DayPhase(name='golden_hour', color=(255, 0, 20, 90), time=None, steps=0, preset=6, lamps_on: False),
    DayPhase(name='sunset', color=(200, 0, 10, 125), time=None, steps=0, preset=7, lamps_on: False),
    DayPhase(name='dusk', color=(15, 40, 20, 10), time=None, steps=0, preset=8, lamps_on: True),
    DayPhase(name='last_light', color=(0, 10, 0, 0), time=None, steps=0, preset=9, lamps_on: True),
    DayPhase(name='midnight2', color=(0, 8, 0, 0), time='11:59:59 PM', steps=0, preset=1, lamps_on: True),
    ]

color_steps = []

# # Define start and end colors as (R, B, G, W)
# start_color = (0, 30, 0, 18)                              
# end_color = (0, 30, 0, 18)

def current_minutes():
    # Get the current time
    current_time = datetime.now()
    # Extract the hour and minute components
    current_hour = current_time.hour
    current_minute = current_time.minute
    # Calculate the total minutes elapsed since midnight
    return current_hour * 60 + current_minute
                
def interpolate_colors(start_color, end_color, steps):
    # Unpack the start and end colors
    r1, b1, g1, w1 = start_color
    r2, b2, g2, w2 = end_color
    # Generate interpolated values for each color component
    r_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (r2 - r1) + r1) for i in range(steps)]
    g_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (g2 - g1) + g1) for i in range(steps)]
    b_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (b2 - b1) + b1) for i in range(steps)]
    w_values = [round(pytweening.easeInOutCubic(i / (steps - 1)) * (w2 - w1) + w1) for i in range(steps)]
    # Create color objects for each step
    color_objects = [Color(int(r), int(b), int(g), int(w)) for r, b, g, w in zip(r_values, b_values, g_values, w_values)]
    return color_objects

def init_phases():
    # clear the wled scheduler
    schedule.clear()
    # Load times from JSON
    with open('./times.json', 'r') as f:
        sun_times = json.load(f)
    # Manually add midnight time
    sun_times['midnight'] = '12:00:00 AM'
    # Remove day_length
    sun_times = {key: value for key, value in sun_times.items() if key != 'day_length'}
    # Convert times from string to datetime
    for k in sun_times.keys():
        phase = next((phase for phase in day_phases if phase.name == k), None)
        phase.time = sun_times[k]

    next_index = 1
    for i in range(len(day_phases)):
            next_time = datetime.strptime(day_phases[next_index].time, '%I:%M:%S %p')
            time_diff = next_time - datetime.strptime(day_phases[i].time, '%I:%M:%S %p')
            day_phases[i].steps = round(time_diff.total_seconds() / 60)  # Convert seconds to minutes
#           print(f'name: {day_phases[i].name} time: {day_phases[i].time} steps: {day_phases[i].steps}')
            schedule.every().day.at(next_time).do(send_wled_request, preset=day_phases[i].preset)

            next_index += 1
            next_index = 0 if next_index >= len(day_phases) else next_index

def init_color_steps():
    next_index = 1
    for d in day_phases:
        next_color = day_phases[next_index].color
        color_steps.extend(interpolate_colors(d.color, next_color, d.steps))
        next_index += 1
        # print(f'name: {d.name} time: {d.time} steps: {d.steps}')
        if next_index > len(day_phases) -1:
            next_index = 0

def wled_set_preset(preset_number):
    # URL for the JSON API endpoint
    url = f"http://{WLED_IP}/json/state"
   
    payload = {
        "ps": preset_number,
    }
    
    try:
    # Send the POST request
    response = requests.post(url, json=payload)
    # Check for successful response
    if response.status_code == 200:
        print(f"Preset {preset_number} activated.")
    else:
        print(f"Failed to activate preset. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")

def send_wled_request(preset):
    """Send API request to WLED to set a preset."""
    url = f"http://{WLED_IP}/json/state"
    payload = {
        "ps": preset
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Preset {preset} activated successfully.")
        else:
            print(f"Failed to activate preset {preset}. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    
    # Initalize Day Phases
    init_phases()
    # Initalize colors
    init_color_steps()
    
    start_index = current_minutes()
   
    try:  
        while True:
            for i in range(strip.numPixels()):
                try:
                    strip.setPixelColor(i, color_steps[start_index+i])
                except IndexError:
                    start_index = 0
            strip.show()
            start_index+=1
            time.sleep(15)

    except KeyboardInterrupt:
        if args.clear:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0,0,0))
            strip.show()
            
            
#  Turn On/Off relay for gas lamps
#  How to send WLED requests on time 