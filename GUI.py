# Import tkinter and ttk modules
import tkinter as tk
import tkinter.ttk as ttk

# Create the main window
window = tk.Tk()
window.title("Dark Green GUI")
window.geometry("300x200")

# Set the background color to dark green
window.config(bg="#006400")

# Create a black button
button = ttk.Button(window, text="Click Me", style="Black.TButton")
button.pack(padx=10, pady=10)

# Create a custom style for the button
style = ttk.Style()
style.configure("Black.TButton", foreground="black", background="black")

# Start the main loop
window.mainloop()
