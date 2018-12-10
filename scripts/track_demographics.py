#!/usr/bin/env python3
import pandas as pd 
import argparse

def hh_list(filter_var):

    print("Generating household list...")
    data = pd.read_csv('data/xwaveid.tab', sep ='\t')
    data = data.loc[data['fwintvd_dv'] != -8.0]  # drop any BHPS households not present in UKHLS, i.e. if first wave interview (UKHLS) is inapplicable. 
    hidp_list = data[['pidp', filter_var, 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']] # only save households ids and filter variable
    
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

    filter_var = args.filter_var  # demographic variable to filter on
    filter_val = args.filter_val      # value of filter variable

    print("\nfilter: %s" % filter_var)
    print("value: %d\n" % filter_val)

    hidp_list = hh_list(filter_var) # obtain list of household ids to match each hh

    pidp_list = hidp_list.loc[hidp_list[filter_var] == filter_val, 'pidp'].head(10) # individuals (needed to match households)
    waves = [1,2,3,4,5,6,7]                      # waves to include
    var_name = '_hhsize'                         # variable to extract  

    print("Extracting variable data...")
    var_dict = {}
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        var_dict[wave] = data[[waveletter+'_hidp', waveletter+var_name]]

    track_dict = {}
    for pidp in pidp_list:

        track_dict[pidp]  = track_hh(pidp, waves, var_name, hidp_list, var_dict)    

    #convert to dataframe for easier visualisation
    track_df = pd.DataFrame.from_dict(track_dict, orient='index', columns = ['a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp'])
    print("\n")
    print(track_df)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("filter_var", type=str, help="demographic variable to filter on. the chosen variable must be in xwaveid.tab", 
        nargs='?', default='sex')
    parser.add_argument("filter_val", type=int, help="value of filter variable", 
        nargs='?', default=1)        
    args = parser.parse_args()

    main()
