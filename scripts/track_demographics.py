#!/usr/bin/env python3
import pandas as pd 
import numpy as np 

def track_hh(pidp, waves, var_name, hidp_list, var_dict):
    """ 
    Track households over time. Read the hidps for a hh and extract their corresponding values of hh_var.
    Outputs the values for the chosen variable for any given number of waves. 
    """

    hh_row = hidp_list.loc[hidp_list['pidp'] == pidp] # household the individual is a member off in each wave 

    print("Extracting %s..." % var_name)
    
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
    hidp_list = pd.read_csv('data/xwave_hh_list_unique.csv') # obtain list of household ids to match each hh

    pidp_list = list(hidp_list['pidp'].head(10))          # individuals (needed to match households)
    waves = [1,2,3,4,5,6,7] # waves to include
    var_name = '_hhsize'    # variable to extract  

    print("Extracting variable data...")
    var_dict = {}
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        var_dict[wave] = data[[waveletter+'_hidp', waveletter+var_name]]

    track_dict = {}
    for pidp in pidp_list:

        track_dict[pidp]  = track_hh(pidp, waves, var_name, hidp_list, var_dict)    
        print(track_dict[pidp])

    #convert to dataframe for easier visualisation
    track_df = pd.DataFrame.from_dict(track_dict, orient='index', columns = ['a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp'])
    print(track_df)

if __name__ == "__main__":
    main()
