#!/usr/bin/env python3
"""
This script generates a dataframe with the value of a chosen parameter of any given household over time.
There is the option to save a list of households IDs to CSV. 
This will generate a file where each row is the IDs of a household at every wave.
"""
import pandas as pd 
import numpy as np 

def hh_list():

    print("Generating household list...")
    data = pd.read_csv('data/xwaveid.tab', sep ='\t')
    hidp_list = data[['pidp', 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']]

    #hidp_list.to_csv('data/xwave_hh_list.csv')
    return hidp_list

def extract_var(wave, var_name):

    waveletter = chr(96+wave) # 1 -> "a" etc
    data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
    hh_var = data[[waveletter+'_hidp', waveletter+var_name]]
    return hh_var

def track_hh(pidp, waves, var_name):
    """ 
    Track households over time. Read the hidps for a hh and extract their corresponding values of hh_var.
    Outputs the values for the chosen variable for any given number of waves. 
    """
    hidp_list = hh_list() # obtain list of household ids to match each hh

    print("Extracting %s..." % var_name)
    hh_var_dict = {}    #pd.DataFrame()
    for wave in waves:
        hh_var = extract_var(wave, var_name)  #.set_index(waveletter+'_hidp')
        hh_var_dict[wave] = hh_var

    hh_row = hidp_list.loc[hidp_list['pidp'] == pidp] # household the individual is a member off in each wave 

    track_vals = []
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc       
        val_df = hh_var_dict[wave] #variable values for a given wave
        w_val = val_df.loc[val_df[waveletter+'_hidp'] == hh_row[waveletter+'_hidp'].item(), waveletter+'_hhsize'].values #extract value for the hh at that wave
        if w_val.size == 0: #if the household wasn't present in a wave, set it's value to '-9'
            w_val = [-9]
        track_vals.extend(w_val)  

    first_appearance = next(i for i, v in enumerate(track_vals) if v != -9)
    last_appearance = next(i for i, v in enumerate(reversed(track_vals)) if v != -9)

    print("Household first present in wave %d." % (first_appearance+1))
    print("Household last present in wave %d." % (len(track_vals)-last_appearance))
    print("Initial household value: %d" % track_vals[first_appearance])
    print("Final household value: %d" % track_vals[len(track_vals)-(last_appearance+1)])
    
    return track_vals

def main(): 

    pidp = 280165           # individual (needed to match households)
    waves = [1,2,3,4,5,6,7] # waves to include
    var_name = '_hhsize'    # variable to extract
    
    track_vals = track_hh(pidp, waves, var_name)

    # generate dataframe for easier data handling
    track_df = pd.DataFrame(data=[pidp], columns=['pidp']) 
    for wave in waves: 
        waveletter = chr(96+wave) # 1 -> "a" etc
        track_df[waveletter+var_name] = track_vals[wave-1]
    print(track_df)

if __name__ == "__main__":
    
    main()