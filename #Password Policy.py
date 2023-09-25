#Password Policy
import re
import subprocess

# Define the minimum password length
MIN_LENGTH = 8

# Define the regular expression pattern for a strong password
# This pattern enforces at least one uppercase letter, one lowercase letter, one digit, and a minimum length
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{%d,}$" % MIN_LENGTH

# Function to check if a password meets the policy
def is_password_strong(password):
    return bool(re.match(PASSWORD_PATTERN, password))

# Function to enforce the password policy for a user
def enforce_password_policy(username):
    try:
        # Get the user's current password hash
        password_hash = subprocess.check_output(["sudo", "grep", "-E", "^%s:" % username, "/etc/shadow"], universal_newlines=True)
        password_hash = password_hash.strip().split(":")[1]

        # Prompt the user to change their password if it doesn't meet the policy
        while True:
            new_password = input("Enter a new password: ")
            if is_password_strong(new_password):
                break
            else:
                print("Password does not meet the policy requirements. Please try again.")

        # Set the new password
        subprocess.call(["sudo", "passwd", username], input=new_password.encode("utf-8"))

        print("Password successfully changed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    username = input("Enter the username: ")
    enforce_password_policy(username)
