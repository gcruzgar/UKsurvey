"""
author: Gonzalo
date started: 19/10/18

This script creates a list of individuals that are present in all specified waves.
It selects one of these individuals at random and tracks their evolution over time.
It outputs the status of the chosen variable at each wave.

Things to do:
-see if a change in variable value results in any changes in the household. 
-create dictionary with possible values for each variable.
"""

import pandas as pd 
from random import sample

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
    for n in range(3,len(filelist)+1):
        id_int = set(pidp_dic[str(n)]).intersection(id_int)
    return id_int

if 'id_list' not in vars():
    print("Generating id_list...")
    id_list = longevity(filelist)
else:
    print("id_list already present")

def track_event(filelist, var_key, possible_status, id_list = None, pidp = None):
    """ Compare the state of an individual at different times. 
    Will choose an individual at random if one is not specified. """
    
    if pidp == None:
        if 'id_list' not in globals():
            print("id_list not found. Generating list...")
            id_list = longevity(filelist)
        pidp = sample(id_list, 1)[0]
        print("Random individual chosen. Id: %d\n" % pidp)

    var_evol = []
    wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}
    c=1
    for name in filelist:
        print("Loading wave %d data..." % c)
        df = pd.read_csv(name, sep='\t') 
        kword = wn[c] + var_key
        v = df.loc[df['pidp'] == pidp, kword].values
        var_evol.extend(v)
        c+=1

    print("\nIndividual %d started as '%s' and finished as '%s'" % (pidp, possible_status[var_evol[0]], possible_status[var_evol[6]]))
    return var_evol

#var_key = '_mlstat'
#possible_status = {1: "single, never married/in civil partnership", 2: "married",
#    3: "civil partner", 4: "separated from spouse", 5: "divorced", 6: "widowed",
#    7: "separated from civil partner", 8: "former civil partner", 
#    9: "surviving civil partner", -1: "don't know", -9: "missing", 
#    -8: "inapplicable", -7: "proxy", -2: "refusal"}

var_key = '_jbstat'
possible_status = {1: "self employed", 2: "in paid employment",
    3: "unemployed", 4: "retired", 5: "on maternity leave", 6: "looking after family or home",
    7: "full-time student", 8: "long-term isck or disabled", 9: "on a government training scheme",
    10: "unpaid worker in family business", 97: "doing something else", -1: "don't know", 
    -9: "missing", -8: "inapplicable", -7: "proxy", -2: "refusal"}

var_evol = track_event(filelist, var_key, possible_status, id_list)
