from scapy.all import sniff, IP, ICMP, TCP, UDP
from collections import defaultdict
import time
import logging

class ImprovedIDS:
    def __init__(self):
        self.icmp_sources = defaultdict(int)
        self.port_scans = defaultdict(set)
        self.threshold_icmp = 10  # initial threshold
        self.threshold_ports = 50  # initial threshold
        logging.basicConfig(filename='alerts.log', level=logging.INFO)
        self.start_time = time.time()

    def dynamic_threshold_adjustment(self):
        # Adjust thresholds dynamically based on time or other criteria
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 60:  # adjust thresholds every minute (60 seconds)
            self.threshold_icmp += 5  # increment by a fixed value or a percentage
            self.threshold_ports += 10  # adjust as needed
            self.start_time = time.time()

    def analyze_packet(self, packet):
        self.dynamic_threshold_adjustment()
        
        if packet.haslayer(IP):
            ip_src = packet[IP].src

            if packet.haslayer(ICMP):
                self.icmp_sources[ip_src] += 1
                if self.icmp_sources[ip_src] > self.threshold_icmp:
                    alert_msg = f"[!] Possible ping sweep attack from {ip_src}"
                    print(alert_msg)
                    logging.info(alert_msg)
                    self.icmp_sources[ip_src] = 0

            elif packet.haslayer(TCP) or packet.haslayer(UDP):
                dst_port = packet[TCP].dport if packet.haslayer(TCP) else packet[UDP].dport
                self.port_scans[ip_src].add(dst_port)
                if len(self.port_scans[ip_src]) > self.threshold_ports:
                    alert_msg = f"[!] Possible port scan attack from {ip_src}"
                    print(alert_msg)
                    logging.info(alert_msg)
                    self.port_scans[ip_src].clear()

            else:
                print(f"Packet: {packet.summary()}")

def main():
    ids = ImprovedIDS()
    print("Starting packet capture for 10.42.0.0/24 network... (Press Ctrl+C to stop)")
    try:
        # Add a filter for the 10.42.0.0/24 network
        sniff(prn=ids.analyze_packet, store=0, filter="net 10.42.0.0/24")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
