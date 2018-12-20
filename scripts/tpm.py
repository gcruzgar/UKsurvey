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

# def remap(table, column, mapping):
#     """ Remaps to values in mapping and discards unmapped values """

#     # first remove any values that are not keys in the mapping
#     table = table[table[column].isin(mapping.keys())]
#     # now map the values
#     table[column].replace(mapping, inplace=True)
    
#     hhtype_map = {
#         1: 0, 2: 0, 3: 0, # single occ
#         4: 3, 5: 3, # single parent
#         6: 1, 8: 1, 10: 1, 11: 1, 12: 1, 19: 1, 20: 1, 21: 1, # couples
#         16: 4, 17:4, 18: 4, 22: 4, 23: 4 # mixed
#     }

#     tenure_map = { 1: 0, # 2 (owned) in census
#       2: 1, # 3 (mortgaged) in census
#       3: 2, 4: 2, # 5 (rented social) in census
#       5: 3, 6: 3, 7: 3 # 6 (rented private) in census
#     }

#     # constrain within range then shift
#     data = constrain(data, waveletter+'_hsrooms', 1, 6, shift=-1)
#     data = constrain(data, waveletter+'_hsbeds', 1, 4, shift=-1)
#     data = constrain(data, waveletter+'_hhsize', 1, 4, shift=-1)

#     return table

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

    tpm = tpm.fillna(value=0) # display missing transitions as zero percentage
    tpm.index.name = 'final state'  
    tpm.columns.name = 'initial state'
    tpm = tpm.T # Transpose matrix

    print(tpm.round(2))

    # export table to csv
    if args.s:
        out_dir = "data/w"+var_name+"-tpm.csv"
        tpm.to_csv(out_dir)
        print("\n Table saved to '%s'." % out_dir)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default='_hhtype_dv',
        help="variable of interest to extract. must be in hhresp.tab. type without wave prefix 'w', e.g. _hhtype_dv")
    parser.add_argument("-s", action='store_true',
        help = "save output to csv")      
    args = parser.parse_args()
     
    main()