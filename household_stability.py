"""
author: Gonzalo
date started: 24/10/18

This script generates a list of households for every individual present in all waves.

Note: takes a long time to run.

Things to do:
-load hidp file and compare number of members in hh
"""
import pandas as pd 
from random import sample

# name of files/waves to compare
filelist = ["a_indall.tab", "b_indall.tab", "c_indall.tab", 
"d_indall.tab", "e_indall.tab", "f_indall.tab", "g_indall.tab"]

def longevity(filelist):
    """ List of individuals that are present in all waves """
    pidp_dic = {}
    wc=1
    for name in filelist:
        print("Loading wave %d data..." % wc)
        df = pd.read_csv(name, sep='\t')
        pidp_dic[str(wc)] = df['pidp']
        wc+=1
    
    id_int = set(pidp_dic['2']).intersection(set(pidp_dic['1']))
    for n in range(3,len(filelist)+1):
        id_int = set(pidp_dic[str(n)]).intersection(id_int)
    return id_int

if 'id_list' not in vars():
    print("Generating id_list...")
    id_list = longevity(filelist)
else:
    print("id_list already present")

def household_id_list(filelist, pidp):
    """ For a set of waves, obtain a list of household IDs belonging to the same individual. """

    hidp_list = []
    wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}
    c=1
    for name in filelist:
        df = pd.read_csv(name, sep='\t')
        kword = wn[c]+'_hidp'
        hidp = df.loc[df['pidp'] == pidp, kword].values
        hidp_list.extend(hidp)
        c+=1
    return hidp_list

c = 0
house_dic = {}
for pidp in id_list:
    c +=1
    if c > 10:
        break
    else:
        house_dic[str(pidp)] = household_id_list(filelist, pidp)
        print("Individual %d ... done" % pidp)
