#!/usr/bin/env python3
import pandas as pd 
import argparse

def main ():
    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:                             # catch variables without underscore
        var_name = '_'+args.var_name
    print("\nvariable: %s" % var_name)

    in_state = args.in_state          # value of initial state
    print("Initial state: %d\n" % in_state)

    adf  = pd.read_csv("data/a_hhresp.tab", sep ='\t')
    adf = adf[['a_hrpid', 'a'+var_name]].set_index('a_hrpid')

    bdf  = pd.read_csv("data/b_hhresp.tab", sep ='\t')
    bdf = bdf[['b_hrpid', 'b'+var_name]].set_index('b_hrpid')

    ij_df = pd.concat([adf, bdf], axis=1, join='inner')

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
