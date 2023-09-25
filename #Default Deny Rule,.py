#Default Deny Rule,
import subprocess

# Define the shell commands to set up the firewall rules
commands = [
    "sudo ufw default deny incoming",
    "sudo ufw default deny outgoing",
    "sudo ufw allow ssh",
    "sudo ufw allow 1883/tcp",  # Replace with the appropriate IoT port
    "sudo ufw logging on",
    "sudo ufw enable"
]

# Function to execute shell commands
def execute_commands(commands):
    try:
        for command in commands:
            subprocess.call(command, shell=True)
        print("Firewall rules configured successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    execute_commands(commands)
