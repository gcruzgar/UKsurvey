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
import numpy as np 

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

# for each individual
pidp = 280165 #individual
hh_row = hh_list.loc[hh_list['pidp'] == pidp] #household individual is a member off in each wave 

track_vals = []
for wave in waves:
    waveletter = chr(96+wave) # 1 -> "a" etc
    #print(waveletter)
    val_df = hh_var_dict[wave] #variable values for a given wave
    w_val = val_df.loc[val_df[waveletter+'_hidp'] == hh_row[waveletter+'_hidp'].item(), waveletter+'_hhsize'].values #extract value for the hh at that wave
    if w_val.size == 0:
       w_val = nan
    track_vals.extend(w_val)
    #print(track_vals)

first_appearance = next(i for i, v in enumerate(track_vals) if v != -9)
#last_appearance = next(i for i, v in enumerate(track_vals.reverse) if v != -9) # FIX!
print("Household first present in wave %d." % (first_appearance+1))
#print("Household last present in wave %d." % (last_appearance+1))
print("Initial household value: %d" % track_vals[first_appearance])
#print("Final household value: %d" % track_vals[last_appearance])