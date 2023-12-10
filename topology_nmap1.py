import subprocess

def run_nmap(subnet, output_file):
    try:
        # Run the sudo nmap command and redirect the output to the specified file
        subprocess.run(['sudo', 'nmap', '-v', '-sn', subnet, '-oN', output_file], check=True)
        print(f"Nmap scan results have been written to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running nmap: {e}")

def process_nmap_output(input_file, output_file):
    try:
        devices_list = []

        with open(input_file, "r") as f:
            lines = f.readlines()

        device_info = {}
        for line in lines:
            if "Nmap scan report for" in line:
                if device_info:
                    devices_list.append(device_info)
                device_info = {"IP": line.split()[-1]}
            elif "MAC Address:" in line:
                mac_info = line.split(" ", 3)
                device_info["MAC"] = mac_info[2]
                device_info["Device Name"] = mac_info[3].strip("()\n")

        if device_info:
            devices_list.append(device_info)

        with open(output_file, "w") as f:
            for device in devices_list:
                f.write(f"Device Name: {device.get('Device Name', 'N/A')}\n")
                f.write(f"MAC Address: {device.get('MAC', 'N/A')}\n")
                f.write(f"IP Address: {device['IP']}\n")
                f.write("\n")

    except Exception as e:
        print(f"Error processing Nmap output: {e}")

def display_output(file_path):
    try:
        with open(file_path, "r") as file:
            print(file.read())
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

# Specify the subnet and file paths
subnet = '10.42.0.0/24'
nmap_output_file = 'devicescan.txt'
formatted_output_file = 'devices_formatted.txt'

# Run the sudo nmap command
run_nmap(subnet, nmap_output_file)

# Process Nmap output
process_nmap_output(nmap_output_file, formatted_output_file)

# Display formatted output
display_output(formatted_output_file)
