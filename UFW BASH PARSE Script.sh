#!/bin/bash
# Define the UFW log file path
infile=/var/log/ufw.log

# Loop through each line of the log file
while read line; do
    # Extract the timestamp from the log line (first 15 characters)
    logtime=$(echo $line | cut -c 1-15 ) 

    # Check if the log entry is a UFW BLOCK event
    if [[ $line == *"UFW BLOCK"* ]]; then 
        case $line in
        *"DPT"*)
            # Extract source IP, destination IP, port, and protocol
            ip="${line##*SRC=}"
            ip="${ip%% *}"
            dst="${line##*DST=}"
            dst="${dst%% *}"
            port="${line##*DPT=}"
            port="$dst:${port%% *}"
            proto="${line##*PROTO=}"
            proto="${proto%% *}"
            mac="${line##*MAC=}"
            mac="${mac%% *}"
            
            # Extract and format the MAC address or set to "unknown" if empty
            macAdd="src: $(echo $mac | cut -d ':' -f7,8,9,10,11,12)"  
            if [[ -z "${mac// }" ]]; then 
                macAdd='src: unknown mac addr ' 
            fi 
            
            # Print the BLOCK event in the desired format
            echo "[ $logtime ] [!BLOCK!] [ $macAdd $ip --X $port $proto ]" 
            ;;
        *"DST"*)
            # Extract source IP, destination IP, and protocol
            ip="${line##*SRC=}"
            ip="${ip%% *}"
            dst="${line##*DST=}"
            dst="${dst%% *}"
            proto="${line##*PROTO=}"
            proto="${proto%% *}"
            mac="${line##*MAC=}"
            mac="${mac%% *}"
            
            # Format and print the BLOCK event
            macAdd="[Source MAC: $(echo $mac | cut -d ':' -f7,8,9,10,11,12)]"
            echo "[ $logtime ] $macAdd mDNS:$ip ->X $dst"
            ;;    
        esac
    
    # Check if the log entry is a UFW ALLOW event
    elif [[ $line == *"UFW ALLOW"* ]]; then
        case $line in
        *"DPT"*)
            # Extract source IP, destination IP, port, and protocol
            ip="${line##*SRC=}"
            ip="${ip%% *}"
            dst="${line##*DST=}"
            dst="${dst%% *}"
            port="${line##*DPT=}"
            port="$dst:${port%% *}"
            proto="${line##*PROTO=}"
            proto="${proto%% *}"
            mac="${line##*MAC=}"
            mac="${mac%% *}"
            
            # Extract and format the MAC address or set to a default if empty
            macAdd="src: $(echo $mac | cut -d ':' -f7,8,9,10,11,12)"  
            if [[ "${#macAdd}" -le 17  ]]; then 
                macAdd='src: lo:ca:lh:os:t    ' 
            fi 
            
            # Print the ALLOW event in the desired format
            echo "[ $logtime ] [ allow ] [ $macAdd $ip --> $port $proto ]" 
            ;;   
        esac
    fi
done <  "$infile"
