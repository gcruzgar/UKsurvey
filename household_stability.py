"""
author: Gonzalo
date started: 24/10/18

This script generates a list of households for every individual present in all waves.

Things to do:
-update to all waves
-load hidp file and compare number of members in hh
"""
import pandas as pd 
from random import sample

# name of files/waves to compare
filename1 = "a_indresp.tab"
filename2 = "b_indresp.tab"

def wave_intercept(filename1, filename2):
    """ Check which individuals from a wave are present in the next wave. """
     
    df1 = pd.read_csv(filename1, sep='\t')
    df2 = pd.read_csv(filename2, sep='\t')

    df1_id = df1['pidp']
    df2_id = df2['pidp']

    #intercept between two lists:
    id_intercept = set(df2_id).intersection(set(df1_id))
    return list(id_intercept)

id_intercept = wave_intercept(filename1,filename2)

filelist = ["a_indresp.tab", "b_indresp.tab"]

def household_id_list(filelist, pidp):
    """ For a set of waves, obtain a list of household IDs belonging to the same individual. """

    hidp_list = []
    wn = {1:'a', 2:'b'}
    c=1
    for name in filelist:
        df = pd.read_csv(name, sep='\t')
        if pidp in df['pidp'].values:
            kword = wn[c]+'_hidp'
            hidp = df.loc[df['pidp'] == pidp, kword].values
            hidp_list.extend(hidp)
        c+=1
    return hidp_list

house_dic = {}
for pidp in id_intercept:
    house_dic[str(pidp)] = household_id_list(filelist, pidp)
    print("Individual %d ... done" % pidp)
