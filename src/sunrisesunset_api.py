import requests
from datetime import datetime, timedelta
from dataclasses import dataclass
import time
from color import init_color_steps
from wled_api import init_wled
import globals

def fetch_sun_times():
    """Fetch sun times from the API."""
    print("Fetching sun times...")
    url = f"https://api.sunrisesunset.io/json?lat={LAT}&lng={LNG}&time_format=24"
    response = requests.get(url)
    data = response.json()
    print(data)
    return {
        "midnight": "00:00:00",
        "first_light": data['results']['first_light'],
        "dawn": data['results']['dawn'],
        "sunrise": data['results']['sunrise'],
        "solar_noon": data['results']['solar_noon'],
        "golden_hour": data['results']['golden_hour'],
        "sunset": data['results']['sunset'],
        "dusk": data['results']['dusk'],
        "last_light": data['results']['last_light'],
       