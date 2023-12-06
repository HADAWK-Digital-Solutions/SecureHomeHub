#A function for the PythonGUI.pyw

def compare_files(self):
    # Paths to the files and scripts
    devices_formatted_path = "devices_formatted.txt"
    iot_devices_script_path = os.path.join(os.getcwd(), 'IoT_devices.py')

    # Initial check for the existence of devices_formatted.txt
    original_exists = os.path.exists(devices_formatted_path)
    
    # Store the original content
    original_content = ""
    if original_exists:
        with open(devices_formatted_path, 'r') as file:
            original_content = file.read()

    # Run the IoT_devices.py script
    subprocess.run(['python3', iot_devices_script_path])

    # Read the updated content
    updated_content = ""
    if os.path.exists(devices_formatted_path):
        with open(devices_formatted_path, 'r') as file:
            updated_content = file.read()

    # Compare original and updated content
    result_text = ""
    if original_content == updated_content:
        result_text = "No changes were detected in devices_formatted.txt."
    elif not original_exists:
        result_text = "The original file did not exist. New content has been created."
    else:
        # Perform a detailed comparison
        differences = []
        original_lines = original_content.splitlines()
        updated_lines = updated_content.splitlines()

        for line_number, (orig_line, updated_line) in enumerate(zip(original_lines, updated_lines), start=1):
            if orig_line != updated_line:
                differences.append(f"Line {line_number}:\n  Original: {orig_line}\n  Updated : {updated_line}")

        # Additional lines in updated content
        for extra_line in updated_lines[len(original_lines):]:
            line_number += 1
            differences.append(f"Line {line_number} (Updated): {extra_line}")

        # Additional lines in original content
        for extra_line in original_lines[len(updated_lines):]:
            line_number += 1
            differences.append(f"Line {line_number} (Original): {extra_line}")

        result_text = "\n".join(differences) if differences else "Files are identical but updated."

    # Show the result in a pop-up dialog
    tk.messagebox.showinfo("File Comparison Result", result_text)

