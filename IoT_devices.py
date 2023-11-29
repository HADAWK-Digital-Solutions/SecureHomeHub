import subprocess

# Define the subnet you want to scan
subnet = "10.42.0.0/24"

# Define the output file path
output_file = "online_devices.txt"

# Run the nmap command using subprocess
try:
    nmap_command = f"sudo nmap -v -R -sn -PE -PS80 -PU40,125 {subnet} -oG -"
    grep_command = "grep 'Status: Up'"
    awk_command = r"awk '{print \"{\"name\": \"\"$2\"\", \"ip\": \"\"$2\"\", \"mac\":\"\"system(\"arp -e | grep \"\"$2\"\" | awk \'{print $3}\'\")\"}\"}'"

    full_command = f"{nmap_command} | {grep_command} | {awk_command} > {output_file}"

    result = subprocess.run(full_command, shell=True, capture_output=True, text=True, check=True)
    
    print(f"Scan results have been written to {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Error running nmap: {e}")
