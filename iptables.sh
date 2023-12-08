#!/bin/bash

# Deny all in/out by default
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# Allow loopback interface
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# Allow established and related connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH/RDPon our port
iptables -A INPUT -p tcp --dport 49646 -j ACCEPT
iptables -A INPUT -p tcp --dport 49648 -j ACCEPT

# Blocking default SSH (port 22), RDP (port 3389), and FTP (port 21)
iptables -A INPUT -p tcp --dport 22 -j DROP
iptables -A INPUT -p tcp --dport 3389 -j DROP
iptables -A INPUT -p tcp --dport 21 -j DROP

#Blocking Ports
iptables -A INPUT -p tcp --dport 23 -j DROP   # Block Telnet
iptables -A INPUT -p tcp --dport 25 -j DROP   # Block SMTP
iptables -A INPUT -p udp --dport 161 -j DROP  # Block SNMP
iptables -A INPUT -p udp --dport 162 -j DROP  # Block SNMP Trap
iptables -A INPUT -p tcp --dport 135 -j DROP  # Block RPC
iptables -A INPUT -p udp --dport 137 -j DROP  # Block NetBIOS
iptables -A INPUT -p udp --dport 138 -j DROP  # Block NetBIOS
iptables -A INPUT -p tcp --dport 139 -j DROP  # Block NetBIOS
iptables -A INPUT -p tcp --dport 445 -j DROP  # Block SMB
iptables -A INPUT -p tcp --dport 1433 -j DROP # Block Microsoft SQL Server
iptables -A INPUT -p tcp --dport 1434 -j DROP # Block Microsoft SQL Monitor
iptables -A INPUT -p tcp --dport 69 -j DROP   # Block TFTP
iptables -A INPUT -p udp --dport 123 -j DROP  # Block NTP

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
# Additional MAC address rules

# Brute Force Protection for SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# Brute Force Protection for our SSH port
iptables -A INPUT -p tcp --dport 49646 -m conntrack --ctstate NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 49646 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# SYN Flood Protection
iptables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP

# ICMP Protection
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# Blacklist IP addresses
# iptables -A INPUT -s [MALICIOUS_IP] -j DROP
# iptables -A OUTPUT -d [MALICIOUS_IP] -j DROP

# Limit the Number of Parallel Connections per IP
iptables -A INPUT -p tcp -m connlimit --connlimit-above 50 -j DROP

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "Dropped: " --log-level 7 -m limit --limit 5/m

# Save the rules
iptables-save > /etc/iptables/rules.v4
