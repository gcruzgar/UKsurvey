"""
author: Gonzalo
date started: 19/10/18

This script tracks the evolution of an individual over time.
It outputs their marital status at each wave.

Things to do:
-try other variables.
-see if a change in variable value results in any changes in the household. 
"""

import pandas as pd 
from random import randint, sample

filename1 = "a_indresp.tab"
filename2 = "b_indresp.tab"

#pidp = 

filelist = ["a_indresp.tab", "b_indresp.tab", "c_indresp.tab", 
"d_indresp.tab", "e_indresp.tab", "f_indresp.tab", "g_indresp.tab"]

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
    for n in range(3,len(filelist)):
        id_int = set(pidp_dic[str(n)]).intersection(id_int)
    return id_int

if 'id_list' not in vars():
    id_list = longevity(filelist)
    print("id_list ready")
else:
    print("id_list already present")

def track_event(filename1, filename2, pidp = None):
    """ Compare the state of an individual at different times. 
    Will choose an individual at random if one is not specified. """
    
    if pidp == None:
        if 'id_list' not in globals():
            print("id_list not found. Generating list...")
            id_list = longevity(filelist)
        pidp = sample(id_list, 1)[0]
        print("Random individual chosen. Id: %d" % pidp)

    m_evol = []
    wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}
    c=1
    for name in filelist:
        print("Loading wave %d data..." % c)
        df = pd.read_csv(name, sep='\t') 
        kword = wn[c]+'_mlstat'
        mlstat = df.loc[df['pidp'] == pidp, kword].values
        m_evol.append(mlstat)
        c+=1

    marital_status = {1: "single, never married/in civil partnership", 2: "married",
        3: "civil partner", 4: "separated from spouse",
        5: "divorced", 6: "widowed",
        7: "separated from civil partner", 8: "former civil partner",
        9: "surviving civil partner", -1: "don't know",
        -9: "missing", -8: "inapplicable",
        -7: "proxy", -2: "refusal"}

    print("Individual %d started as '%s' and finished as '%s'" % (pidp, marital_status[m_evol[0].item()], marital_status[m_evol[6].item()]))
    return m_evol

m_evol = track_event(filename1, filename2)
