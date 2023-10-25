##iptables Script revision2##

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

# Define a list of IoT device IP addresses (Obviously replace with the required Ip's within our subnet
# For example the NANO Leaf
IOT_DEVICES=("192.168.1.100" "192.168.1.101" "192.168.1.102" "192.168.1.103")

# Allow specific IoT devices eg. nano leaf
for IP in "${IOT_DEVICES[@]}"; do
    iptables -A INPUT -s "$IP" -j ACCEPT
done

# Brute Force Protection (SSH example, adjust as needed)
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set --name SSH
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 --name SSH -j DROP

# DROP vs REJECT (REJECT sends a rejection response, DROP silently drops packets)
# For added security, consider using REJECT for external connections
################ Uncomment the following line to use REJECT for incoming connections ###############
# iptables -A INPUT -j REJECT --reject-with icmp-host-prohibited

# Shaping and QoS (Example: Limit SSH traffic)
iptables -A INPUT -p tcp --dport 22 -m limit --limit 10/min -j ACCEPT

# Large IP Address Sets (Example: Banned IPs)
# Create an IPSet (ipset) with banned IP addresses
ipset create banned_ips hash:ip
# Add banned IPs to the set (This could be blacklisted IP's)
ipset add banned_ips 1.2.3.4
# Block traffic from banned IPs
iptables -A INPUT -m set --match-set banned_ips src -j DROP

# Routing and Forwarding (Example: Port Forwarding)
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward
# Port Forwarding: Redirect incoming traffic from port 8080 to an IoT device
iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.100:80

# DDoS Protection (Example: Rate limiting)
# Limit incoming ICMP packets (adjust rates as needed)
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# Log dropped packets (optional)
iptables -A INPUT -j LOG --log-prefix "Dropped: "

# Drop all other incoming traffic
iptables -A INPUT -j DROP

# Save the rules to persist across reboots
iptables-save > /etc/iptables/rules.v4
