#!/usr/bin/env python3
import pandas as pd 

def hh_list():

    data = pd.read_csv('data/xwaveid.tab', sep ='\t')
    hidp_list = data[['pidp', 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']]

    hidp_list.to_csv('data/xwave_hh_list.csv')
    return hidp_list

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

hidp_list = hh_list()  #.dropna(how='any') to obtain list of individuals in all waves

waves = [1,2,3,4,5,6,7]
var_name = '_hhsize'

print("Extracting %s..." % var_name)
hh_var_dict = {}
for wave in waves:
    hh_var = extract_var(wave, var_name)
    hh_var_dict[wave] = hh_var
