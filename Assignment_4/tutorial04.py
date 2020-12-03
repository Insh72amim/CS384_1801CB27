import csv
import os
import pandas as pd
import shutil
shutil.rmtree('grades')
path="acad_res_stud_grades.csv"
data=pd.read_csv(path)
print(data.columns)
os.mkdir('grades')

def grade_to_score(x):
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

Roll_numbers.remove('roll')
for xyz in Roll_numbers:
    totalcredits_till=0
    receivedcred_till=0
    path = 'grades/' + str(xyz) + "_individual.csv"
    datafile=pd.read_csv(path)
    total_semester=datafile['semester'].unique().max()
    semwise_credit=0
    CPI=0
    print(
        'semester wise score for roll no: ', xyz,'and total semester are',total_semester
    )
    Semester=list()
    Semester_Credits=list()
    Semester_Credits_Cleared=list()
    SPI=list()
    Total_Credits=list()
    Total_Credits_Cleared=list()
    CPII=list()
    helper=0
    for sem in range(1,total_semester+1):
        Semester.append(sem)
        semwise=datafile[(datafile['semester']==sem)]
        credit_array=list(semwise['credit_obtained'].apply(grade_to_score))
        totalcredits=list(semwise['total_credits'])

        a=0
        for x in range(0,len(credit_array)):
            a+=credit_array[x]*totalcredits[x]
        helper=helper+a
        totalcredits_till = totalcredits_till + semwise['total_credits'].sum()
        Semester_Credits.append(semwise['total_credits'].sum())
        Semester_Credits_Cleared.append(semwise['total_credits'].sum())
        SPI.append(round(a/semwise['total_credits'].sum(),2))
        Total_Credits.append(totalcredits_till)
        Total_Credits_Cleared.append(totalcredits_till)
        CPII.append(round(helper/totalcredits_till,2))
    dict={'Semester':Semester,'Semester Credits':Semester_Credits,'Semester_Credits_Cleared':Semester_Credits_Cleared,'SPI':SPI,
          'Total Credits':Total_Credits,'Total Credits Cleared':Total_Credits_Cleared,'CPI':CPII}
    df=pd.DataFrame(dict)
    filename="grades/"+str(xyz)+"_overall.csv"
    df.to_csv(filename)
    print(Roll_numbers)
    print('done')
