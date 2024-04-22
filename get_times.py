import requests
import json
from datetime import datetime

lat, lng = 34.0900, -118.036873

# "sunrise": parse_time(sun_times['sunrise']),
#         "sunset": parse_time(sun_times['sunset']),
#         "golden_hour": parse_time(sun_times['golden_hour']),
#         "dusk": parse_time(sun_times['dusk']),
#         "dawn": parse_time(sun_times['dawn']),
#         "day_length": timedelta(seconds=int(sun_times['day_length'].split(':')[0]) * 3600 + int(sun_times['day_length'].split(':')[1]) * 60)

def fetch_sun_times():
    url = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&formatted=0"  # Use formatted=0 for ISO 8601 time
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
    with open('./times.json', 'w') as f:
        json.dump(data, f)

def main():
     # Replace with your location's latitude and longitude
    times = fetch_sun_times()
    save_to_json(times)

if __name__ == "__main__":
    main()
