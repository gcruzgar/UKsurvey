#!/usr/bin/env python3
import pandas as pd 
import argparse


def main ():

    waves = [1,2,3,4,5,6,7]

    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:                             # catch variables without underscore
        var_name = '_'+args.var_name
    print("\nvariable: %s" % var_name)

    in_state = args.in_state          # value of initial state
    print("Initial state: %d\n" % in_state)

    print("Loading household data...\n")
    # household response data - only keep required variables (files are too big to store in memory)
    var_dict = {}
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        var_dict[wave] = data[[waveletter+'_hrpid', waveletter+var_name]].set_index(waveletter+'_hrpid')

    ij_df = pd.concat([var_dict[1], var_dict[2]], axis=1, join='inner')

    tdf = ij_df.loc[ij_df['a'+var_name] == in_state]
    t = tdf['b'+var_name].value_counts()

    t_perc = t/sum(t) * 100
    print(t_perc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("var_name", type=str, nargs='?', default='_hhtype_dv',
        help="variable of interest to extract. must be in hhresp.tab. type without wave prefix 'w', e.g. _hhtype_dv")   
    parser.add_argument("in_state", type=int, nargs='?', default = 3,
        help="numerical value of initial state")     
    args = parser.parse_args()
     
    main()
