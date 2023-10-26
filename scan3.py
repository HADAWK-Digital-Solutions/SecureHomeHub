import nmap

def scan_network(ip_range):
    # Initialize the object
    scanner = nmap.PortScanner()
    
    # Scan the network; adjust the arguments as needed
    scanner.scan(hosts=ip_range, arguments='-O -sP')

    devices_list = []
    
    for ip in scanner.all_hosts():
        device_info = {
            'ip': ip,
            'name': scanner[ip].hostname(),
            'os': '',
            'mac': ''
        }
        
        # Get OS details, if available
        if 'osclass' in scanner[ip]:
            for osclass in scanner[ip]['osclass']:
                if 'osfamily' in osclass and 'osgen' in osclass:
                    device_info['os'] = osclass['osfamily'] + " " + osclass['osgen']
                    break

        # Get MAC details, if available
        if 'addresses' in scanner[ip] and 'mac' in scanner[ip]['addresses']:
            device_info['mac'] = scanner[ip]['addresses']['mac']
        
        devices_list.append(device_info)

    return devices_list

def display_results(devices_list):
    print("IP Address\tMAC Address\t\tDevice Name\tOperating System")
    print("--------------------------------------------------------------------------------------------")
    for device in devices_list:
        print(f"{device['ip']}\t{device['mac']}\t{device['name']}\t{device['os']}")

if __name__ == "__main__":
    ip_range = "192.168.50.1/24"  # adjust this to your network range
    devices_list = scan_network(ip_range)
    display_results(devices_list)
