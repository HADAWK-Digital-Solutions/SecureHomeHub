import os
import subprocess
 
def get_used_ports():
    result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
 
    # Initialize an empty list to store used ports
    used_ports = []
 
    # Iterate through each line of the 'ss' command output
    for line in lines:
        # Split the line into words
        words = line.split()
 
        # Check if the line contains at least 5 words (protocol, local address, local port)
        if len(words) >= 5:
            protocol = words[0]
            local_address = words[4]
 
            # Split the local address by ':' and get the last part as the local port
            local_port = local_address.split(':')[-1]
 
            # Add the local port to the list of used ports
            used_ports.append(local_port)
 
    return used_ports
 
def block_port(port):
    command = ['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(port), '-j', 'DROP']
    subprocess.run(command)
    print(f"Port {port} is now blocked.")
 
def main():
    used_ports = get_used_ports()
    print(f"Used Ports: {', '.join(used_ports)}")
 
    response = input("Do you want to block any ports? (yes/no): ")
    if response.lower() == 'yes':
        port_to_block = int(input("Enter port number to block: "))
        if port_to_block in map(int, used_ports):
            print(f"Port {port_to_block} is currently in use.")
        else:
            block_port(port_to_block)
 
if __name__ == "__main__":
    main()
