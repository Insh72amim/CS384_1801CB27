from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import datetime
import os
import time

# Creating and initializing the window
root = Tk()
root.title("Untitled")
root.geometry("300x300")
root.resizable(height=None, width=None)

# *****Status bar*****

statbarb = Label(root, text="Ln", relief=SUNKEN, bd=1, anchor="w")

# *****Global variables*****

# Variable for the present file loaded
file_variable = None

# *****Text Area*****

# Adding the text area
text_area = Text(root, undo=True, wrap=None,
                 height=root.winfo_height(), width=root.winfo_width())
text_area.grid(row=0, sticky=N + E + S + W)
# Making the text area auto resizable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# *****Scroll Bar******
# Creating the vertical scrollbar
scrollbarv = Scrollbar(text_area, command=text_area.yview)
# Adding the scrollbar to root
text_area.config(yscrollcommand=scrollbarv.set)
# Packing the scrollbar
scrollbarv.pack(side=RIGHT, fill=Y)

menu = Menu(root)
root.config(menu=menu)

menu.add_command(label="About", command=about)
root.mainloop()
