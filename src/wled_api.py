import requests
import schedule
from datetime import datetime, timedelta
import globals

WLED_IP = "192.168.1.169"


def set_closest_day_phase_preset(day_phases):
    """Set the WLED preset for the closest day phase to the current time."""
    now = datetime.now()
    closest_phase = None
    smallest_diff = timedelta(days=999999999)  # Effectively a very large timedelta

    for phase in day_phases:
        phase_time = datetime.strptime(phase.time, '%H:%M:%S').replace(
            year=now.year, month=now.month, day=now.day
        )
        time_diff = abs(phase_time - now)
        if time_diff < smallest_diff:
            smallest_diff = time_diff
            closest_phase = phase

    if closest_phase:
        print(f"Setting WLED preset for the closest phase: {closest_phase.name}")
        handle_phase_execution(closest_phase)
        # toggle_relays(closest_phase.lamps_on)


def handle_phase_execution(phase):
    """Handle execution of a specific phase."""
    send_wled_preset_request(preset_number=phase.preset)
    # toggle_relays(phase.lamps_on)
    if phase.name == "midnight2":
        print("Final phase executed. Preparing to reinitialize...")
        globals.final_phase_executed = False

def init_wled(day_phases):
    final_phase_executed = False
    schedule.clear()

    # Schedule WLED requests for each phase
    for phase in day_phases:
        print(f"schedule for {phase.time}")
        schedule.every().day.at(phase.time).do(handle_phase_execution, phase=phase)

    # set current WLED preset   
    set_closest_day_phase_preset(day_phases) 

def send_wled_preset_request(preset_number):
    """Send API request to WLED to set a preset."""
    url = f"http://{WLED_IP}/json/state"
    payload = {
        "ps": preset_number
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Preset {preset_number} activated successfully.")
        else:
            print(f"Failed to activate preset {preset}. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
