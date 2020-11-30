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

filename = "Btech_2020_master_data.csv"
number_of_groups = 12
group_allocation(filename, number_of_groups)
