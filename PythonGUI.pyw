#Importing libraries
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import subprocess
from subprocess import call
import ast
import webbrowser

#The main application class is defined (App).
#The class constructor (__init__) sets up the main window and configures its properties.

class App:
    def __init__(self, root):
        self.root = root
        root.title("Secure Home Hub")
        root.geometry("800x480")
        
        # Configure row and column weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Change the background color of the root window to dark blue
        root.configure(bg="#01325e") 

        # Create a frame to hold the buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.grid(row=0, column=0, sticky="nsew")

        # Create and configure buttons
        button_texts = ["Alerts", "Scans", "Users", "Devices", "Network", "Power Off", "Redo Setup"]
        
        self.buttons = []
        for i, text in enumerate(button_texts):
            button = tk.Button(self.button_frame, text=text, command=lambda i=i: self.show_page(i))
            button.grid(row=0, column=i, sticky="nsew")
            self.buttons.append(button)

        # Create frames for each page
        self.pages = []
        alerts_frame = self.create_alerts_page()
        scans_frame = self.create_scans_page()
        users_frame = self.create_users_page()
        devices_frame = self.create_devices_page()
        network_frame = self.create_network_page()
        power_frame = self.create_power_page()
        setup_frame = self.create_setup_page()
        self.pages.extend([alerts_frame, scans_frame, users_frame, devices_frame, network_frame, power_frame, setup_frame])

        # Initially, show the first page (Alerts)
        self.current_page = alerts_frame
        self.current_page.grid(row=1, column=0, columnspan=len(self.buttons), sticky="nsew")

        # Configure column and row weights for resizing
        for i in range(len(self.buttons)):
            self.button_frame.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(0, weight=0)  # Top row
        self.root.grid_rowconfigure(1, weight=1)  # Page row
        
    

        
    #Create Alerts, this is basically the template for all other pages.
    def create_alerts_page(self):
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkBlue.TFrame", background="#01325e")
        frame.configure(style="DarkBlue.TFrame")
        
        label = tk.Label(frame, text="Alerts Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        
        #Adding Listbox
        listbox = tk.Listbox(sub_frame, selectmode=tk.SINGLE, width=40)
        listbox.grid(row=0, column=0, padx=10, pady=1)
        
        # Insert Scans, [AUTO] is used when ti's a Nightly or automatic scan specified from Scan Times. 
        for item in ["ALERT: 2023-10-11 6:20 PM", "ALERT: 2023-10-11 6:29 PM", "ALERT: 2023-10-12 6:40 PM", "ALERT: 2023-10-13 8:20 PM"]:
            listbox.insert(tk.END, item)
            
            
        button = tk.Button(sub_frame, text=f"Alert Times", command=lambda: call(['python', '-i', 'test.py']))
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Alert Triggers")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Alert Priority")
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Intrusion Detection", command=lambda: call(['python', '-i', 'intrusion_detect_v2.py']))
        button.grid(row=0, column=4, padx=10)
        # Add the Help button for opening the specified HTML file
        button = tk.Button(sub_frame, text=f"Help", command=lambda: self.open_help_page("Alerts.html"))
        button.grid(row=1, column=8)
        return frame
    
        #Create users page.
    def create_users_page(self):
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        label = ttk.Label(frame, text="Users Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"User Privileges")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Superusers")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Super User Privileges")
        button.grid(row=0, column=3, padx=10)
        # Add the Help button for opening the specified HTML file
        button = tk.Button(sub_frame, text=f"Help", command=lambda: self.open_help_page("Users.html"))
        button.grid(row=1, column=8)
                # Create a frame to hold the blue rectangles
        rectangles_frame = ttk.Frame(frame, style="DarkGray.TFrame")
        rectangles_frame.pack(fill=tk.BOTH, expand=True)

        # Fetch a list of connected IoT devices (replace this with your actual User fetching logic if possible? Again, this is moreso an example because I tried for 30 minutes to make a window function with a new window and it magically blew up in my face, so consider it more of a placeholder for a user list. really.)
        device_list = [
            {"name": "User1", "rank": "SuperUser"},
            {"name": "User2", "rank": "User"},
            {"name": "User3", "rank": "User"},
            # Add more devices as needed
        ]

        # Calculate the number of columns for the grid
        num_columns = 3  # You can adjust this based on your layout

        # Iterate over the device list and create a square for each device
        for i, device in enumerate(device_list):
            # Create a Canvas widget for each square
            canvas = tk.Canvas(rectangles_frame, bg="white", width=150, height=50)
            canvas.grid(row=i // num_columns, column=i % num_columns, padx=10, pady=10, sticky="nsew")

            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1 = 0, 0
            x2, y2 = canvas.winfo_reqwidth(), canvas.winfo_reqheight()

            # Create a rectangle on the canvas
            canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

            # Display the name and IP of the device
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{device['name']}\n{device['rank']}", fill="white")

        return frame
    

    def compare_files(self):
        # Specify the path to the IoT_devices.txt file
        file_path = "IoT_devices.txt"
        
        # Create a StringVar for result_text
        result_text = tk.StringVar()
    
        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                original_content = file.read()
    
            # Compare the original content with the script output
            iot_devices_script_path = os.path.join(os.getcwd(), 'IoT_devices.py')
            iot_devices_script_output = subprocess.check_output(['python3', iot_devices_script_path], universal_newlines=True)
    
            if original_content == iot_devices_script_output:
                result_text.set("The files are identical.")
            else:
                # Display the differences
                differences = []
    
                # Split the content into lines for a more detailed comparison
                original_lines = original_content.splitlines()
                script_output_lines = iot_devices_script_output.splitlines()
    
                # Iterate through lines and compare
                for i, (orig_line, script_line) in enumerate(zip(original_lines, script_output_lines), start=1):
                    if orig_line != script_line:
                        differences.append(f"Line {i}:\n  Original: {orig_line}\n  Script  : {script_line}")
    
                # If one file is longer than the other, add remaining lines
                if len(original_lines) > len(script_output_lines):
                    for i in range(len(script_output_lines), len(original_lines)):
                        differences.append(f"Line {i + 1} (Original): {original_lines[i]}")
    
                elif len(script_output_lines) > len(original_lines):
                    for i in range(len(original_lines), len(script_output_lines)):
                        differences.append(f"Line {i + 1} (Script): {script_output_lines[i]}")
    
                result_text.set("\n".join(differences))
        else:
            # If the file doesn't exist, run the script and capture the output
            iot_devices_script_path = os.path.join(os.getcwd(), 'IoT_devices.py')
            iot_devices_script_output = subprocess.check_output(['python3', iot_devices_script_path], universal_newlines=True)
            result_text.set(f"The file {file_path} does not exist. Script output:\n{iot_devices_script_output}")
    
        # Show the result in a pop-up dialog
        tk.messagebox.showinfo("File Comparison Result", result_text.get())


    

    # Create Devices Page
    def create_devices_page(self):
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#034785")
        frame.configure(style="DarkGray.TFrame")
    
        label = tk.Label(frame, text="Devices Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"Topology", command=lambda: call(['sudo', 'python3', '-i', 'topology_nmap1.py']))
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Connect Devices", command=self.compare_files)
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Scan for Intrusion on Devices", command=lambda: call(['python3', '-i', 'intrusion_detect_v2.py']))
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Display Ports", command=lambda: call(['python3', '-i', 'display_ports.py']))
        button.grid(row=0, column=4, padx=10)
        # Add the Help button for opening the specified HTML file
        button = tk.Button(sub_frame, text=f"Help", command=lambda: self.open_help_page("Devices.html"))
        button.grid(row=1, column=8)
    
        # Create a frame to hold the blue rectangles
        rectangles_frame = ttk.Frame(frame, style="DarkGray.TFrame")
        rectangles_frame.pack(fill=tk.BOTH, expand=True)
    
        # Open devices_formatted.txt and read each line
        with open('devices_formatted.txt', 'r') as f:
            lines = f.readlines()
    
        # Initialize the devices_list
        device_list = []
    
        # Iterate through each line, convert it to a dictionary, and append to devices_list
        for line in lines:
            device_info = ast.literal_eval(line.strip())
            device_list.append(device_info)
    
        # Now devices_list contains the information from devices_formatted.txt
    
        # Define a function to calculate the number of columns based on window width
        def calculate_num_columns(window_width, min_width):
            return max(1, window_width // min_width)
    
        # Define a function to calculate the maximum canvas dimensions
        def calculate_max_canvas_dimensions(device_list):
            max_width, max_height = 0, 0
            for device in device_list:
                text = f"IP: {device['IP']}\nMAC: {device['MAC']}\nStatus: {device['Status']}"
                text_length = max(len(line) for line in text.split('\n'))
                width = 15 * text_length
                height = 30 * len(text.split('\n'))
                max_width = max(max_width, width)
                max_height = max(max_height, height)
            return max_width, max_height + 10
    
        # Calculate the maximum canvas dimensions
        max_canvas_width, max_canvas_height = calculate_max_canvas_dimensions(device_list)
    
        # Update the number of columns based on the window width
        num_columns = calculate_num_columns(frame.winfo_width(), max_canvas_width)
    
        # Function to update the layout when the window is resized
        def update_layout(event):
            nonlocal num_columns
    
            # Update the number of columns based on the new window width
            num_columns = calculate_num_columns(event.width, max_canvas_width)
    
            # Redraw the canvas widgets with the updated layout
            redraw_canvas()
    
        # Function to redraw the canvas widgets with the current layout
        def redraw_canvas():
            # Clear existing widgets
            for widget in rectangles_frame.winfo_children():
                widget.destroy()
    
            # Iterate over the device list and create a square for each device
            for i, device in enumerate(device_list):
                # Create a Canvas widget for each square
                canvas = tk.Canvas(rectangles_frame, bg="white", width=max_canvas_width, height=max_canvas_height)
                canvas.grid(row=i // num_columns, column=i % num_columns, padx=10, pady=10, sticky="nsew")
    
                # Define the padding
                padding = 2
    
                # Define the coordinates for the top-left and bottom-right corners of the rectangle
                x1, y1 = padding, padding
                x2, y2 = max_canvas_width - padding, max_canvas_height - padding
    
                # Create a rectangle on the canvas
                canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
    
                # Display the information of the device
                text = f"IP: {device['IP']}\nMAC: {device['MAC']}\nStatus: {device['Status']}"
                canvas.create_text(x1 + padding, (y1 + y2) / 2, anchor="w", text=text, fill="white")
    
        # Bind the window resize event to the update_layout function
        frame.bind("<Configure>", update_layout)
    
        # Initial layout
        redraw_canvas()
    
        return frame

    def open_help_page(self, html_file_name):
        try:
            # Assuming that the HTML files are in the same directory as the script
            relative_path = os.path.join(os.path.dirname(__file__), html_file_name)
    
            # Open the specified HTML file in the default web browser using the webbrowser module
            webbrowser.open(relative_path, new=2)
        except Exception as e:
            # Handle any errors or exceptions here
            print(f"Error: {e}")



    #Create Scans page 
    def create_scans_page(self) :
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Scans Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        
        #Adding Listbox
        listbox = tk.Listbox(sub_frame, selectmode=tk.SINGLE, width=40)
        listbox.grid(row=0, column=0, padx=10, pady=1)
        
        # Insert Scans, [AUTO] is used when ti's a Nightly or automatic scan specified from Scan Times. 
        for item in ["Scan 2023-10-12 11:39 PM", "Scan 2023-10-13 11:20 PM", "Scan 2023-10-14 10:20 PM", "[AUTO] Scan 2023-10-15 9:30 PM"]:
            listbox.insert(tk.END, item)
        
        # Add buttons
        button = tk.Button(sub_frame, text=f"Scan Times")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Scan after Alerts")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Quick Enable Nightly Scans")
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Scan Script", command=lambda: call(['python', '-i', 'scan2.1py']))
        button.grid(row=0, column=4, padx=10)
        # Add the Help button for opening the specified HTML file
        button = tk.Button(sub_frame, text=f"Help", command=lambda: self.open_help_page("Scans.html"))
        button.grid(row=1, column=8)
        return frame
    
    def toggle_kill_switch(self):
        # Toggle between "up" and "down" commands
        if self.kill_switch_state.get() == "down":
            command = "sudo nmcli connection up Wired"
            self.kill_switch_state.set("up")
        else:
            command = "sudo nmcli connection down Wired"
            self.kill_switch_state.set("down")

        # Execute the command
        subprocess.run(command.split())

    #Create Network Page
    def create_network_page(self):
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")

        label = tk.Label(frame, text="Network Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)

        # Create a StringVar to track the state of the kill switch
        self.kill_switch_state = tk.StringVar(value="down")

        
        kill_switch_button = tk.Button(sub_frame, text="Emergency Kill Switch", command=self.toggle_kill_switch)
        kill_switch_button.grid(row=0, column=0, padx=10)
        button = tk.Button(sub_frame, text="Scan for Network Intrusion", command=lambda: call(['python3', '-i', 'intrusion_detect_v2.py']))
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text="Internet Connection Check")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text="Display Used Ports", command=lambda: call(['python', '-i', 'display_ports.py']))
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text="Check for Malicious Files", command=lambda: call(['python', '-i', 'check_malicious_files_network.py']))
        button.grid(row=0, column=4, padx=10)
        # Add the Help button for opening the specified HTML file
        button = tk.Button(sub_frame, text=f"Help", command=lambda: self.open_help_page("Network.html"))
        button.grid(row=1, column=8)
        return frame
    
    #Create power options page
    def create_power_page(self) :
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Power Options")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text="Power off", command=self.shutdown_device)
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text="Lock", command=self.lock_device)
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text="Restart", command=self.restart_device)
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Help", command=lambda: self.open_help_page("Power.html"))
        button.grid(row=1, column=8)
        return frame
    
    def show_page(self, index):
        # Hide the current page
        self.current_page.grid_forget()
        # Show the selected page
        self.current_page = self.pages[index]
        self.current_page.grid(row=1, column=0, columnspan=len(self.buttons), sticky="nsew")
        
        
        # Define a function to shut down the Ubuntu device
    def shutdown_device(self):
        try:
            # Use the 'poweroff' command to shut down the device
            subprocess.run(['sudo', 'poweroff'])
        except Exception as e:
            # Handle any errors or exceptions here
            print(f"Error: {e}")
            
            
                # Define a method to restart the Ubuntu device
    def restart_device(self):
        try:
            # Use the 'reboot' command to restart the device
            subprocess.run(['sudo', 'reboot'])
        except Exception as e:
            # Handle any errors or exceptions here
            print(f"Error: {e}")
            
            
                    # Define a method to lock the Ubuntu device
    def lock_device(self):
        try:
            # Use the 'gnome-screensaver-command' to lock the screen
            subprocess.run(['gnome-screensaver-command', '-l'])
        except Exception as e:
            # Handle any errors or exceptions here
            print(f"Error: {e}")
    
    
    #Create setup page.
    def create_setup_page(self) :
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Setup")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"Redo Setup", command=lambda: os.system('setup.c'))
        button.grid(row=0, column=1)
        button = tk.Button(sub_frame, text=f"Hotspot Setup", command=lambda: os.system('hotspot_setup.sh'))
        button.grid(row=0, column=2)
        return frame

    def show_page(self, index):
        # Hide the current page
        self.current_page.grid_forget()
        # Show the selected page
        self.current_page = self.pages[index]
        self.current_page.grid(row=1, column=0, columnspan=len(self.buttons), sticky="nsew")

if __name__ == "__main__":
    #Run the IoT_devices.py script
    subprocess.run(['python3', 'IoT_devices.py'])

    root = tk.Tk()
    app = App(root)
    root.mainloop()
