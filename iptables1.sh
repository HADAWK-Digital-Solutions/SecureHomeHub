#!/bin/bash

# Flush existing rules and set default policies
iptables -F
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Loopback interface is allowed
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH for remote access (replace 22 with your SSH port if modified)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow specific ports for IoT devices (replace with actual ports)
# Nano Leaf LED's
iptables -A INPUT -p tcp --dport 12345 -j ACCEPT
# Web Camera
iptables -A INPUT -p tcp --dport 56789 -j ACCEPT
# Ecobee Thermostat
iptables -A INPUT -p tcp --dport 67890 -j ACCEPT

# Log dropped packets (optional)
iptables -A INPUT -j LOG --log-prefix "Dropped: "

# Drop all other incoming traffic
iptables -A INPUT -j DROP

# Save the rules to persist across reboots
iptables-save > /etc/iptables/rules.v4

#Replace the placeholders like 12345, 56789, and 67890 with the actual ports your IoT devices use.
#Ensure that you have correctly configured your IoT devices to use these specified ports.
#If you've modified your SSH port from the default 22, make sure to update the SSH rule accordingly.
#This script flushes existing rules, so use it with caution, especially if you have other rules set up.
#After creating and saving this script (e.g., as firewall.sh), make it executable:

bash
Copy code
chmod +x firewall.sh
Then, execute the script as root or with sudo:

bash
Copy code
sudo ./firewall.sh
This script will configure IPTables to enforce a default deny policy while allowing communication on specified ports for your IoT devices. Make sure to test your IoT devices' connectivity after applying the rules to ensure they work as expected. Additionally, consider adding rules for outbound traffic as per your network requirements.




