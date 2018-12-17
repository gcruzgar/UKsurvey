#!/usr/bin/env python3
import pandas as pd 

def main ():

    var_name = '_hhtype_dv'
    var_val = 3

    adf  = pd.read_csv("data/a_hhresp.tab", sep ='\t')
    adf = adf[['a_hrpid', 'a'+var_name]].set_index('a_hrpid')

    bdf  = pd.read_csv("data/b_hhresp.tab", sep ='\t')
    bdf = bdf[['b_hrpid', 'b'+var_name]].set_index('b_hrpid')

    ij_df = pd.concat([adf, bdf], axis=1, join='inner')

    tdf = ij_df.loc[ij_df['a'+var_name] == var_val]
    t = tdf['b'+var_name].value_counts()

    t_perc = t/sum(t) * 100
    print(t_perc)

if __name__ == "__main__":
    
    main()
