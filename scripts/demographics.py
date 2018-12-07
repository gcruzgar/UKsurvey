#!/usr/bin/env python3
"""
WIP
"""

import pandas as pd 
import numpy as np 

def hh_list():

    print("Generating household list...")
    data = pd.read_csv('data/xwaveid.tab', sep ='\t')
    hidp_list = data[['pidp', 'sex', 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']]

    # only need one row per household. Drop duplicates caused by multiple members sharing a household.
    hidp_list_unique = hidp_list.drop_duplicates(subset=['a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp'])

    return hidp_list_unique

def extract_var(wave, var_name):

    waveletter = chr(96+wave) # 1 -> "a" etc
    data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
    hh_var = data[[waveletter+'_hidp', waveletter+var_name]]
    return hh_var

def track_hh(sex, waves, var_name, hidp_list):

    hh_row = hidp_list.loc[hidp_list['sex'] == sex] # only keep values with the required demographic
    
    print("Extracting %s..." % var_name)
    
    track_vals = []
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc    

        hh_var = extract_var(wave, var_name) # extract required variable for all households

        w_val = hh_var.loc[hh_var[waveletter+'_hidp'] == hh_row[waveletter+'_hidp'].item(), waveletter+var_name].values #extract value for the hh at that wave
        if w_val.size == 0: #if the household wasn't present in a wave, set it's value to '-9'
            w_val = [-9]
        track_vals.extend(w_val)  
    
    return track_vals
