import nmap
import socket

def get_hostname(ip):
    """Return the hostname for a given IP address."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        # No reverse DNS record found
        return None

def scan(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')

    devices_list = []
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:  # Only include hosts with a MAC address
            device_info = {
                'ip': host,
                'mac': nm[host]['addresses']['mac'],
                'name': get_hostname(host)
            }
            devices_list.append(device_info)

    return devices_list

def display_result(devices_list):
    print("IP Address\t\tMAC Address\t\tDevice Name")
    print("---------------------------------------------------------------")
    for device in devices_list:
        name = device['name'] if device['name'] else 'Unknown'
        print(device['ip'] + "\t\t" + device['mac'] + "\t\t" + name)

def save_to_file(devices_list, filename="Topology.txt"):
    # Save the scan results to a text file.
    with open(filename, "w") as file:
        file.write("IP Address\t\tMAC Address\t\tDevice Name\n")
        file.write("---------------------------------------------------------------\n")
        for device in devices_list:
            name = device['name'] if device['name'] else 'Unknown'
            file.write(device['ip'] + "\t\t" + device['mac'] + "\t\t" + name + "\n")

if __name__ == "__main__":
    devices_list = scan("10.42.0.0/24")
    display_result(devices_list)
    save_to_file(devices_list)
