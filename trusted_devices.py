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

def tag_trusted_devices(devices):
    trusted_devices = []
    for device in devices:
        print(f"Device: IP = {device['ip']}, MAC = {device['mac']}")
        tag = input("Tag this device as trusted? (yes/no): ")
        if tag.lower() == 'yes':
            trusted_devices.append(device)
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
    save_trusted_devices(trusted_devices)
    print("Trusted devices saved.")

if __name__ == "__main__":
    main()