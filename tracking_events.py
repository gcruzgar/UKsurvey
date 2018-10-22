"""
author: Gonzalo
date started: 19/10/18

This script tracks the evolution of an individual over time.
It outputs their marital status at each wave.

Things to do:
-add more waves and store output as timeseries.
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

    print("\nLoading data...")
    df1 = pd.read_csv(filename1, sep='\t')
    df2 = pd.read_csv(filename2, sep='\t')
    print("Complete")
    if pidp == None:
        if 'id_list' in vars():
            pidp = sample(id_list, 1)
        else:
            while pidp == None:
                r = randint(0, len(df1))
                if r in df2['pidp']:
                    pidp = df1['pidp'][r]
        print("Random individual chosen. Id: %d" % pidp)

    mlstat_1 = df1.loc[df1['pidp'] == pidp, 'a_mlstat'].item()
    mlstat_2 = df2.loc[df2['pidp'] == pidp, 'b_mlstat'].item()

    m_evol = [mlstat_1, mlstat_2]

    marital_status = {1: "single, never married/in civil partnership", 2: "married",
        3: "civil partner", 4: "separated from spouse",
        5: "divorced", 6: "widowed",
        7: "separated from civil partner", 8: "former civil partner",
        9: "surviving civil partner", -1: "don't know",
        -9: "missing", -8: "inapplicable",
        -7: "proxy", -2: "refusal"}

    print("Individual %d went from %s to %s" % (pidp, marital_status[mlstat_1], marital_status[mlstat_2]))
    return m_evol

m_evol = track_event(filename1, filename2)
