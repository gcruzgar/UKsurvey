#!/usr/bin/env python3
"""
This script generates a dataframe with person identifiers as rows and a variable, such as w_hhsize, as columns.
The variable of interest can be specified as well as whether to filter results by age or gender.
"""
import pandas as pd 
import argparse
from common import hh_list, track_hh

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
