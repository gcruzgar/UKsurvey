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

def track_hh(sex, waves, var_name):

    hidp_list = hh_list() # obtain list of household ids to match each hh

    print("Extracting %s..." % var_name)
    hh_var_dict = {}    #pd.DataFrame()
    for wave in waves:
        hh_var = extract_var(wave, var_name)  #.set_index(waveletter+'_hidp')
        hh_var_dict[wave] = hh_var

    hh_rows = hidp_list.loc[hidp_list['sex'] == sex] # households within a given demographic

    
    return track_vals