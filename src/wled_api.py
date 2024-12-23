import requests
import schedule
from datetime import datetime, timedelta
import globals
from utils import convert_rgb_int_to_rgb

WLED_IP = "192.168.1.169"

def _send_wled_set_request(cyc_rgb_colors):
    """Send API request to WLED to set a preset."""
    url = f"http://{WLED_IP}/json/state"

    payload = {
        "on": "true",
        "tt": 55000,
        "bri": 255,
        "ledmap": 0,
        "mainseg": 0,
        "seg": [
            {
            "id": 0,
            "start": 0,
            "stop": 20,
            "on": "true",
            "col": [[cyc_rgb_colors[0]]]
            },
            {
            "id": 1,
            "start": 20,
            "stop": 40,
            "on": "true",
            "col": [[cyc_rgb_colors[1]]]
            },
            {
            "id": 2,
            "start": 40,
            "stop": 60,
            "on": "true",
            "col": [[cyc_rgb_colors[2]]]
            },
            {
            "id": 3,
            "start": 60,
            "stop": 80,
            "on": "true",
            "col": [[cyc_rgb_colors[3]]]
            },
            {
            "id": 4,
            "start": 80,
            "stop": 100,
            "on": "true",
            "col": [[cyc_rgb_colors[4]]]
            }
        ]
        }
        
    print(f"payload: {payload}")

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"cyc colors activated successfully.")
        else:
            print(f"Failed to activate cyc colors. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")

def set_cyc_light(cyc_color_rgb_int_segments):
    cyc_rbg_colors = []
    for cyc_color in cyc_color_rgb_int_segments:
        converted_cyc_colors = convert_rgb_int_to_rgb(cyc_color)
        print(f"converted_cyc_colors: {converted_cyc_colors}")
        cyc_rbg_colors.append(converted_cyc_colors)

    _send_wled_set_request(cyc_rbg_colors)
