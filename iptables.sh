#!/bin/bash

# Function to add rules for specific services
add_service_rule() {
    local service_port="$1"
    iptables -A INPUT -i wlan0 -p tcp --dport "$service_port" -j ACCEPT
    iptables -A FORWARD -i wlan0 -o eth0 -p tcp --dport "$service_port" -j ACCEPT
}

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
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow communication between NAT (192.168.50.206) and VLAN (10.42.0.1/24)
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPT

# Allow specific IoT devices by MAC address
declare -A IOT_DEVICES=(
    ["50:02:91:57:0A:DA"]="Tuya Bulb 1"
    ["50:02:91:B0:1D:3E"]="Tuya Bulb 2"
    ["A0:92:08:70:1C:39"]="Tuya Plug"
    ["00:55:DA:52:62:FE"]="Nano Leaf"
    ["78:8C:B5:94:BE:BC"]="Kasa Smart Plug"
    ["48:02:2A:47:AD:4D"]="Netwave IP Camera"
    # Add more MAC addresses and hostnames as needed
)

for MAC in "${!IOT_DEVICES[@]}"; do
    iptables -A FORWARD -m mac --mac-source "$MAC" -j ACCEPT
done

# Brute Force Protection (SSH example, adjust as needed)
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# DDoS Protection (Example: Rate limiting)
# Limit incoming ICMP packets (adjust rates as needed)
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# Add service-specific rules here:
# Example: Allow MQTT traffic on port 1883
add_service_rule 1883

# Log dropped packets to a log file
iptables -A INPUT -j LOG --log-prefix "Dropped: " --log-level 7 -m limit --limit 5/m

# Save the rules to persist across reboots
iptables-save > /etc/iptables/SecureHomeHubRule.v4
