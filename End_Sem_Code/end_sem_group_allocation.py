import pandas as pd
import re
pattern=re.compile(r'\d+(\D+)\d+')
def group_allocation(filename, number_of_groups):
    datafile = pd.read_csv(filename)
    unique_branches = set()

    for x in datafile['Roll']:
        if pattern.search(x):
            unique_branches.add(pattern.search(x).group(1))

    print(unique_branches)
    files = dict()
    for x in unique_branches:
        files[x] = dict()
        files[x]['Roll'] = list()
        files[x]['Name'] = list()
        files[x]['Email'] = list()

    for post in range(len(datafile['Roll'])):
        branch = pattern.search(datafile['Roll'][post]).group(1)
        files[branch]['Roll'].append(datafile['Roll'][post])
        files[branch]['Name'].append(datafile['Name'][post])
        files[branch]['Email'].append(datafile['Email'][post])

    datastrength = {}
    datastrength['STRENGTH'] = []
    datastrength['BRANCH_CODE'] = []

    for x in unique_branches:
        new_files = {}
        new_files['Roll'] = list()
        new_files['Roll'] = files[x]['Roll'].copy()
        new_files['Name'] = list()
        new_files['Name'] = files[x]['Name'].copy()
        new_files['Email'] = list()
        new_files['Email'] = files[x]['Email'].copy()
        data = pd.DataFrame(new_files)
        data=data.sort_values(['Roll'])
        data.to_csv(x + '.csv')
        datastrength['BRANCH_CODE'].append(x)
        datastrength['STRENGTH'].append(len(files[x]['Roll']))

    newdata = pd.DataFrame(datastrength)
    newdata = newdata.sort_values(['STRENGTH', 'BRANCH_CODE'])

    groupwisedistribution = {}
    post=0
    for x in unique_branches:
        y = len(files[x]['Roll'])
        groupwise = int(y / number_of_groups)
        groupwisedistribution[x] = list()
        for z in range(number_of_groups):
            groupwisedistribution[x].append(groupwise)
        remaining = y % number_of_groups
        post = post % number_of_groups
        for z in range(remaining):
            groupwisedistribution[x][post] += 1
            post=post+1
            post=post%number_of_groups
    groups = {}
    for x in range(number_of_groups):
        groups[x] = {}
        groups[x]['NAME'] = list()
        groups[x]['ROLL'] = list()
        groups[x]['e-MAIL'] = list()
    for x in unique_branches:
        post = 0
        flag = 0
        size = (groupwisedistribution[x][post])
        while post < number_of_groups:

            groups[post]['NAME'].append(files[x]['Name'][flag])
            groups[post]['ROLL'].append(files[x]['Roll'][flag])
            groups[post]['e-MAIL'].append(files[x]['Email'][flag])
            flag = flag + 1
            size -= 1
            if size == 0:
                post = post + 1
                if post < number_of_groups:
                    size = (groupwisedistribution[x][post])


    newdata.to_csv('branch_strength.csv')

filename = "Btech_2020_master_data.csv"
number_of_groups = 12
group_allocation(filename, number_of_groups)
