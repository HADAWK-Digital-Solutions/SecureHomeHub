import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        root.title("Secure Home Hub")
        root.geometry("600x500")
        
        # This will create style object
    

        # Change the background color of the root window to dark gray
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

    def create_alerts_page(self):
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        
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
        return frame
    
    def create_users_page(self):
        frame = ttk.Frame(self.root)
        style = ttk.Style()
        style.configure("DarkGray.TFrame", background="#01325e")
        frame.configure(style="DarkGray.TFrame")
        
        label = tk.Label(frame, text="Users Page")
        label.pack(pady=20)
        sub_frame = ttk.Frame(frame)
        sub_frame.pack(pady=20)
        button = tk.Button(sub_frame, text=f"User Privleges")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Superusers")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Super User Priveleges")
        button.grid(row=0, column=3, padx=10)
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
        button = tk.Button(sub_frame, text=f"Power off")
        button.grid(row=0, column=1, padx=10)
        button = tk.Button(sub_frame, text=f"Lock")
        button.grid(row=0, column=2, padx=10)
        button = tk.Button(sub_frame, text=f"Restart")
        button.grid(row=0, column=3, padx=10)
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
