import re
import subprocess

def run_nmap(subnet, output_file):
    try:
        # Run the sudo nmap command and redirect the output to the specified file
        subprocess.run(['sudo', 'nmap', '-v', '-R', '-sn', '-PE', '-PS80', '-PU40,125', subnet, nmap_output, '>', output_file], check=True)
        print(f"Nmap scan results have been written to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running nmap: {e}")

def process_nmap_output(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            content = file.read()

        # Use regular expressions to extract relevant information
        pattern = re.compile(r'Nmap scan report for (.+?) \((\d+\.\d+\.\d+\.\d+)\).*?MAC Address: ([\da-fA-F:]+)', re.DOTALL)
        matches = pattern.findall(content)

        # Write formatted information to the output file
        with open(output_file, 'w') as out_file:
            for match in matches:
                name, ip, mac = match
                formatted_output = f'{{"name": "{name}", "ip": "{ip}", "mac": "{mac}"}},'
                out_file.write(formatted_output + '\n')

        print(f"Processed scan results have been written to {output_file}")
    except Exception as e:
        print(f"Error processing Nmap output: {e}")

# Specify the subnet and file paths
subnet = '10.42.0.0/24'
nmap_output = """-oG - | grep "Status: Up" | awk '{print "{\"name\": \""$2"\", \"ip\": \""$2"\", \"mac\":\""system("arp -e | grep "$2" | awk '\''{print $3}'\'")"\"},"}'"""
nmap_output_file = 'devicescan.txt'
formatted_output_file = 'devices_formatted.txt'

# Run the sudo nmap command
run_nmap(subnet, nmap_output_file)

# Process Nmap output
process_nmap_output(nmap_output_file, formatted_output_file)
