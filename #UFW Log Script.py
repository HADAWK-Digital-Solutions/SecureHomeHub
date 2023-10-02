#UFW Monitor Log Script

import subprocess
import os
import time
import sys

# Define the path to the firewall rule configuration file
FIREWALL_RULES_FILE = "/etc/ufw/user.rules"

# Define the path for the audit log file
AUDIT_LOG_FILE = "/var/log/firewall_audit.log"

# Function to check for changes in the firewall rules
def check_firewall_rules():
    try:
        # Read the current firewall rule configuration
        with open(FIREWALL_RULES_FILE, "r") as f:
            current_rules = f.read()

        # Check if the audit log file exists, create it if not
        if not os.path.exists(AUDIT_LOG_FILE):
            with open(AUDIT_LOG_FILE, "w") as f:
                f.write("Firewall Rule Audit Log\n")

        # Read the previous rules snapshot from the audit log
        with open(AUDIT_LOG_FILE, "r") as f:
            previous_rules = f.read()

        # Compare the current rules with the previous snapshot
        if current_rules != previous_rules:
            # Rules have changed, log the event
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] Firewall rules have been modified.\n"

            # Log the change in the audit log file
            with open(AUDIT_LOG_FILE, "a") as f:
                f.write(log_entry)

            # Optionally, send an email or trigger an alert to administrators here
            print("Firewall rules have been modified. Check the audit log for details.")
        else:
            print("Firewall rules are unchanged.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to continuously monitor the firewall rules
def monitor_firewall_rules(interval_seconds):
    try:
        while True:
            check_firewall_rules()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python firewall_audit.py <monitoring_interval_seconds>")
        sys.exit(1)

    monitoring_interval = int(sys.argv[1])

    print("Firewall Rule Audit and Monitoring Script")
    print("Press Ctrl+C to stop monitoring.")
    monitor_firewall_rules(monitoring_interval)
