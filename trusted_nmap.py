import subprocess
import json
import re

def scan_network(subnet):
    try:
        # Run nmap, scanning for IP and MAC addresses
        result = subprocess.check_output(['nmap', '-sn', subnet])

        # Decode the result from bytes to string
        result = result.decode('utf-8')

        devices = parse_nmap_output(result)
        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error during scan: {e}")
        return []
    except FileNotFoundError:
        print("nmap not found. Please install nmap.")
        return []

def parse_nmap_output(output):
    # Regular expressions to match IP and MAC addresses
    ip_regex = r'Nmap scan report for ([\d\.]+)'
    mac_regex = r'MAC Address: ([\w:]+)'

    devices = []
    current_ip = None

    for line in output.split('\n'):
        ip_match = re.search(ip_regex, line)
        mac_match = re.search(mac_regex, line)

        if ip_match:
            current_ip = ip_match.group(1)
        elif mac_match and current_ip:
            devices.append({'ip': current_ip, 'mac': mac_match.group(1)})
            current_ip = None

    return devices

def main():
    subnet = "10.42.0.0/24"  # Change to your target subnet
    devices = scan_network(subnet)
    print(json.dumps(devices, indent=4))

if __name__ == "__main__":
    main()
