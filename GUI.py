# Import CustomTkinter library
import customtkinter as ctk

# Set the default appearance mode to dark
ctk.set_appearance_mode("dark")

# Set the default color theme to green
ctk.set_default_color_theme("green")

# Create the root window using CustomTkinter
root = ctk.CTk()

# Create a label widget using CustomTkinter
label = ctk.CLabel(root, text="Hello, world!", font=("Arial", 20))

# Create a button widget using CustomTkinter
button = ctk.CButton(root, text="Click me!", command=lambda: print("You clicked the button!"))

# Place the widgets using grid method
label.grid(row=0, column=0, padx=10, pady=10)
button.grid(row=1, column=0, padx=10, pady=10)

# Start the main loop
root.mainloop()
