#!/bin/bash

## Dropping traffic from reserved and private IP address ranges, as well as loopback traffic ##
# Array of subnets to block
_subnets=("224.0.0.0/3" "169.254.0.0/16" "172.16.0.0/12" "192.0.2.0/24" "192.168.0.0/16" "10.0.0.0/8" "0.0.0.0/8" "240.0.0.0/5")

# Loop through each subnet and drop traffic from it
for _sub in "${_subnets[@]}" ; do
  iptables -t mangle -A PREROUTING -s "$_sub" -j DROP
done

# Drop loopback traffic except for the local interface (lo)
iptables -t mangle -A PREROUTING -s 127.0.0.0/8 ! -i lo -j DROP
