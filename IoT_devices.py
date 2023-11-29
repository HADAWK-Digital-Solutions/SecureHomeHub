import subprocess
import re

# Define the subnet you want to scan
subnet = "10.42.0.0/24"

# Define the output file path
output_file = "IoT_devices.txt"

# Run the nmap command using subprocess
try:
    result = subprocess.run(["sudo", "nmap", "-sn", subnet], capture_output=True, text=True, check=True)
    output = result.stdout

    # Use regular expression to extract device name, IP, and MAC address for online hosts
    pattern = re.compile(r'Nmap scan report for (.+?) \((\d+\.\d+\.\d+\.\d+)\)\s*MAC Address: ((?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))', re.MULTILINE)
    matches = pattern.findall(output)

    # Write the extracted information to the output file
    with open(output_file, "w") as file:
        for match in matches:
            file.write(f"Device Name: {match[0]}\n")
            file.write(f"IP Address: {match[1]}\n")
            file.write(f"MAC Address: {match[2]}\n")
            file.write("\n")

    print(f"Scan results have been written to {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error running nmap: {e}")
