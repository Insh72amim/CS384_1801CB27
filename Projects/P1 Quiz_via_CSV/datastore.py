import sqlite3
import utils
import csv
import re

class user_datastore:
    def __init__(self):
        self.conn = sqlite3.connect("project1_quiz_cs384")
        self.conn.execute('''CREATE TABLE IF NOT EXISTS project1_registration(
                username VARCHAR(10),
                password VARCHAR(45),
                name VARCHAR(45), 
                whatsapp_number VARCHAR(10)
        )''')
        self.conn.commit()
    def get_user(self,roll):
        found = True
        cur = self.conn.cursor()
        data = cur.execute('''SELECT * FROM project1_registration WHERE username=:roll''',{"roll":roll}).fetchone()
        if data == None:
            found = False
        cur.close()
        return {
            "found" : found,
            "data" : data
        }
    def register(self,roll,text_password,name,whatsapp_number):
        if self.get_user(roll)["found"]:
            return False
        self.conn.execute('''INSERT INTO project1_registration(username,password,name,whatsapp_number) VALUES(?,?,?,?)''',
        [
            (roll),
            (utils.genMD5(text_password)),
            (name),
            (whatsapp_number)
        ])
        self.conn.commit()
        return True
    def check_cred(self,roll,password):
        found = True
        msg = "Logged in"
        data = self.get_user(roll)
        if data.get("found") == False:
            found = False
            msg = "{} not found".format(roll)
        if found and data.get("data")[1] != utils.genMD5(password):
            msg = "invalid Password"
            found = False
        return {
            "success" : found,
            "msg" : msg
        }
    
class quiz_datastore:
    def __init__(self,filename):
        self.filename = "quiz_wise_questions/{}".format(filename)
    def get_quiz(self):
        in_file = open(self.filename,"r")
        reader = csv.DictReader(in_file)
        q_time = int(reader.fieldnames[-1].split("time=")[1][:-1])
        questions = dict()
        for row in reader:
            row.pop(reader.fieldnames[-1])
            options = [row.get("option1"),row.get("option2"),row.get("option3"),row.get("option4")]
            row.pop("option1")
            row.pop("option2")
            row.pop("option3")
            row.pop("option4")
            row["options"] = options
            questions[row.get("ques_no")] = row
        return {
            "questions" : questions,
            "q_time" : q_time*60
        }

class users_marks_datastore:
    def __init__(self):
        self.conn = sqlite3.connect("project1_quiz_cs384")
        self.conn.execute('''CREATE TABLE IF NOT EXISTS project1_marks(
                roll VARCHAR(10),
                quiz_num VARCHAR(45),
                total_marks INT
        )''')
        self.conn.commit()
    def get_mark(self,roll,quiz_num):
        data = self.conn.execute(
            "SELECT * FROM project1_marks WHERE roll=:roll and quiz_num=:quiz_num",
            {"roll":roll,"quiz_num":quiz_num}
        ).fetchone()
        return data
    def update_mark(self,roll,quiz_num,marks):
        if self.get_mark(roll,quiz_num) == None:
                    self.conn.execute('''INSERT INTO project1_marks(roll,quiz_num,total_marks) VALUES(?,?,?)''',
                    [
                        (roll),
                        (quiz_num),
                        (marks)
                    ])
        else:
                    self.conn.execute(
                        '''UPDATE project1_marks SET total_marks=:total_marks WHERE roll=:roll and quiz_num=:quiz_num''',
                        {"total_marks":marks,"roll":roll,"quiz_num":quiz_num}
                    )
        self.conn.commit()
    def export_csv(self):
        for q_num in self.__get_all_quiz():
            print(q_num)
            file_name = "quiz{}.csv".format(int(re.findall(r"\d+",q_num)[0]))
            f = open(file_name,"w")
            writer = csv.DictWriter(f,fieldnames=["Roll No","Quiz No","Total Marks"])
            writer.writeheader()
            for d in self.conn.execute("SELECT * FROM project1_marks WHERE quiz_num=:quiz_num",{"quiz_num":q_num}).fetchall():
                writer.writerow({
                    "Roll No": d[0],
                    "Quiz No" : d[1],
                    "Total Marks" : d[2]
                })
    def __is_quiz_exists(self,quiz_num):
        return self.conn.execute(
            "SELECT quiz_num FROM project1_marks WHERE quiz_num=:quiz_num",
            {"quiz_num":quiz_num}
        ).fetchone() != None
    def __get_all_quiz(self):
        ok = True
        out = []
        i = 1
        while ok:
            q_num = "q{}.csv".format(i)
            if self.__is_quiz_exists(q_num):
                out.append(q_num)
                i+=1
            else:
                ok = False
        return out

# umd = users_marks_datastore()
# umd.update_mark("1801CE21","quiz1.csv",98)
# umd.update_mark("1801CE22","quiz1.csv",98)
# umd.update_mark("1801CE23","quiz1.csv",98)
# umd.update_mark("1801CE21","quiz2.csv",98)
# umd.update_mark("1801CE22","quiz2.csv",98)
# umd.update_mark("1801CE23","quiz2.csv",98)

# # print(umd.get_mark("1801CE21","quiz1.csv"))
# umd.export_csv()