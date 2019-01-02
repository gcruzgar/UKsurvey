#!/usr/bin/env python3
import pandas as pd 
import numpy as np
import argparse
from common import remap, constrain, transitions
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.mode.chained_assignment = None # supress SettingWithCopyWarning - False positive when using remap

def census_map(data, var_name, wave):
    """ map survey data to census"""

    waveletter = chr(96+wave) # 1 -> "a" etc

    var_map = {
        '_hhtype_dv' : {
            1: 0, 2: 0, 3: 0, # single occ
            4: 3, 5: 3, # single parent
            6: 1, 8: 1, 10: 1, 11: 1, 12: 1, 19: 1, 20: 1, 21: 1, # couples
            16: 4, 17:4, 18: 4, 22: 4, 23: 4 # mixed
        },
        '_tenure_dv' : { 1: 0, # 2 (owned) in census
            2: 1, # 3 (mortgaged) in census
            3: 2, 4: 2, # 5 (rented social) in census
            5: 3, 6: 3, 7: 3 # 6 (rented private) in census
        }
    }

    var_con = {
        '_hsrooms': [1,6],
        '_hsbeds': [1,4],
        '_hhsize': [1,4]
    }

    if var_name in var_map.keys():

        data = remap(data, waveletter+var_name, var_map[var_name])

        if var_name == '_hhtype_dv':
            couples = data.index[data[waveletter+var_name] == 1].tolist()
            np.random.seed(9238456) # set seed to always get the same "random" numbers
            to_change = np.random.choice(couples, size = round(0.25*len(couples)), replace=False)
            data.loc[to_change, waveletter+var_name] = 2

    if var_name in var_con.keys():

        if var_name == '_hsbeds':  # Census automatically turns 0 beds into 1
            data[waveletter+'_hsbeds'] = np.maximum(data[waveletter+'_hsbeds'], 1)  
        if var_name == '_hsrooms': # Rooms excl. bedrooms -> to rooms incl. beds, i.e. total 
            data[waveletter+'_hsrooms'] = data[waveletter+'_hsrooms'] + data[waveletter+'_hsbeds']

        data = constrain(data, waveletter+var_name, var_con[var_name][0], var_con[var_name][1], shift=-1)

    return data

def main ():

    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:                             # catch variables without underscore
        var_name = '_'+args.var_name
    print("\nvariable: %s" % var_name)
    if args.r:
        print("remap selected")   
        
    # household response data - only keep required variables (files are too big to store in memory)
    print("Loading household data...\n")
    var_dict = {}
    for wave in range(1,8):

        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        
        if var_name != '_hsrooms':
            data = data[[waveletter+'_hrpid', waveletter+var_name]]
        else:
            data = data[[waveletter+'_hrpid', waveletter+var_name, waveletter+'_hsbeds']]

        # mapping to census category values
        if args.r:
            data = census_map(data, var_name, wave)
        
        var_dict[wave] = data.set_index(waveletter+'_hrpid')

    # possible states
    states = var_dict[1]['a'+var_name].unique()
    states = np.sort(states)
    
    # transitions from wave w to wave w+1
    print("Calculating average transition probabilities...")
    tpm = pd.DataFrame()
    for in_state in states:
        t_ave = pd.DataFrame()
        t_ave[in_state] = transitions(var_name, in_state, var_dict)[1]
        tpm = pd.concat([tpm, t_ave], axis=1)

    tpm = tpm.fillna(value=0) # display missing transitions as zero percentage
    tpm.index.name = 'final state'  
    tpm.columns.name = 'initial state'
    tpm = tpm.T # Transpose matrix

    print(tpm.round(2))

    # plot probabilities
    ax = sns.heatmap(tpm, linewidth=.5, cmap="GnBu", annot=True, cbar_kws={'label':'Percentage (%)'})
    ax.set_title('Average Transition Probabilities')
    plt.show()

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
        help= "save output to csv")
    parser.add_argument("-r", action='store_true',
        help= "remap variable to census definitions" )      
    args = parser.parse_args()
     
    main()