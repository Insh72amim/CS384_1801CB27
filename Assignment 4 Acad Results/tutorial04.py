import csv
import os
import pandas as pd
import shutil
shutil.rmtree('grades')
path="acad_res_stud_grades.csv"
data=pd.read_csv(path)
print(data.columns)
os.mkdir('grades')

def g2s(x):
    if x=='AA':
        return 10
    if x=='AB':
        return 9
    if x=='BB':
        return 8
    if x=='BC':
        return 7
    if x=='CC':
        return 6
    if x=='CD':
        return 5
    if x=='DD':
        return 4
    else:
        return 0

Roll_numbers=list();

with open('acad_res_stud_grades.csv','r') as file:
    reader=csv.reader(file)
    print(reader)
    for row in reader:
        path='grades/'+str(row[1])+"_individual.csv"
        if(os.path.isfile(path) == False):
            Roll_numbers.append(row[1])
            with open(path, 'a') as file2:
                writer = csv.writer(file2)
                writer.writerow(['Roll', 'semester', 'Year', 'sub_code', 'total_credits',
       'credit_obtained', 'sub_type'])
        with open(path,'a') as file2:
            writer=csv.writer(file2)
            writer.writerow([row[1],row[2],row[3],row[4],row[5],row[6],row[8]])
