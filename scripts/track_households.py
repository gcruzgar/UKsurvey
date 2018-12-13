#!/usr/bin/env python3
"""
This script generates a dataframe with person identifiers as rows and a variable, such as w_hhsize, as columns.
The variable of interest can be specified as well as whether to filter results by age or gender.
"""
import pandas as pd 
import argparse

def hh_list():
    """
    Generate a dataframe with the w_hidp corresponding to each pidp, 
    as well as the sex and year of birth for filtering purposes.
    """
    print("Generating household list...")
    data = pd.read_csv('data/xwaveid.tab', sep ='\t')
    data = data.loc[data['fwintvd_dv'] != -21.0]  # drop any entries with no data from UKHLS. 

    # only save households ids and variables needed for filtering
    hidp_list = data[['pidp', 'sex', 'birthy', 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']]
  
    # only need one row per household. Drop duplicates caused by multiple members sharing a household.
    hidp_list = hidp_list.drop_duplicates(subset=['a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp'])

    return hidp_list

def track_hh(pidp, waves, var_name, hidp_list, var_dict):
    """ 
    Track households over time. Read the hidps for a hh and extract their corresponding values of hh_var.
    Outputs the values for the chosen variable for any given number of waves. 
    """

    hh_row = hidp_list.loc[hidp_list['pidp'] == pidp] # household the individual is a member off in each wave 
    
    track_vals = []
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc    

        hh_var = var_dict[wave]
           
        w_val = hh_var.loc[hh_var[waveletter+'_hidp'] == hh_row[waveletter+'_hidp'].item(), waveletter+var_name].values #extract value for the hh at that wave
        if w_val.size == 0: #if the household wasn't present in a wave, set it's value to '-9'
            w_val = [-9]
        track_vals.extend(w_val)  
    
    return track_vals

def main():

    hidp_list = hh_list()             # obtain list of household ids to match each hh

    waves = [1,2,3,4,5,6,7]           # waves to include
    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:                             # catch variables without underscore
        var_name = '_'+args.var_name
    print("\nvariable: %s" % var_name)
    if args.s:
        s_val = args.s                # sex
        print("sex: %s" % s_val)
        hidp_list = hidp_list.loc[(hidp_list['sex'] == s_val)]
    if args.b:
        b_val = args.b                # year of birth
        print("year of birth: %d" % b_val) 
        hidp_list = hidp_list.loc[(hidp_list['birthy'] == b_val)]

    # Individuals (needed to match households). Only process for first 200 values.
    pidp_list = hidp_list['pidp'].head(200) 

    print("\nExtracting variable data...")
    var_dict = {}
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        var_dict[wave] = data[[waveletter+'_hidp', waveletter+var_name]]

    track_dict = {}
    for pidp in pidp_list:

        track_dict[pidp]  = track_hh(pidp, waves, var_name, hidp_list, var_dict)    

    #convert to dataframe for easier visualisation
    track_df = pd.DataFrame.from_dict(track_dict, orient='index', columns = ['a'+var_name,  'b'+var_name, 'c'+var_name, 
        'd'+var_name, 'e'+var_name, 'f'+var_name, 'g'+var_name])
    track_df.index.name = 'pidp'

    # drop any households that were only present for 2 waves or less
    drop_index = track_df.index[(track_df == -9).sum(axis=1) >= 0.70*track_df.shape[1]]
    track_df.drop(drop_index, axis=0, inplace=True)
    print(track_df.head(10))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=int, nargs='?', help="sex, 1 for male or 2 for female")
    parser.add_argument("-b", type=int, nargs='?', help="year of birth [YYYY]")
    parser.add_argument("var_name", type=str, nargs='?', default='_hhsize',
        help="variable of interest to extract. must be in hhresp.tab. type without wave prefix 'w', e.g. _hhsize")        
    args = parser.parse_args()

    main()
