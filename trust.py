from scapy.all import ARP, Ether, srp
import json

def scan_network():
    # IP Address for the destination
    target_ip = "10.42.0.0/24"
    # Create ARP packet
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

def display_devices(devices):
    print("\nDiscovered Devices:")
    for index, device in enumerate(devices):
        print(f"{index+1}: IP = {device['ip']}, MAC = {device['mac']}")

def tag_trusted_devices(devices):
    display_devices(devices)
    trusted_devices = []
    indices = input("\nEnter the numbers of the devices to tag as trusted (separate by commas, e.g., 1,3,5): ")
    for index in indices.split(','):
        try:
            device_index = int(index.strip()) - 1
            if 0 <= device_index < len(devices):
                trusted_devices.append(devices[device_index])
            else:
                print(f"Invalid number: {index}")
        except ValueError:
            print(f"Invalid input: {index}")
    return trusted_devices

def save_trusted_devices(trusted_devices):
    with open('trusted_devices.json', 'w') as file:
        json.dump(trusted_devices, file, indent=4)

def main():
    print("Scanning network...")
    devices = scan_network()
    if not devices:
        print("No devices found.")
        return

    trusted_devices = tag_trusted_devices(devices)
    if trusted_devices:
        save_trusted_devices(trusted_devices)
        print("Trusted devices saved.")
    else:
        print("No devices tagged as trusted.")

if __name__ == "__main__":
    main()
