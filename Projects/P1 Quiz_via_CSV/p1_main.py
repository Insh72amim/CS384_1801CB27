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


class home_screen:
    def __init__(self, roll, name):
        self.roll = roll
        self.name = name
        mainmaster = Tk()
        Label(mainmaster, text="Select Quiz", font=(
            "Helvetica", 20, "bold italic")).pack()
        selected_quiz = StringVar()
        for filename in os.listdir("./quiz_wise_questions"):
            if filename.endswith(".csv"):
                Radiobutton(mainmaster, text=filename[:-4], variable=selected_quiz,
                            value=filename, anchor="e", justify=LEFT).pack()
        Button(mainmaster, text="Click!!", command=lambda: [
               mainmaster.destroy(), self.start_quiz(selected_quiz.get())]).pack()
        mainmaster.mainloop()

    def start_quiz(self, filename):
        quiz_screen = Tk()

        def unat_event(event):
            self.__get_unattem()
        quiz_screen.bind("<Control_L><Alt_L><U>", unat_event)

        def goto_event(event):
            self.__go_to()
        quiz_screen.bind("<Control_L><Alt_L><G>", goto_event)

        def submit_event(event):
            self.submit()
        quiz_screen.bind("<Control_L><Alt_L><F>", submit_event)

        def export_event(event):
            self.__export_csv()
        quiz_screen.bind("<Control_L><Alt_L><E>", export_event)
        self.filename = filename
        self.user_mark_ds = datastore.users_marks_datastore()
        self.q_ds = datastore.quiz_datastore(filename).get_quiz()
        info_frame = Frame(quiz_screen)
        info_frame.pack(side=TOP)
        self.channel = queue.Queue()
        self.max_timer = self.q_ds.get("q_time")
        thread = threading.Thread(target=self.timer)
        Label(info_frame, text="Timer: ").grid(row=0, sticky=W)
        self.timer_lb = Label(info_frame, text="")
        self.timer_lb.grid(row=0, column=1)
        Label(info_frame, text="Roll: ").grid(row=1, sticky=W)
        Label(info_frame, text=self.roll).grid(row=1, column=1)
        Label(info_frame, text="Name: ").grid(row=2, sticky=W)
        Label(info_frame, text=self.name).grid(row=2, column=1)
        Button(info_frame, text="Unattempted Questions",
               command=self.__get_unattem).grid(row=3, sticky=W)
        Button(info_frame, text="Goto Question:",
               command=self.__go_to).grid(row=3, column=1)
        Button(info_frame, text="Export Database into CSV",
               command=self.__export_csv).grid(row=4, sticky=W)
        self.info_frame = info_frame
        thread.start()
        # Question frame
        self.response = {key: value for key, value in zip(self.q_ds.get(
            "questions").keys(), [-1]*len(self.q_ds.get("questions")))}
        self.ques_frame = Frame(quiz_screen)
        self.ques_frame.pack()
        self.q_num = 1
        self.ques = self.create_q(self.q_num)
        self.opts = self.create_options()
        self.display_q(self.q_num)
        self.next_btn = Button(
            self.ques_frame, text="Save & Next", command=self.next)
        self.submit_btn = Button(
            self.ques_frame, text="Final Submit", command=self.submit)
        self.next_btn.pack(pady=10, padx=5, side=LEFT)
        self.submit_btn.pack(pady=10, padx=5)
        #########################################################
        self.quiz_screen = quiz_screen
        quiz_screen.mainloop()
