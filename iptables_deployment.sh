#!/bin/bash

log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    log "Error: This script must be run as root."
    exit 1
fi

log "Flushing existing rules and setting default policies..."
iptables -F
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Loopback interface is allowed
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Define a list of IoT device MAC addresses and their preferred hostnames
declare -A IOT_DEVICES=(
    ["50:02:91:57:0A:DA"]="Tuya Bulb 1"
    ["50:02:91:B0:1D:3E"]="Tuya Bulb 2"
    ["A0:92:08:70:1C:39"]="Tuya Plug"
    ["00:55:DA:52:62:FE"]="Nano Leaf"
    ["78:8C:B5:94:BE:BC"]="Kasa Smart Plug"
    # Add more MAC addresses and hostnames as needed
)

# Allow specific IoT devices by MAC address
for MAC in "${!IOT_DEVICES[@]}"; do
    ebtables -A INPUT -s "$MAC" -j ACCEPT
done

# Brute Force Protection (SSH example, adjust as needed)
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# Allow RDP (Remote Desktop Protocol) traffic on port 3389
# iptables -A INPUT -p tcp --dport 3389 -j ACCEPT

# DROP vs REJECT (REJECT sends a rejection response, DROP silently drops packets)
# For added security, uncomment the next line to use REJECT for incoming connections
# iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited

# DDoS Protection (Example: Rate limiting)
# Limit incoming ICMP packets (adjust rates as needed)
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# Log dropped packets to a log file
log "Logging dropped packets..."
iptables -A INPUT -j LOG --log-prefix "Dropped: " --log-level 7 -m limit --limit 5/m

# Additional Security Rules (Add your custom rules here)

# Rule 1: Allow DNS traffic (UDP and TCP)
iptables -A INPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p tcp --dport 53 -j ACCEPT

# Rule 2: Allow NTP traffic (UDP)
iptables -A INPUT -p udp --dport 123 -j ACCEPT

# Rule 3: Allow ICMP echo replies (ping replies)
iptables -A INPUT -p icmp --icmp-type echo-reply -j ACCEPT

# Rule 4: Allow outbound DNS traffic
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Rule 5: Allow outbound NTP traffic
iptables -A OUTPUT -p udp --dport 123 -j ACCEPT

# Save the rules to persist across reboots
log "Saving iptables rules..."
iptables-save > /etc/iptables/SecureHomeHubRule.v4

# Check if ebtables is installed
if ! command -v ebtables &> /dev/null; then
    log "Error: ebtables is not installed. Please install ebtables and try again."
    exit 1
fi

# Save the ebtables rules
log "Saving ebtables rules..."
ebtables-save > /etc/ebtables/SecureHomeHubRule

# Make sure ebtables service is enabled and started
log "Enabling and starting ebtables service..."
systemctl enable ebtables.service
systemctl start ebtables.service

# Check if Filebeat is installed
if ! dpkg -l | grep -q "filebeat"; then
    log "Installing Filebeat..."
    sudo apt-get update
    sudo apt-get install -y filebeat
fi

# Create a Filebeat configuration for iptables logs
log "Configuring Filebeat for iptables logs..."
cat <<EOF > /etc/filebeat/iptables.yml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/iptables.log  # Update this path to the location of your iptables log file

output.elasticsearch:
  hosts: ["http://localhost:9200"]  # Update this to match your Elasticsearch host and port
EOF

# Start Filebeat with the custom configuration
log "Starting Filebeat..."
filebeat -e -c /etc/filebeat/iptables.yml

log "Setup completed."

