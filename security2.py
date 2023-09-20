#This script will check packets, unused ports in the routers, protocols and ensure the network is safe.

import os
from scapy.all import rdpcap, IP, TCP, UDP

# Constants
PCAP_FILE = "output.pcap"
ALL_PORTS = set(range(1, 65536))


def capture_traffic(filename, duration=60):
    print(f"Capturing traffic for {duration} seconds...")
    os.system(f"sudo dumpcap -w {filename} -a duration:{duration}")
    print(f"Traffic saved to {filename}")


def analyze_traffic(filename):
    packets = rdpcap(filename)

    observed_ports = set()
    traffic_summary = {}

    for packet in packets:
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

            if packet.haslayer(TCP):
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                observed_ports.add(dst_port)
                protocol = "TCP"
            elif packet.haslayer(UDP):
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                observed_ports.add(dst_port)
                protocol = "UDP"
            else:
                continue

            key = (src_ip, dst_ip, protocol)
            if key not in traffic_summary:
                traffic_summary[key] = set()
            traffic_summary[key].add(dst_port)

    return observed_ports, traffic_summary


def display_traffic(traffic_summary):
    for (src_ip, dst_ip, protocol), ports in traffic_summary.items():
        ports_str = ", ".join(map(str, sorted(ports)))
        print(f"{protocol} Traffic from {src_ip} to {dst_ip} on ports: {ports_str}")


def display_unused_ports(observed_ports):
    unused_ports = ALL_PORTS - observed_ports
    if unused_ports:
        print(f"Unobserved (potentially unused) ports: {', '.join(map(str, sorted(unused_ports)))}")
    else:
        print("All ports were observed in the capture!")


def check_security_concerns(traffic_summary):
    # Placeholder for potential security checks. This can be far more sophisticated.
    for (src_ip, dst_ip, protocol), ports in traffic_summary.items():
        if 22 in ports:  # Check for SSH as an example
            print(f"Potential security concern: {protocol} traffic observed on port 22 (SSH) from {src_ip} to {dst_ip}")


if __name__ == "__main__":
    capture_traffic(PCAP_FILE)
    observed_ports, traffic_summary = analyze_traffic(PCAP_FILE)
    display_traffic(traffic_summary)
    display_unused_ports(observed_ports)
    check_security_concerns(traffic_summary)
