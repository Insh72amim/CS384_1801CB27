from tkinter import *
from tkinter import messagebox
import datastore
import os
import time
import queue
import threading
import csv


class screen:
    def __init__(self):
        self.mainmaster = Tk()
        self.user_datastore = datastore.user_datastore()
        # Variables for Register
        self.reg_rollnumber = StringVar()
        self.reg_pass = StringVar()
        self.reg_name = StringVar()
        self.reg_whatsappNumber = StringVar()
        # Variables for login
        self.login_Roll = StringVar()
        self.login_password = StringVar()
        #########################
        self.fill_screen()
        self.mainmaster.mainloop()

    def fill_screen(self):
        # Header
        self.header = Label(self.mainmaster, text="Login", font=('', 35))
        self.header.pack()
        # Login Frame
        lg_frame = Frame(self.mainmaster, padx=5, pady=5)
        Label(lg_frame, text='Roll No: ', font=(
            '', 20), pady=5, padx=5).grid(sticky=W)
        Entry(lg_frame, textvariable=self.login_Roll,
              bd=5, font=('', 15)).grid(row=0, column=1)
        Label(lg_frame, text='Password: ', font=(
            '', 20), pady=5, padx=5).grid(sticky=W)
        Entry(lg_frame, textvariable=self.login_password, bd=5,
              font=('', 15), show='*').grid(row=1, column=1)
        Button(lg_frame, text=' Login ', bd=3, font=('', 15),
               padx=5, pady=5, command=self.login).grid()
        Button(lg_frame, text=' Register ', bd=3, font=('', 15), padx=5,
               pady=5, command=self.rg_screen).grid(row=2, column=1)
        self.lg_frame = lg_frame
        self.lg_frame.pack()
        # Register Frame
        rg_frame = Frame(self.mainmaster)
        rg_frame = Frame(self.mainmaster, padx=5, pady=5)
        Label(rg_frame, text='Name: ', font=(
            '', 20), pady=5, padx=5).grid(sticky=W)
        Entry(rg_frame, textvariable=self.reg_name,
              bd=5, font=('', 15)).grid(row=0, column=1)
        Label(rg_frame, text='Password: ', font=(
            '', 20), pady=5, padx=5).grid(sticky=W)
        Entry(rg_frame, textvariable=self.reg_pass, bd=5,
              font=('', 15), show='*').grid(row=1, column=1)
        Label(rg_frame, text='Roll No: ', font=(
            '', 20), pady=5, padx=5).grid(sticky=W)
        Entry(rg_frame, textvariable=self.reg_rollnumber,
              bd=5, font=('', 15)).grid(row=2, column=1)
        Label(rg_frame, text='Whatsapp_No: ', font=(
            '', 20), pady=5, padx=5).grid(sticky=W)
        Entry(rg_frame, textvariable=self.reg_whatsappNumber,
              bd=5, font=('', 15)).grid(row=3, column=1)
        Button(rg_frame, text='Register', bd=3, font=('', 15),
               padx=5, pady=5, command=self.register).grid()
        Button(rg_frame, text='Back', bd=3, font=('', 15), padx=5,
               pady=5, command=self.login_screen).grid(row=4, column=1)
        self.rg_frame = rg_frame

    def login_screen(self):
        self.login_Roll.set('')
        self.login_password.set('')
        self.rg_frame.pack_forget()
        self.header["text"] = "Login"
        self.lg_frame.pack()

    def rg_screen(self):
        self.reg_rollnumber.set('')
        self.reg_pass.set('')
        self.reg_name.set('')
        self.reg_whatsappNumber.set('')
        self.lg_frame.pack_forget()
        self.header['text'] = 'Register'
        self.rg_frame.pack()

    def login(self):
        res = self.user_datastore.check_cred(
            self.login_Roll.get(), self.login_password.get())
        if res.get("success") == False:
            messagebox.showerror("Error", res.get("msg"))
        else:
            user = self.user_datastore.get_user(
                self.login_Roll.get()).get("data")
            self.mainmaster.destroy()
            home_screen(user[0], user[2])

    def register(self):
        ok = self.user_datastore.register(
            self.reg_rollnumber.get(),
            self.reg_pass.get(),
            self.reg_name.get(),
            self.reg_whatsappNumber.get()
        )
        if ok:
            messagebox.showinfo("Success", "successfully registered")
        else:
            messagebox.showerror(
                "Error", "{} already exists".format(self.reg_rollnumber.get()))
