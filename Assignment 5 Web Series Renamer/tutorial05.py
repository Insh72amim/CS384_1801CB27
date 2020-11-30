import os
import re

episode_pd = 2
season_pd = 2


def rm_zero(s):
    '''
    Fn to remove leading zero in numbers
    '''
    s = s.strip()
    for i in range(len(s)):
        if s[i] !='0':
            return s[i:]


#considering folder in current dir
def rename_FIR(folder_name):
    path = os.path.join(os.getcwd(),os.path.join('Subtitles',folder_name))
    try:
        for file in os.listdir(path):
            name = file.split('-')
            name = [i.strip() for i in name]
            # print(file)
            i = ''
            for s in name[1:]:
                if 'Episode' in s:
                    i = s
                    break
            episode = (episode_pd - len(rm_zero(i.split()[1])))*'0' + rm_zero(i.split()[1])
            ext = name[-1].split('.')[-1]
            file_name = name[0] +" Episode " + episode + "." + ext
            file_name_old = os.path.join(path,file)
            file_name = os.path.join(path,file_name)
            try:
                os.rename(file_name_old,file_name)
            except:
                os.remove(file_name_old)
    except:
        pass


def rename_Game_of_Thrones(folder_name):
    # rename Logic


def rename_Sherlock(folder_name):
    # rename Logic


def rename_Suits(folder_name):
    # rename Logic


def rename_How_I_Met_Your_Mother(folder_name):
    # rename Logic
