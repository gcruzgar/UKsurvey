#!/usr/bin/env python3
"""
Objectives:
for any given variable:
    the final result should either print the evolution of a household over time, similar to that in tracking_events.py
    e.g. print("\nHousehold %d started as '%s' and finished as '%s'")

    or create a dataframe with pidp (one individual per household) and the value of the variable at each year
    e.g. |pidp|a_var|b_var|c_var|d_var|e_var|f_var|
         |100 |1    |1    |1    |2    |2    |2    |
"""
import pandas as pd 

def hh_list():

    data = pd.read_csv('data/xwaveid.tab', sep ='\t')
    hh_list = data[['pidp', 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']]

    hh_list.to_csv('data/xwave_hh_list.csv')
    return hh_list

def extract_var(wave, var_name):

    waveletter = chr(96+wave) # 1 -> "a" etc
    data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
    hh_var = data[[waveletter+'_hidp', waveletter+var_name]]
    return hh_var

def track_hh():
    # the idea is to track households over time
    # obtain a dataframe with values of the chosen variable for every household
    # read the hidps for a hh and extract their corresponding values of hh_var
    pass

hh_list = hh_list()  #.dropna(how='any') to obtain list of individuals in all waves

waves = [1,2,3,4,5,6,7]
var_name = '_hhsize'

print("Extracting %s..." % var_name)
hh_var_dict = {}    #pd.DataFrame()
for wave in waves:
    hh_var = extract_var(wave, var_name)  #.set_index(waveletter+'_hidp')
    hh_var_dict[wave] = hh_var

pidp = 280165
hh_row = hh_list.loc[hh_list['pidp'] == pidp]

b_val = hh_var_dict[2].loc[hh_var_dict[2]['b_hidp'] == hh_row['b_hidp'].item(), 'b_hhsize'].item() 
#track_vals = [pidp, a_val, b_val ...]