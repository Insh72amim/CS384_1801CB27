import os
import time
import sqlite3
import csv
import bcrypt
import time
import re
import keyboard
import threading
import getpass as gp
import pandas as pd
from tkinter import *

global path
path = os.getcwd()

global end_timer, detect_keypress
end_timer, detect_keypress = False, True

global uanttempted_ques
uanttempted_ques = []

def create_load_reg_data():
    users_data = []
    filename = sqlite3.connect("project1 quiz cs384.db")
    c = filename.cursor()

    try:
        c.execute(
            """CREATE TABLE project1_registration
	    	         (name text, roll text, password text, contact integer(10))"""
        )
    except:
        pass

    for row in c.execute("SELECT * FROM project1_registration"):
        users_data.append(row)
    filename.close()

    return users_data


# print(users_data)
# exit()

# currPath = os.getcwd()


def timer(quiz):

    time_detail = 0
    with open(os.path.join(path, "quiz_wise_questions", f"q{quiz}.csv"), "r") as file:
    	reader = csv.reader(file)
    	for row in reader:
    		time_detail = row[10]
    		file.close()
    		break
    tt = re.findall('\d+', time_detail)

    root = Tk()
    root.geometry("300x80")
    root.title("Timer")

    minute = StringVar()
    second = StringVar()

    minute.set("00")
    second.set("00")

    minuteEntry = Entry(root, width=3, font=(
        "Arial", 18, ""), textvariable=minute)
    minuteEntry.place(x=100, y=20)

    secondEntry = Entry(root, width=3, font=(
        "Arial", 18, ""), textvariable=second)
    secondEntry.place(x=150, y=20)

    t = (int(tt[0]))*60

    while t > -1:
        mins, secs = divmod(t, 60)
        if end_timer:
        	root.destroy()
        	break
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
        root.update()
        time.sleep(1)
        t -= 1


def register_login():

    reg_users = create_load_reg_data()
    reg_roll_no = []
    for r in reg_users:
        reg_roll_no.append(r[1])

    name = ""
    roll_no = ""
    password = ""
    contact_no = 0

    username = input("Username: ")
    if username in reg_roll_no:
        # print("Password: ")
        password = gp.getpass("Password:")
        # print(hashed_pw)

        if bcrypt.checkpw(password.encode('utf-8'), reg_users[reg_roll_no.index(username)][2]):
            print("Succesfully logged in!")
            return reg_users[reg_roll_no.index(username)]
        else:
            print("Wrong Password")
    else:
        print("User is not registered. Kindly register.")
        name = input("Name: ")
        roll_no = input("Roll No.: ")
        contact_no = int(input("Contact No.: "))
        password = gp.getpass("Password:")
        hashable_pw = bytes(password, encoding="utf-8")
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = sqlite3.connect("project1 quiz cs384.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO project1_registration VALUES (?,?,?,?)",
            (name, roll_no, hashed_pw, contact_no),
        )
        conn.commit()
        conn.close()
        print("Successfully registered!")
        return (name, roll_no, hashed_pw, contact_no)


def print_user_data(user_data, skipped):
    os.system('cls')
    print(f"Roll: {user_data[1]}\nName: {user_data[0]}")
    if skipped:
    	print(f"Unattempted Questions: ", skipped_questions)
    else:
    	print(f"Unattempted Questions: ")
    print("Goto Question: Press Ctrl+Alt+G")
    print("Final Submit: Press Ctrl+Alt+F")
    print("Export Database into CSV: Press Ctrl+Alt+E")
    print()


def save_marks_in_database(roll_no, quiz_no, marks):
    os.chdir(path)
    # print("MARKS: ", type(marks.item()))
    conn = sqlite3.connect('project1 quiz cs384.db')
    c = conn.cursor()

    try:
        c.execute(
            """CREATE TABLE project1_marks
	    	         (roll text, quiz_no integer(2), marks integer(3))"""
        )
    except:
        pass

    if not type(marks) == int:
    	mark = marks.item()
    else:
    	mark = marks
    data = (roll_no, quiz_no)
    c.execute("DELETE FROM project1_marks WHERE roll=? AND quiz_no=?", data)
    c.execute("INSERT INTO project1_marks VALUES (?,?,?)",
              (roll_no, quiz_no, mark))
    conn.commit()
    conn.close()


