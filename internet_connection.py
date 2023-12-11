import subprocess
import ipaddress

# Function to generate IP addresses in a subnet
def generate_ips(subnet):
    network = ipaddress.ip_network(subnet)
    return [str(ip) for ip in network.hosts()]

# Function to quickly check if IP is up
def is_ip_up(ip):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", ip], universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

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
        if is_ip_up(ip):
            latency = ping_ip(ip)
            if latency is not None:
                if latency < 20:
                    print(f"IP: {ip} is up and meets the standard with latency: {latency}ms")
                else:
                    print(f"IP: {ip} is up but does not meet the standard with latency: {latency}ms")
        else:
            print(f"IP: {ip} is down or not responding.")

if __name__ == "__main__":
    main()
