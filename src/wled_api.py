import requests
import schedule
from datetime import datetime, timedelta
import globals

WLED_IP = "192.168.1.168"
BRIGHTNESS = 100

def _send_wled_set_request(cyc_rgb_colors):
    """Send API request to WLED to set a preset."""
    url = f"http://{WLED_IP}/json/state"

    payload = {
        "on": True,
        "tt": 55000,
        "bri": BRIGHTNESS,
        "ledmap": 0,
        "mainseg": 0,
        "seg": [
            {
            "id": 0,
            "start": 0,
            "stop": 20,
            "on": True,
            "col": [list(cyc_rgb_colors[0])]
            },
            {
            "id": 1,
            "start": 20,
            "stop": 40,
            "on": True,
            "col": [list(cyc_rgb_colors[1])]
            },
            {
            "id": 2,
            "start": 40,
            "stop": 60,
            "on": True,
            "col": [list(cyc_rgb_colors[2])]
            },
            {
            "id": 3,
            "start": 60,
            "stop": 80,
            "on": True,
            "col": [list(cyc_rgb_colors[3])]
            },
            {
            "id": 4,
            "start": 80,
            "stop": 100,
            "on": True,
            "col": [list(cyc_rgb_colors[4])]
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

def set_cyc_light(cyc_color_tuples):
    """
    Set the cyclical light segments to the colors in the provided list of tuples.
    :param cyc_color_tuples: A list of tuples representing RGB or RGBW colors.
    """
    cyc_rgb_colors = []

    for cyc_color in cyc_color_tuples:
        # Validate and process the color tuple
        if len(cyc_color) == 3:  # RGB
            r, g, b = cyc_color
            w = 0  # Default white channel to 0
        elif len(cyc_color) == 4:  # RGBW
            r, g, b, w = cyc_color
        else:
            raise ValueError(f"Invalid color tuple: {cyc_color}. Must be RGB or RGBW.")

        # Append the processed color
        cyc_rgb_colors.append((r, g, b, w))

    # Send the processed colors to the WLED API
    _send_wled_set_request(cyc_rgb_colors)