def print_marks_from_database(roll_no):
    os.chdir(path)
    conn = sqlite3.connect('project1 quiz cs384.db')
    c = conn.cursor()

    users_data = []

    roll = (roll_no,)
    for row in c.execute("SELECT * FROM project1_marks WHERE quiz_no=?", roll):
        users_data.append(row)

    print(users_data)


def detect_hotkeys():
    tmp = ''
    while detect_keypress:
        try:
            if keyboard.is_pressed('ctrl+alt+u') or keyboard.is_pressed('ctrl+alt+U'):
                tmp = 'skip_question'
                return tmp
            elif keyboard.is_pressed('ctrl+alt+g') or keyboard.is_pressed('ctrl+alt+G'):
                tmp = 'goto_question'
                return tmp
            elif keyboard.is_pressed('ctrl+alt+f') or keyboard.is_pressed('ctrl+alt+F'):
                end_quiz = True
                end_timer = True
                tmp = 'final_submit'
                return tmp
            elif keyboard.is_pressed('ctrl+alt+e') or keyboard.is_pressed('ctrl+alt+E'):
                tmp = 'export_to_csv'
                return tmp
            elif keyboard.is_pressed('1'):
            	tmp = '1'
            	print("1")
            	return tmp
            elif keyboard.is_pressed('2'):
            	tmp = '2'
            	print("2")
            	return tmp
            elif keyboard.is_pressed('3'):
            	tmp = '3'
            	print("3")
            	return tmp
            elif keyboard.is_pressed('4'):
            	tmp = '4'
            	print("4")
            	return tmp
            elif keyboard.is_pressed('s') or keyboard.is_pressed('S'):
            	tmp = 's'
            	print("s")
            	return tmp
            elif keyboard.is_pressed('ctrl+q') or keyboard.is_pressed('ctrl+Q'):
            	tmp = 'q'
            	return tmp
        except:
            print("an error occured")
            break

def export_to_csv():
	for i in range(1,4):
		fileName = f"quiz{i}.csv"
		conn = sqlite3.connect('project1 quiz cs384.db')
		c = conn.cursor()
		data_to_write = []
		for row in c.execute("SELECT * FROM project1_marks WHERE quiz_no=?", (i,)):
			data_to_write.append(row)
		# print(data_to_write)
		if not data_to_write == []:
			with open(os.path.join(path, "quiz_wise_responses", fileName), "w") as file:
				writer = csv.writer(file)
				writer.writerow(["Roll No.", "Quiz No.", "Marks"])
				writer.writerows(data_to_write)

