#!/bin/bash

# Deny all in/out by default
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow loopback interface
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (port 22) from any IP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT

# Allow RDP (port 3389) from any IP
iptables -A INPUT -p tcp --dport 3389 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 3389 -m conntrack --ctstate ESTABLISHED -j ACCEPT

# Allow specific IoT devices by MAC address
#Tuya Bulb 1
iptables -A INPUT -m mac --mac-source 50:02:91:57:0A:DA -j ACCEPT
#Tuya Bulb 2
iptables -A INPUT -m mac --mac-source 50:02:91:B0:1D:3E -j ACCEPT
#Tuya Plug
iptables -A INPUT -m mac --mac-source 50:A0:92:08:70:1C:39 -j ACCEPT
#Nano Leaf
iptables -A INPUT -m mac --mac-source 50:00:55:DA:52:62:FE -j ACCEPT
#Kasa Smart Plug
iptables -A INPUT -m mac --mac-source 50:78:8C:B5:94:BE:BC -j ACCEPT

# ... and other MAC address rules

# Brute Force Protection for SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# DDoS Protection: Rate limiting ICMP
iptables -A OUTPUT -p icmp -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p icmp -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# Allow DNS traffic
iptables -A OUTPUT -p udp --dport 53 -d 192.168.50.1 -j ACCEPT
iptables -A INPUT -p udp --sport 53 -s 192.168.50.1 -m conntrack --ctstate ESTABLISHED -j ACCEPT

# Allow HTTP (80) and HTTPS (443) for web browsing
iptables -A OUTPUT -p tcp -m multiport --dports 80,443 -j ACCEPT
iptables -A INPUT -p tcp -m multiport --sports 80,443 -m conntrack --ctstate ESTABLISHED -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "Dropped: " --log-level 7 -m limit --limit 5/m

# Save the rules
iptables-save > /etc/iptables/SecureHomeHubRule.v4
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

