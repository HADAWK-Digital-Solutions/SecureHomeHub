import os
import subprocess

def get_used_ports():
    result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    ports = [line.split()[-1].split(":")[-1] for line in lines[1:]]
    return ports

def block_port(port):
    command = ['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(port), '-j', 'DROP']
    subprocess.run(command)

def main():
    used_ports = get_used_ports()
    print(f"Used Ports: {', '.join(used_ports)}")

    response = input("Do you want to block any ports? (yes/no): ")
    if response.lower() == 'yes':
        port_to_block = input("Enter port number to block: ")
        if port_to_block in used_ports:
            print(f"Port {port_to_block} is currently in use.")
        else:
            block_port(port_to_block)
            print(f"Port {port_to_block} is now blocked.")

if __name__ == "__main__":
    main()
