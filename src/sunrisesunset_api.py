from typing import List
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass
import time
from model import Phase

# Location for sun times API
LAT, LNG = 34.0900, -118.036873

def _fetch_sun_times():
    """Fetch sun times from the API."""
    print("Fetching sun times...")
    url = f"https://api.sunrisesunset.io/json?lat={LAT}&lng={LNG}&time_format=24"
    response = requests.get(url)
    data = response.json()
    print("api.sunrisesunset.io response")
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
        "eod": "23:59:59",
    }

def _minutes_between_times(time1, time2):
    """
    Calculate the positive difference in minutes between two times,
    accounting for crossing midnight.
    :param time1: First time as a string in 'HH:MM:SS' format.
    :param time2: Second time as a string in 'HH:MM:SS' format.
    :return: Difference in minutes as a positive integer.
    """
    fmt = '%H:%M:%S'
    t1 = datetime.strptime(time1, fmt)
    t2 = datetime.strptime(time2, fmt)

    # If t2 is earlier than t1, assume t2 is on the next day
    if t2 < t1:
        t2 += timedelta(days=1)

    delta = t2 - t1
    return int(delta.total_seconds() / 60)

def _generate_phases(sun_times: dict) -> List[Phase]:
    """
    Generate a list of Phase models from sun_times.
    :param sun_times: Dictionary of phase names and their corresponding times.
    :return: List of Phase models with calculated seconds between phases.
    """
    # Convert sun_times into a list of Phase models
    phases = []
    keys = list(sun_times.keys())
    
    for i, key in enumerate(keys):
        time = sun_times[key]
        # Calculate seconds to the next phase
        next_key = keys[(i + 1) % len(keys)]
        next_time = sun_times[next_key]
        total_seconds = _minutes_between_times(time, next_time)
        
        # Create a Phase instance and add it to the list
        phases.append(Phase(name=key, start_time=time, seconds=total_seconds))
    
    return phases


def get_phases():
    sun_times = _fetch_sun_times()
    return _generate_phases(sun_times)

  