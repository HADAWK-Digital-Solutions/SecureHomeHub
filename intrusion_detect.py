from scapy.all import sniff, IP, ICMP, TCP, UDP
from collections import defaultdict

class SimpleIDS:
    def __init__(self):
        # Stores IP addresses from which we've seen ICMP requests
        self.icmp_sources = defaultdict(int)
        # Stores destination ports for TCP/UDP packets for each IP
        self.port_scans = defaultdict(set)

    def analyze_packet(self, packet):
        if packet.haslayer(IP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            
            if packet.haslayer(ICMP):
                self.icmp_sources[ip_src] += 1
                if self.icmp_sources[ip_src] > 10:  # Arbitrary threshold
                    print(f"[!] Possible ping sweep attack from {ip_src}")
                    self.icmp_sources[ip_src] = 0  # Reset count to avoid repetitive alerts

            elif packet.haslayer(TCP) or packet.haslayer(UDP):
                dst_port = packet[TCP].dport if packet.haslayer(TCP) else packet[UDP].dport
                self.port_scans[ip_src].add(dst_port)
                if len(self.port_scans[ip_src]) > 50:  # Arbitrary threshold
                    print(f"[!] Possible port scan attack from {ip_src}")
                    self.port_scans[ip_src].clear()  # Clear set to avoid repetitive alerts

            else:
                print(f"Packet: {packet.summary()}")

def main():
    ids = SimpleIDS()
    print("Starting packet capture... (Press Ctrl+C to stop)")
    sniff(prn=ids.analyze_packet, store=0)

if __name__ == "__main__":
    main()
