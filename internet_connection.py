import subprocess
import re

# Function to get IP addresses from ARP table
def get_ip_addresses():
    arp_output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
    ip_addresses = re.findall(r"\((.*?)\)", arp_output)
    return ip_addresses

# Function to ping IP and return latency
def ping_ip(ip):
    try:
        output = subprocess.check_output(["ping", "-c", "1", ip], universal_newlines=True)
        for line in output.split("\n"):
            if "time=" in line:
                latency = float(line.split("time=")[1].split(" ")[0])
                return latency
    except subprocess.CalledProcessError:
        return None

# Main function
def main():
    ips = get_ip_addresses()
    for ip in ips:
        latency = ping_ip(ip)
        if latency is not None:
            if latency < 20:
                print(f"IP: {ip} meets the standard with latency: {latency}ms")
            else:
                print(f"IP: {ip} does not meet the standard with latency: {latency}ms")
        else:
            print(f"IP: {ip} could not be pinged or is unreachable.")

if __name__ == "__main__":
    main()
