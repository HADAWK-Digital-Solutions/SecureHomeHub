import subprocess
import os
import sys

# Path to the Snort configuration file and the interface on which to listen
SNORT_CONF = '/etc/snort/snort.conf'
INTERFACE = 'eth0'
ALERT_FILE = '/var/log/snort/alert'

def is_snort_running():
    """Check if Snort is currently running."""
    try:
        output = subprocess.check_output(['pgrep', 'snort'])
        return True
    except subprocess.CalledProcessError:
        return False

def start_snort():
    """Start Snort if it is not already running."""
    if not is_snort_running():
        print("Snort is not running. Starting Snort.")
        subprocess.run(['sudo', 'snort', '-q', '-A', 'console', '-c', SNORT_CONF, '-i', INTERFACE])
    else:
        print("Snort is already running.")

def update_rules():
    """Update Snort rules. Assumes PulledPork or similar is installed."""
    print("Updating Snort rules...")
    subprocess.run(['sudo', 'pulledpork.pl', '-c', '/etc/snort/pulledpork.conf'])

def parse_alerts():
    """Parse the Snort alert file and print out alerts."""
    try:
        with open(ALERT_FILE, 'r') as file:
            alerts = file.read()
            print(alerts)
    except IOError:
        print(f"Could not read alert file: {ALERT_FILE}")

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == 'start':
            start_snort()
        elif sys.argv[1] == 'update':
            update_rules()
        elif sys.argv[1] == 'parse':
            parse_alerts()
        else:
            print("Unknown command. Available commands: start, update, parse")
    else:
        print("No command provided. Available commands: start, update, parse")
