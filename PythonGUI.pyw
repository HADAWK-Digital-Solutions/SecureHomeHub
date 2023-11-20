# The above class creates a graphical user interface (GUI) for a secure home hub application with
# different pages for alerts, scans, users, devices, network, power options, and setup.


#Importing libraries
import tkinter as tk
from tkinter import ttk
import os
import subprocess
from subprocess import call

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
        button = tk.Button(sub_frame, text=f"Help", command=lambda: os.system('start " " readme.txt'))
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
        button = tk.Button(sub_frame, text=f"Help", command=lambda: os.system('start " " readme.txt'))
        button.grid(row=1, column=5)
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
    
    #Create Devices Page
    def create_devices_page(self):
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#034785")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Devices Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"Topology", command=lambda: call(['python', '-i', 'topology.py']))
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Connect Devices", command=compare_files)
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Scan for Intrusion on Devices", command=lambda: call(['python', '-i', 'intrusion_detect_v2.py']))
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Display Ports", command=lambda: call(['python', '-i', 'display_ports.py']))
        button.grid(row=0, column=4, padx=10)
        button = tk.Button(sub_frame, text=f"Help", command=lambda: os.system('start " " readme.txt'))
        button.grid(row=1, column=8)
        
        def compare_files():
            # Read the contents of the original file
            original_file_path = filedialog.askopenfilename(title="Select the original file",
                                                            filetypes=[("Text files", "*.txt")])
            
            with open(original_file_path, 'r') as file:
                original_content = file.read()
    
            # Run the IoT_devices.py script and capture its output
            iot_devices_script_output = subprocess.check_output(['python', 'IoT_devices.py'], universal_newlines=True)
    
            # Compare the original content with the script output
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

        # Create a frame to hold the blue rectangles
        rectangles_frame = ttk.Frame(frame, style="DarkGray.TFrame")
        rectangles_frame.pack(fill=tk.BOTH, expand=True)

        # Fetch a list of connected IoT devices (replace this with your actual device fetching logic)
        device_list = [
            {"name": "Device1", "ip": "192.168.1.1"},
            {"name": "Device2", "ip": "192.168.1.2"},
            {"name": "Device3", "ip": "192.168.1.3"},
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
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{device['name']}\n{device['ip']}", fill="white")
        return frame
    
        
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
        button = tk.Button(sub_frame, text=f"Help", command=lambda: os.system('start " " readme.txt'))
        button.grid(row=1, column=8)
        
        return frame
    
    #Create Netowkr Page
    def create_network_page(self) :
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Network Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"Connected Devices")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Internet Connection")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Connectivity Test")
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Snort", command=lambda: call(['python', '-i', 'snort.py']))
        button.grid(row=0, column=4, padx=10)
        button = tk.Button(sub_frame, text=f"Help", command=lambda: os.system('start " " readme.txt'))
        button.grid(row=1, column=7)
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
        button = tk.Button(sub_frame, text=f"Help", command=lambda: os.system('start " " readme.txt'))
        button.grid(row=1, column=5)
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
    root = tk.Tk()
    app = App(root)
    root.mainloop()
