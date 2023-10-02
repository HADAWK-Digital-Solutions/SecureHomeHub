#!/usr/bin/env python3
import re
import subprocess
import time

# Define the path to the UFW log file
LOG_FILE = "/var/log/ufw.log"

# Define a regular expression pattern to match log entries
LOG_ENTRY_PATTERN = r"^\[(.*?)\] UFW (ALLOW|BLOCK) .* SRC=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*DST=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+).*PROTO=(\w+).*DPT=(\d+)"

# Function to parse and format a log entry
def parse_log_entry(entry):
    match = re.match(LOG_ENTRY_PATTERN, entry)
    if match:
        timestamp, action, src_ip, dst_ip, proto, port = match.groups()
        if action == "ALLOW":
            result = f"[ {timestamp} ] [ ALLOW ] [ src: {src_ip} --> {dst_ip}:{port} {proto} ]"
        else:
            result = f"[ {timestamp} ] [ BLOCK ] [ src: {src_ip} --> {dst_ip}:{port} {proto} ]"
        return result
    return None

# Function to continuously monitor and parse the UFW log
def monitor_ufw_log(interval_seconds):
    try:
        previous_log = ""

        while True:
            # Read the current UFW log
            current_log = subprocess.check_output(["cat", LOG_FILE], text=True)

            # Find new log entries by comparing with the previous log
            new_entries = current_log[len(previous_log) :].strip().split("\n")

            for entry in new_entries:
                parsed_entry = parse_log_entry(entry)
                if parsed_entry:
                    print(parsed_entry)

            # Update the previous log with the current log
            previous_log = current_log

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    try:
        # Set the monitoring interval (in seconds)
        monitoring_interval = 2

        print("UFW Log Parser")
        print("Press Ctrl+C to stop monitoring.")
        monitor_ufw_log(monitoring_interval)

    except KeyboardInterrupt:
        print("Monitoring stopped.")
