import os
import subprocess

# Configuration
DOWNLOADS_DIRECTORY = "/path/to/your/downloads/directory"  # Replace with the actual path

def update_and_check():
    """
    Update system packages and check for vulnerabilities.
    """
    try:
        print("Updating system packages...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)
        
        print("Checking for threats using ClamAV...")
        subprocess.run(["sudo", "clamscan", "-r", "--bell", "-i", "/"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during update or scan: {e}")

def check_downloads_for_viruses():
    """
    Check downloaded files for potential viruses.
    """
    try:
        print(f"Checking files in {DOWNLOADS_DIRECTORY} for threats...")
        subprocess.run(["sudo", "clamscan", "-r", "--bell", "-i", DOWNLOADS_DIRECTORY], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during downloads scan: {e}")

if __name__ == "__main__":
    update_and_check()
    check_downloads_for_viruses()