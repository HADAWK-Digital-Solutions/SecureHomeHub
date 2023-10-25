##Adding several devices within our Net##
#!/bin/bash

# List of IoT device IP addresses(This would be expected in home full of wireless communication)
IOT_DEVICES=(
    10.42.0.2
    10.42.0.3
    10.42.0.4
    10.42.0.5
    10.42.0.6
    10.42.0.7
    10.42.0.8
    10.42.0.9
    10.42.0.10
    10.42.0.11
)

# General rules
# Allow specific ports for IoT devices
for IP in "${IOT_DEVICES[@]}"; do
    iptables -A INPUT -s "$IP" -j ACCEPT
done

# Log dropped packets (optional)
iptables -A INPUT -j LOG --log-prefix "Dropped: "

# Drop all other incoming traffic
iptables -A INPUT -j DROP

# Save the rules to persist across reboots
iptables-save > /etc/iptables/ListIoTRule.v4
