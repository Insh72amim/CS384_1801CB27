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


def next(self):
        if self.q_num >= len(self.q_ds.get("questions")):
            messagebox.showwarning(
                "Warning", "You are at the end.Press Submit to proceed")
        else:
            self.response["{}".format(self.q_num)] = self.opt_selected.get()
            self.q_num += 1
            self.opt_selected.set(self.response["{}".format(self.q_num)])
            self.display_q(self.q_num)

    def submit(self):
        self.response["{}".format(self.q_num)] = self.opt_selected.get()
        self.end_quiz()

    def check_quiz(self):
        total_marks = 0
        total_quiz_marks = 0
        total_unattempted = 0
        total_cor_ques = 0
        total_wrong_ques = 0
        out_fname = "individual_responses/{}_{}.csv".format(
            self.filename.split(".csv")[0], self.roll)
        writer = csv.DictWriter(open(out_fname, "w"), fieldnames=["ques_no", "question", "option1", "option2", "option3", "option4",
                                                                  "correct_option", "marks_correct_ans", "marks_wrong_ans", "compulsory", "marked_choice", "Total", "Legend"])
        writer.writeheader()
        for q in self.q_ds.get("questions").values():
            total = 0
            resp = self.response[q.get("ques_no")]
            q["marked_choice"] = resp
            if resp == -1:
                q["marked_choice"] = ""
                q["Legend"] = "Unattempted"
                total_unattempted += 1
            if resp == int(q.get("correct_option")):
                total = int(q.get("marks_correct_ans"))
                q["Legend"] = "Correct Choice"
                total_cor_ques += 1
            elif resp == -1 and q.get("compulsory") == "y":
                total = int(q.get("marks_wrong_ans"))
                q["Legend"] = "Wrong Choice"
                total_wrong_ques += 1
            elif resp != -1 and resp != int(q.get("correct_option")):
                total = int(q.get("marks_wrong_ans"))
                q["Legend"] = "Wrong Choice"
                total_wrong_ques += 1
            q["Total"] = total
            q["option1"] = q.get("options")[0]
            q["option2"] = q.get("options")[1]
            q["option3"] = q.get("options")[2]
            q["option4"] = q.get("options")[3]
            q.pop("options")
            writer.writerow(q)
            total_marks += total
            total_quiz_marks += int(q.get("marks_correct_ans"))
        self.user_mark_ds.update_mark(self.roll, self.filename, total_marks)
        temp_dct = {key: value for key, value in zip(
            writer.fieldnames, [""]*len(writer.fieldnames))}
        temp_dct["Total"] = total_marks
        temp_dct["Legend"] = "Marks Obtained"
        writer.writerow(temp_dct)
        temp_dct["Total"] = total_quiz_marks
        temp_dct["Legend"] = "Total Quiz Marks"
        writer.writerow(temp_dct)
        return {
            "total_ques": len(self.q_ds.get("questions")),
            "total_attemp": len(self.q_ds.get("questions"))-total_unattempted,
            "total_Correct": total_cor_ques,
            "total_wrong": total_wrong_ques,
            "total_marks": total_marks,
            "total_quiz_marks": total_quiz_marks
        }

    def end_quiz(self):
        self.ques_frame.destroy()
        self.info_frame.destroy()
        result = self.check_quiz()
        Label(self.quiz_screen, text="Quiz Submitted!\nHere The Result").grid(row=0)
        Label(self.quiz_screen, text="Total Quiz Questions: ").grid(
            row=1, sticky=W)
        Label(self.quiz_screen, text=result.get(
            "total_ques")).grid(row=1, column=1)
        Label(self.quiz_screen, text="Total Quiz Questions Attempted: ").grid(
            row=2, sticky=W)
        Label(self.quiz_screen, text=result.get(
            "total_attemp")).grid(row=2, column=1)
        Label(self.quiz_screen, text="Total Correct Questions: ").grid(
            row=3, sticky=W)
        Label(self.quiz_screen, text=result.get(
            "total_Correct")).grid(row=3, column=1)
        Label(self.quiz_screen, text="Total Wrong Questions: ").grid(
            row=4, sticky=W)
        Label(self.quiz_screen, text=result.get(
            "total_wrong")).grid(row=4, column=1)
        Label(self.quiz_screen, text="Total Marks Obtained: ").grid(
            row=5, sticky=W)
        Label(self.quiz_screen, text=result.get(
            "total_marks")).grid(row=5, column=1)

    def create_options(self):
        b_val = 0
        b = []
        self.opt_selected = IntVar()
        self.opt_selected.set(-1)
        while b_val < 4:
            btn = Radiobutton(self.ques_frame, text="",
                              variable=self.opt_selected, value=b_val + 1)
            b.append(btn)
            btn.pack()
            b_val = b_val + 1
        self.if_correct_label = Label(self.ques_frame, text="")
        self.ng_marking = Label(self.ques_frame, text="")
        self.is_com = Label(self.ques_frame, text="")
        self.if_correct_label.pack()
        self.ng_marking.pack()
        self.is_com.pack()
        return b

    def create_q(self, ques_num):
        q = self.q_ds.get("questions").get(
            "{}".format(ques_num)).get("question")
        qLabel = Label(self.ques_frame, text=q)
        qLabel.pack()
        return qLabel

    def display_q(self, ques_num):
        b_val = 0
        q = self.q_ds.get("questions").get("{}".format(ques_num))
        self.ques['text'] = "Q"+str(ques_num) + ". " + q.get("question")
        for op in q.get("options"):
            self.opts[b_val]['text'] = op
            b_val = b_val + 1
        self.if_correct_label["text"] = "Credits if Correct Option: {}".format(
            q.get("marks_correct_ans"))
        self.ng_marking["text"] = "Negative Marking: {}".format(
            q.get("marks_wrong_ans"))
        self.is_com["text"] = "Is compulsory: {}".format(q.get("compulsory"))


    def timer(self):
        min, sec = divmod(self.max_timer, 60)
        self.timer_lb["text"] = '{:02d}:{:02d}'.format(min, sec)
        if self.max_timer == 0:
            self.channel.put("Stop")
            print("time out")
            self.end_quiz()
            return
        self.timer_lb.after(1000, self.timer)
        self.max_timer -= 1

    def __export_csv(self):
        self.user_mark_ds.export_csv()
        print("csv files exported")

    def __get_unattem(self):
        temp_screen = Tk()
        temp_screen.geometry("300x100")
        temp_screen.title("Unattempted Questions")
        for q in self.response:
            if self.response[q] == -1:
                Label(temp_screen, text="Q{}".format(q)).pack()
        Button(temp_screen, text="OK", command=lambda:  [
               temp_screen.destroy()]).pack()

    def __go_to(self):
        temp_screen = Tk()
        temp_screen.title("Go To")
        f = Frame(temp_screen)
        f.pack()
        go_to_var = StringVar(f)
        go_to_var.set("")
        Label(f, text='Go To').grid(row=0, column=0)
        Entry(f, textvariable=go_to_var, bd=5).grid(row=0, column=1)

        def jump():
            new_f = Frame(temp_screen)
            new_f.pack()
            if go_to_var.get() != "":
                in_q = go_to_var.get()
                go_to_var.set("")
                if in_q in [i for i in self.response.keys()]:
                    q = self.q_ds.get("questions").get("{}".format(in_q))
                    Label(f, text="Q{}. {}".format(
                        q.get("ques_no"), q.get("question"))).grid(sticky=W)
                    o_selected = IntVar(f)
                    o_selected.set(-1)
                    for i in range(4):
                        Radiobutton(f, text=q.get("options")[
                                    i], variable=o_selected, value=i+1).grid(sticky=W)

                def ano_belo():
                    self.response[q.get("ques_no")] = o_selected.get()
                    if q.get("ques_no") == str(self.q_num):
                        self.opt_selected.set(o_selected.get())
                Button(f, text="Save", command=ano_belo).grid(sticky=W)
        Button(f, text="Jump", command=jump).grid(row=1, column=0)
        Button(f, text="Close X", command=lambda: [
               temp_screen.destroy()]).grid(row=1, column=1)

        # temp_screen.mainloop()
scr = screen()
