import requests

# Configuration
GATEWAY_URL = "10.42.0.0/24"  # replace with your gateway's IP and port
LIST_DEVICES_ENDPOINT = "/list_devices"  # replace with the appropriate endpoint

def list_connected_devices():
    """
    Sends a command to the gateway to list all connected IoT devices.
    """
    try:
        response = requests.get(GATEWAY_URL + LIST_DEVICES_ENDPOINT)
        
        if response.status_code == 200:
            devices = response.json()
            for device in devices:
                print(f"Device ID: {device['id']}, Device Name: {device['name']}")
        else:
            print(f"Failed to get list of devices. Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_connected_devices()
