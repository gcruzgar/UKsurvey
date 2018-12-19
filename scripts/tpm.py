#!/usr/bin/env python3
import pandas as pd 
import numpy as np
import argparse

def transitions(var_name, in_state, var_dict):
    """
    percentage distributions of transitions from in_state in wave w to any state in wave w+1
    """

    t_perc_df = pd.DataFrame()
    for wave in range(1,7):
        
        ij_df = pd.concat([var_dict[wave], var_dict[wave+1]], axis=1, join='inner') # inner join between wave w1 and w2

        w1 = chr(96+wave)
        w2 = chr(97+wave)

        is_df = ij_df.loc[ij_df[w1+var_name] == in_state]   # frequency of state in w2 given state in_state in w1
        t = is_df.groupby(w2+var_name)[w2+var_name].count()   

        t_perc_df[w1+w2] = t/sum(t) * 100
        
    t_perc_df = t_perc_df.fillna(value=0)
    t_ave = t_perc_df.mean(axis=1)

    return t_ave

def main ():

    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:                             # catch variables without underscore
        var_name = '_'+args.var_name
    print("\nvariable: %s" % var_name)
       
    # household response data - only keep required variables (files are too big to store in memory)
    print("Loading household data...\n")
    var_dict = {}
    for wave in range(1,8):

        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        var_dict[wave] = data[[waveletter+'_hrpid', waveletter+var_name]].set_index(waveletter+'_hrpid')

    # possible states
    states = var_dict[1]['a'+var_name].unique()
    states = np.sort(states)
    
    # transitions from wave w to wave w+1
    print("Calculating average transition probabilities...")
    tpm = pd.DataFrame()
    for in_state in states:
        t_ave = pd.DataFrame()
        t_ave[in_state] = transitions(var_name, in_state, var_dict)
        tpm = pd.concat([tpm, t_ave], axis=1)

    tpm = tpm.fillna(value=0)         # display missing transitions as zero percentage
    tpm = tpm.T                       # Transpose matrix
    tpm.index.name = 'initial state'  # or final_state if not transposed
    print(tpm.round(2))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default='_hhtype_dv',
        help="variable of interest to extract. must be in hhresp.tab. type without wave prefix 'w', e.g. _hhtype_dv")      
    args = parser.parse_args()
     
    main()