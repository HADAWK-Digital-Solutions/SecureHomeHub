import scapy.all as scapy
import socket

def get_hostname(ip):
    """Return the hostname for a given IP address."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        # No reverse DNS record found
        return None

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices_list = []
    for element in answered_list:
        device_info = {
            "ip": element[1].psrc,
            "mac": element[1].hwsrc,
            "name": get_hostname(element[1].psrc)
        }
        devices_list.append(device_info)
    return devices_list

def display_result(devices_list):
    print("IP Address\t\tMAC Address\t\tDevice Name")
    print("---------------------------------------------------------------")
    for device in devices_list:
        name = device["name"] if device["name"] else "Unknown"
        print(device["ip"] + "\t\t" + device["mac"] + "\t\t" + name)

if __name__ == "__main__":
    devices_list = scan("10.42.0.0/24")
    display_result(devices_list)
