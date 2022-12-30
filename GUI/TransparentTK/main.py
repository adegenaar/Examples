
# Import module
import tkinter as tk
#from tkinter import *
 
# Create object
root = tk.Tk()
 
# Adjust size
root.geometry("400x400")
 
# set minimum window size value
root.minsize(400, 400)
 
# set maximum window size value
root.maxsize(400, 400)

# Create semi-transparent window
#root.attributes('-alpha',0.5)
 
# Create transparent window
root.wm_attributes('-transparentcolor', root['bg']) 

label1 = tk.Label(root, text='here i am')
label1.pack(side='top')

# Creating a tuple containing 
# the specifications of the font.
Font_tuple = ("CaskaydiaCove NF", 20, "bold")
  
# Parsed the specifications to the
# Text widget using .configure( ) method.
label1.configure(font = Font_tuple,fg="yellow")

# Use overrideredirect() method, i.e. make it a frameless window
root.overrideredirect(True)

# Execute tkinter
root.mainloop()