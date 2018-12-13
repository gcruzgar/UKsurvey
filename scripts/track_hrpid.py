#!/usr/bin/env python3

import pandas as pd 
import argparse

def track_hh(pidp, waves, var_name, hidp_df, var_dict):
    """ 
    Track households over time. Read the hidps for a hh and extract their corresponding values of hh_var.
    Outputs the values for the chosen variable for any given number of waves. 
    """

    hh_row = hidp_df.loc[hidp_df['pidp'] == pidp] # household the individual is a member off in each wave 
    
    track_vals = []
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc    
        hh_var = var_dict[wave]

        # extract value for the hh at each wave   
        w_val = hh_var.loc[hh_var[waveletter+'_hidp'] == hh_row[waveletter+'_hidp'].item(), waveletter+var_name].values
        if w_val.size == 0: #if the household wasn't present in a wave, set it's value to '-9'
            w_val = [-9]
        track_vals.extend(w_val)  
    
    return track_vals

def main ():

    waves = [1,2,3,4,5,6,7]
    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:                             # catch variables without underscore
        var_name = '_'+args.var_name
    print("\nvariable: %s" % var_name)

    print("\nGenerating household list...")

    # household response data - only keep required variables (files are too big to store in memory)
    var_dict = {}
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        var_dict[wave] = data[[waveletter+'_hidp', waveletter+'_hrpid', waveletter+var_name]]

    # household ids
    hidp_df = pd.read_csv("data/xwaveid.tab", sep='\t')
    hidp_df = hidp_df[['pidp', 'sex', 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']]
    hrpid_df = var_dict[1][['a_hidp', 'a_hrpid']]

    # dataframe with reference person for each household only
    hidp_df = hidp_df.loc[hidp_df['pidp'].isin(hrpid_df['a_hrpid'].values)]

    # option to filter by gender
    if args.s:
        s_val = args.s                
        print("sex: %s" % s_val)
        hidp_df = hidp_df.loc[(hidp_df['sex'] == s_val)]

    print("Extracting variable data...\n")

    track_df = pd.DataFrame()
    for pidp in hidp_df['pidp'].head(100):
        track_df[pidp]  = track_hh(pidp, waves, var_name, hidp_df, var_dict)
    track_df = track_df.T
    track_df.columns = ['a'+var_name,  'b'+var_name, 'c'+var_name, 
            'd'+var_name, 'e'+var_name, 'f'+var_name, 'g'+var_name]
    track_df.index.name = 'hrpid' 

    # drop any households that were only present for 2 waves or less
    drop_index = track_df.index[(track_df == -9).sum(axis=1) >= 0.70*track_df.shape[1]]
    track_df.drop(drop_index, axis=0, inplace=True)
    print(track_df.head(10))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=int, nargs='?', help="sex, 1 for male or 2 for female")
    parser.add_argument("var_name", type=str, nargs='?', default='_hhsize',
        help="variable of interest to extract. must be in hhresp.tab. type without wave prefix 'w', e.g. _hhsize")        
    args = parser.parse_args()

    main()