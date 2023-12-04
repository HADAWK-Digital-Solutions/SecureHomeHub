import subprocess
import re
from collections import defaultdict
import logging

# Initialize logging
logging.basicConfig(filename='network_scan.log', level=logging.INFO)

class NetworkScanner:
    def __init__(self, subnet, threshold_ports=100):
        self.subnet = subnet
        self.port_scans = defaultdict(int)
        self.threshold_ports = threshold_ports

    def run_nmap_scan(self):
        try:
            result = subprocess.check_output(['nmap', '-sS', '-T4', self.subnet])
            return result.decode()
        except subprocess.CalledProcessError as e:
            logging.error(f"Error during nmap scan: {e}")
            return ""

    def parse_nmap_output(self, output):
        for line in output.split('\n'):
            if 'Nmap scan report for' in line:
                ip_address = line.split()[-1]
            elif '/tcp' in line:
                self.port_scans[ip_address] += 1

    def analyze_scans(self):
        for host, ports_scanned in self.port_scans.items():
            if ports_scanned > self.threshold_ports:
                alert_msg = f"[!] Potential port scan detected from {host}"
                print(alert_msg)
                logging.info(alert_msg)

    def display_results(self):
        for host, ports in self.port_scans.items():
            print(f"Host: {host}, Ports Scanned: {ports}")

def main():
    subnet = "10.42.0.0/24"  # Define your subnet
    scanner = NetworkScanner(subnet)
    print("Starting network scan... (This may take a while)")
    nmap_output = scanner.run_nmap_scan()
    scanner.parse_nmap_output(nmap_output)
    scanner.analyze_scans()
    scanner.display_results()

if __name__ == "__main__":
    main()