def start_quiz(quiz, user):
    questions_folder = os.path.join(path, "quiz_wise_questions")
    responses_folder = os.path.join(path, "quiz_wise_responses")
    individual_folder = os.path.join(path, "individual_responses")

    roll_no = user[1]
    quiz_no = quiz

    csv_to_open = "q"+str(quiz_no)+".csv"
    os.chdir(questions_folder)
    df_quiz = pd.read_csv(csv_to_open)
    count, tmp = 0, ''
    global skipped_questions
    marks_quiz, skipped_questions, responses_for_csv = [], [], []
    no_of_skipped_questions, correct, wrong, total_marks = 0, 0, 0, 0
    show_skipped = False
    # print(df_quiz.loc[0])
    # exit()

    while count < df_quiz.shape[0]:
        # os.system('clear')
        # print(list(df_quiz.loc[0][0:-1]))
        # exit()
        count += 1
        marks_gained = 0
        print_user_data(user, show_skipped)
        # print()
        print(f"    Question {count}) {df_quiz.question[count-1]}")
        print(f"Option 1) {df_quiz.option1[count-1]}")
        print(f"Option 2) {df_quiz.option2[count-1]}")
        print(f"Option 3) {df_quiz.option3[count-1]}")
        print(f"Option 4) {df_quiz.option4[count-1]}")
        print()
        print(
            f"    Credits if Correct Option: {df_quiz.marks_correct_ans[count-1]}")
        print(f"Negative Marking: {df_quiz.marks_wrong_ans[count-1]}")
        compulsion_map = {'n': "No", 'y': "Yes"}
        print(
            f"Is compulsory: {compulsion_map[df_quiz.compulsory[count-1]]}")
        print()

        if compulsion_map[df_quiz.compulsory[count-1]] == "Yes":
            print("   Enter Choice (1, 2, 3, 4):  ")
            tmp = detect_hotkeys()
        else:
            print("   Enter Choice (1, 2, 3, 4, S):  ")
            tmp = detect_hotkeys()
        time.sleep(0.5)
        # print(f"You Answered: Option {tmp}")
        # print(f"Correct Ansswer: {df_quiz.correct_option[count-1]}")

        if tmp == str(df_quiz.correct_option[count-1]):
            # print(tmp)
            marks_gained = df_quiz.marks_correct_ans[count-1]
            correct += 1
        elif tmp == 's':
            # print(tmp)
            skipped_questions.append(count)
            no_of_skipped_questions += 1
            marks_gained = 0
        elif tmp == 'export_to_csv':
        	count -= 1
        	export_to_csv()
        	marks_gained = 0
        elif tmp == 'skip_question':
        	count -= 1
        	show_skipped = True
        elif tmp == 'goto_question':
            count = int(input("Goto the question no. :"))
            count -= 1
            continue
        elif tmp == 'final_submit':
        	count -= 1
        	break
        else:
            marks_gained = df_quiz.marks_wrong_ans[count-1]
            wrong += 1
            # count -= 1
        # print(f"Marks gained : {marks_gained}")
        marks_quiz.append(marks_gained)
        # print("count: ", count)
        if (not count<1) and tmp in ['1','2','3','4','s']:
	        total_marks += df_quiz.marks_correct_ans[count-1]
	        extra = [tmp]
	        responses_for_csv.append(list(df_quiz.loc[count-1][0:-1]))
	        responses_for_csv[count-1] += extra

    # ----------------------------------Responses csv files-------------------------------------
    header_responses = df_quiz.columns.values
    header_responses = list(header_responses)[:-1]

    additional_header = ['marked choice']
    header_responses = header_responses + additional_header
    # --------------------Change of path----------------
    os.chdir(path)
    os.chdir(os.path.join(path, "individual_responses"))
    # --------------------------------------------------------
    total_marks_obtained = sum(marks_quiz)
    additional_col = {
        "Total": [correct, wrong, no_of_skipped_questions, total_marks_obtained, total_marks],
        "Legend": ["Correct Choices", "Wrong Choices", "Unattempted", "Marks Obtained", "Total Quiz Marks"]
    }

    # print(header_responses)
    new_df = pd.DataFrame(additional_col)
    # print(responses_for_csv)
    responses_df = pd.DataFrame(responses_for_csv, columns=header_responses)
    header_responses += ["Total", "Legend"]
    responses_df = pd.concat([responses_df, new_df], axis=1)

    responses_csv_name = "q" + str(quiz_no) + "_" + roll_no + ".csv"
    responses_df.to_csv(responses_csv_name, index=False)

    save_marks_in_database(roll_no, quiz_no, total_marks_obtained)

    print_user_data(user, show_skipped)
    # print()
    print(f"Total Quiz Questions: {count}")
    print(f"Total Quiz Questions Attempted: {count - no_of_skipped_questions}")
    print(f"Total Correct Questions: {correct}")
    print(f"Total Wrong Questions: {wrong}")
    print(f"Total Marks Questions: {total_marks_obtained}/{total_marks}\n")

    # print_marks_from_database(roll_no)


user = register_login()
# print("User details: ", user)
# timer(1)
# exit()

if not user == []:
    quiz = int(input("Which quiz do you want to attend ? (1/2/3): "))
    t1 = threading.Thread(target=start_quiz, args=(quiz, user,))
    t2 = threading.Thread(target=timer, args=(quiz,))

    t1.start()
    t2.start()

    t1.join()
    end_timer = True
    print("Press 'Ctrl+Q' to quit or 'Ctrl+Alt+E' to export data to csv")
    key = detect_hotkeys()
    if key == 'export_to_csv':
    	# print_marks_from_database(3)
    	export_to_csv()
    	detect_keypress = False
    else:
    	detect_keypress = False
# print("Registered Users:")
# print(reg_names)
'''
if __name__ == "__main__":
    t1 = threading.Thread(target=start_quiz, args=(quiz, user,))
    t2 = threading.Thread(target=detect_hotkeys, args=())
    t3 = threading.Thread(target=timer, args=())

    t1.start()
    t2.start()

    t2.join()
    stat = False'''
