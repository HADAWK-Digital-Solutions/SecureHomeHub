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

# Define a list of IoT device IP addresses
IOT_DEVICES=("192.168.1.100" "192.168.1.101" "192.168.1.102" "192.168.1.103")

# Allow specific IoT devices
for IP in "${IOT_DEVICES[@]}"; do
    iptables -A INPUT -s "$IP" -j ACCEPT
done

# Brute Force Protection (SSH example)
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j LOG --log-prefix "SSH Failed Login: "
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# Port Scanning Detection
iptables -A INPUT -m recent --name portscan --rcheck --seconds 60 --hitcount 10 -j LOG --log-prefix "Port Scan Detected: "
iptables -A INPUT -m recent --name portscan --set -j DROP

# DNS Traffic Logging
iptables -A INPUT -p udp --sport 53 -j LOG --log-prefix "DNS Traffic: "

# HTTP/HTTPS Traffic Logging
iptables -A INPUT -p tcp --dport 80 -j LOG --log-prefix "HTTP Traffic: "
iptables -A INPUT -p tcp --dport 443 -j LOG --log-prefix "HTTPS Traffic: "

# ICMP (Ping) Logging
iptables -A INPUT -p icmp -j LOG --log-prefix "ICMP Traffic: "

# Custom Application Logging
iptables -A INPUT -p tcp --dport 12345 -j LOG --log-prefix "Custom App Traffic: "

# Log dropped packets (optional)
iptables -A INPUT -j LOG --log-prefix "Dropped: "

# Drop all other incoming traffic
iptables -A INPUT -j DROP

# Save the rules to persist across reboots
iptables-save > /etc/iptables/rules.v4
