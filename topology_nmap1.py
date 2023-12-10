import subprocess
import re

def scan_network(subnet):
    try:
        result = subprocess.check_output(['nmap', '-sn', '-sL', subnet])
        result = result.decode('utf-8')
        return parse_nmap_output(result)
    except subprocess.CalledProcessError as e:
        print(f"Error during scan: {e}")
        return []
    except FileNotFoundError:
        print("nmap not found. Please install nmap.")
        return []

def parse_nmap_output(output):
    ip_regex = r'Nmap scan report for ([\w.-]+) \(([\d\.]+)\)'
    mac_regex = r'MAC Address: ([\w:]+) \(([^)]+)\)'
    devices = []
    current_device = {}

    for line in output.split('\n'):
        ip_match = re.search(ip_regex, line)
        mac_match = re.search(mac_regex, line)

        if ip_match:
            current_device = {'name': ip_match.group(1), 'ip': ip_match.group(2)}
        elif mac_match and 'ip' in current_device:
            current_device['mac'] = mac_match.group(1)
            current_device['vendor'] = mac_match.group(2)
            devices.append(current_device)
            current_device = {}

    return devices

def save_devices_to_file(devices, filename):
    with open(filename, 'w') as file:
        for device in devices:
            file.write(f"Name: {device.get('name', 'N/A')}, IP: {device.get('ip', 'N/A')}, MAC: {device.get('mac', 'N/A')}, Vendor: {device.get('vendor', 'N/A')}\n")

def main():
    subnet = "10.42.0.0/24"  # Change to your target subnet
    devices = scan_network(subnet)
    if devices:
        save_devices_to_file(devices, 'connected_devices.txt')
        print("Connected devices saved to connected_devices.txt")
    else:
        print("No devices found.")

if __name__ == "__main__":
    main()
