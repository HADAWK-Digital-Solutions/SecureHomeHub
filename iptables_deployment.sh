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

# DROP vs REJECT (REJECT sends a rejection response, DROP silently drops packets)
# For added security, uncomment the next line to use REJECT for incoming connections
# iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited

# DDoS Protection (Example: Rate limiting)
# Increasing botnet attacks in home IoT environments are growing as more tech devices get connected
# Limit incoming ICMP packets (adjust rates as needed)
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# Log dropped packets to a log file
iptables -A INPUT -j LOG --log-prefix "Dropped: " --log-level 7 -m limit --limit 5/m

# Save the rules to persist across reboots
iptables-save > /etc/iptables/SecureHomeHubRule.v4

# Optionally, you can reload iptables to apply the rules immediately
# systemctl reload iptables
