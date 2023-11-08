import tkinter as tk
from tkinter import ttk
import os
import subprocess

class App:
    def __init__(self, root):
        self.root = root
        root.title("Secure Home Hub")
        root.geometry("800x480")
        

        # Configure row and column weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # EXTREMELY TEMP THIS IS NOT SOMETHING THATS STAYING.
        #def launch_script():
            # More Temp Cramp I Don't Care.
            #script_path = 'display_ports.py'

        # Change the background color of the root window to dark blue
        root.configure(bg="#01325e") 

        # Create a frame to hold the buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.grid(row=0, column=0, sticky="nsew")

        # Create and configure buttons
        button_texts = ["Alerts", "Scans", "Users", "Devices", "Network", "Power Off"]
        
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
        self.pages.extend([alerts_frame, scans_frame, users_frame, devices_frame, network_frame, power_frame])

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
        button = tk.Button(sub_frame, text=f"Alert Times")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Alert Triggers")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Alert Priority")
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Intrusion Detection", command=lambda: os.system("intrusion_detect_v2.py"))
        button.grid(row=0, column=4, padx=10)
        button = tk.Button(sub_frame, text=f"Help", bg="skyblue")
        #This is fucking stupid, I've tried over 30 times to place a fucking button. We are going with the chump method I guess. Fuck this.
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
        button = tk.Button(sub_frame, text=f"User Privleges")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Superusers")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Super User Priveleges")
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Help")
        button.grid(row=1, column=5)
        return frame
    

    def create_devices_page(self):
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#034785")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Devices Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"Manage Devices")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Connect Devices")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Scan for Devices")
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Display Ports", command=lambda: os.system("display_ports.py"))
        button.grid(row=0, column=4, padx=10)
        button = tk.Button(sub_frame, text=f"Help")
        button.grid(row=1, column=8)
        return frame

    def create_scans_page(self) :
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Scans Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"Scan Times")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Scan after Alerts")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Quick Enable Nightly Scans")
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Scan Script", command=lambda: os.system("scan2.1.py"))
        button.grid(row=0, column=4, padx=10)
        button = tk.Button(sub_frame, text=f"Help")
        button.grid(row=1, column=8)
        return frame
    
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
        button = tk.Button(sub_frame, text=f"Help")
        button.grid(row=1, column=5)
        return frame
    
    def create_power_page(self) :
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Power Options")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"Power off", command=lambda: root.quit())
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Lock")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Restart")
        button.grid(row=0, column=3, padx=10)
        button = tk.Button(sub_frame, text=f"Help")
        button.grid(row=1, column=5)
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
