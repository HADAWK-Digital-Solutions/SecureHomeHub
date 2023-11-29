import re
import subprocess

def run_nmap(subnet, output_file):
    try:
        # Run the sudo nmap command and redirect the output to the specified file
        subprocess.run(['sudo', 'nmap', '-v', '-R', '-sn', '-PE', '-PS80', '-PU40,125', subnet, '-oN', output_file], check=True)
        print(f"Nmap scan results have been written to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running nmap: {e}")

def process_nmap_output(input_file, output_file):
    try:
        # Python script to parse nmap scan output and generate devices_formatted.txt

        input_file = "devicescan.txt"
        output_file = "devices_formatted.txt"
        devices_list = []  # Initialize the list
        
        with open(input_file, "r") as f:
            lines = f.readlines()
        
        with open(output_file, "w") as f:
            f.write("# IP Address       MAC Address             Status\n")
        
            for line in lines:
                if "Nmap scan report for" in line:
                    ip_address = line.split()[-1]
                    status = "Down"  # Assume the host is down by default
        
                elif "Host is up" in line:
                    status = "Up"
        
                elif "MAC Address:" in line:
                    mac_address = ' '.join(line.split()[2:])

                    
                    # Create a dictionary for each device
                    device_info = {
                        "IP": ip_address,
                        "MAC": mac_address,
                        "Status": status
                    }
            
                    # Append the dictionary to the list
                    devices_list.append(device_info)

with open(output_file, "w") as f:
    # Write each dictionary as a separate line in the output file
    for device_info in devices_list:
        f.write(str(device_info) + "\n")

    except Exception as e:
        print(f"Error processing Nmap output: {e}")

# Specify the subnet and file paths
subnet = '10.42.0.0/24'
nmap_output_file = 'devicescan.txt'
formatted_output_file = 'devices_formatted.txt'

# Run the sudo nmap command
run_nmap(subnet, nmap_output_file)

# Process Nmap output
process_nmap_output(nmap_output_file, formatted_output_file)
