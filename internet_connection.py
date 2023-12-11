import subprocess
import ipaddress

# Function to generate IP addresses in a subnet
def generate_ips(subnet):
    network = ipaddress.ip_network(subnet)
    return [str(ip) for ip in network.hosts()]

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
    ips = generate_ips('10.42.0.0/24')
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
