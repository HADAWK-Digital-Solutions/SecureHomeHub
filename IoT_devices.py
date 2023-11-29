import subprocess

# Define the subnet you want to scan
subnet = "10.42.0.0/24"

# Define the output file path
output_file = "IoT_devices.txt"

# Run the nmap command using subprocess
try:
    result = subprocess.run(
        f"sudo nmap -v -R -sn -PE -PS80 -PU40,125 {subnet} -oG - | grep 'Status: Up' | awk '{{print \"{{\\\"name\\\": \\\"\"$2\"\\\", \\\"ip\\\": \\\"\"$2\"\\\", \\\"mac\\\":\\\"\"system(\\\"arp -e | grep \"$2\" | awk '{{print $3}}'\\\")\"}}\"}}' > online_devices.txt",
        shell=True,
        capture_output=True,
        text=True,
        check=True
    )
    output = result.stdout
    with open(output_file, "w") as file:
        file.write(output)
    print(f"Scan results have been written to {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error running nmap: {e}")
