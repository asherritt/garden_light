import requests

WLED_IP = "192.168.1.169"

def send_wled_preset_request(preset_number):
    """Send API request to WLED to set a preset."""
    url = f"http://{WLED_IP}/json/state"
    payload = {
        "ps": preset_number
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"Preset {preset} activated successfully.")
        else:
            print(f"Failed to activate preset {preset}. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")