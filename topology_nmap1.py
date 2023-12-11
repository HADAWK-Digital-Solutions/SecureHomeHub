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
        device_info = {}

        with open(input_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            if "Nmap scan report for" in line:
                device_info = {"IP": line.split()[-1]}
            elif "Host is up" in line:
                device_info["Status"] = "Up"
            elif "MAC Address:" in line and device_info.get("Status") == "Up":
                mac_info = line.split(" ", 3)
                device_info["MAC"] = mac_info[2]
                device_info["Device Name"] = mac_info[3].strip("()\n")
                devices_list.append(device_info)
                device_info = {}

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
nmap_output_file = 'list_of_devices.txt'
formatted_output_file = 'list_of_devices.txt'

# Run the sudo nmap command
run_nmap(subnet, nmap_output_file)

# Process Nmap output
process_nmap_output(nmap_output_file, formatted_output_file)

# Display formatted output
display_output(formatted_output_file)

