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

# *****Various functions of the text editor


def createnew(*args):
    global root, text_area, file_variable
    file_variable = None
    root.title("New File")
    text_area.delete(1.0, END)


def openfile(*args):
    global root, text_area, file_variable, origfilecontents
    file_variable = askopenfilename(defaultextension=".txt", filetypes=[
        ("All Files", "*.*"), ("Text Files", "*.txt")])
    if file_variable == "":
        file_variable = None
        origfilecontents = None
    else:
        try:
            root.title(os.path.basename(file_variable))
            text_area.delete(1.0, END)
            file = open(file_variable, "r")
            text_area.insert(1.0, file.read())
            origfilecontents = file.read()
            file.close()
        except:
            root.title("NeeruText")
            showerror("ERROR", str("Unable to open " +
                                   file_variable+"\n"+"Not a .txt file!"))


def savefile(*args):
    global root, text_area, file_variable, origfilecontents
    if file_variable == None:
        saveasfile()
    else:
        file = open(file_variable, "w")
        origfilecontents = text_area.get(1.0, END)
        file.write(text_area.get(1.0, END))
        file.close()
        showinfo("Successfully saved", "All changes saved")


def saveasfile():
    global root, text_area, file_variable
    file_variable = asksaveasfilename(defaultextension=".txt", filetypes=[
        ("All Files", "*.*"), ("Text Documents", "*.txt")])
    if file_variable == "":
        file_variable = None
    else:
        file = open(file_variable, "w")
        file.write(text_area.get(1.0, END))
        file.close()
        showinfo("Successfully saved", str(
            "Saved as "+file_variable+" successfully!"))


def datetimefunc(*args):
    global text_area
    text_area.insert(END, str(datetime.datetime.now()))


def cutop():
    global text_area
    text_area.event_generate("<<Cut>>")


def copyop():
    global text_area
    text_area.event_generate("<<Copy>>")


def pasteop():
    global text_area
    text_area.event_generate("<<Paste>>")


def deleteop():
    global text_area
    ranges = text_area.tag_ranges(SEL)
    text_area.delete(*ranges)


def about():
    showinfo("About NText", "This is a text editor built using Tkinter\nDeveloped by Syed Insherah Amim and Ankush Panghal.\n")


def exitapplication():
    root.quit()


def selectall():
    global text_area
    text_area.event_generate("<<SelectAll>>")


def undofunc():
    global text_area
    try:
        text_area.edit_undo()
    except:
        pass


def redofunc():
    global text_area
    try:
        text_area.edit_redo()
    except:
        pass


def findlinecount():
    global text_area, sub_menu_3
    if text_area.compare("end-1c", "!=", "1.0"):
        submenu6.entryconfig(0, label=str(
            str(int(text_area.index('end').split('.')[0]) - 1)+" Lines"))


def findwordcount():
    global text_area, submenu5
    if text_area.compare("end-1c", "!=", "1.0"):
        submenu5.entryconfig(0, label=str(
            str(len(text_area.get(0.0, END).replace("\n", " ").split(" "))-1)+" Words"))


def exitwithoutsaving():
    global root, text_area, origfilecontents
    if file_variable != None:
        if origfilecontents == text_area.get(1.0, END):
            pass
        else:
            exitapplication()
    result = askquestion(title="Exit", message=str("Do you want to save changes made to "+(
        os.path.basename(file_variable) if file_variable != None else "New File")+" ?"), icon='warning')
    if result == 'yes':
        savefile()
    else:
        exitapplication()

# *****Binding shortcut keys to functions*****


text_area.bind("<F5>", datetimefunc)
text_area.bind("<Control-n>", createnew)
text_area.bind("<Control-s>", savefile)
text_area.bind("<Control-o>", openfile)
# *****Adding the menus*****
menu = Menu(root)
root.config(menu=menu)

# Adding the File submenu

sub_menu_1 = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=sub_menu_1)
sub_menu_1.add_command(label="New    Ctrl+N", command=createnew)
sub_menu_1.add_command(label="Open   Ctrl+O", command=openfile)
sub_menu_1.add_command(label="Save    Ctrl+S", command=savefile)
sub_menu_1.add_command(label="Save as", command=saveasfile)
sub_menu_1.add_separator()
sub_menu_1.add_command(label="Exit", command=exitwithoutsaving)

# Adding the Edit submenu

sub_menu_2 = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=sub_menu_2)
sub_menu_2.add_command(label="Undo        Ctrl+Z", command=undofunc)
sub_menu_2.add_command(label="Redo        Ctrl+Y", command=redofunc)
sub_menu_2.add_separator()
sub_menu_2.add_command(label="Cut          Ctrl+X", command=cutop)
sub_menu_2.add_command(label="Copy       Ctrl+C", command=copyop)
sub_menu_2.add_command(label="Paste       Ctrl+V", command=pasteop)
sub_menu_2.add_command(label="Delete      Del", command=deleteop)
sub_menu_2.add_separator()
sub_menu_2.add_command(label="Select all    Ctrl+A", command=selectall)
sub_menu_2.add_command(label="Date/Time   F5", command=datetimefunc)

# Adding the view submenu

sub_menu_3 = Menu(menu, tearoff=0)
submenu5 = Menu(sub_menu_3, tearoff=0, postcommand=findwordcount)
submenu6 = Menu(sub_menu_3, tearoff=0, postcommand=findlinecount)
menu.add_cascade(label="View", menu=sub_menu_3)
sub_menu_3.add_cascade(label="Word Count", menu=submenu5)
sub_menu_3.add_cascade(label="Line Count", menu=submenu6)
submenu5.add_command(label="0 Words", command=None)
submenu6.add_command(label="0 Lines", command=None)
# Adding the about submenu

sub_menu_4 = Menu(menu, tearoff=0)
menu.add_command(label="About", command=about)
root.mainloop()
