#!/usr/bin/env python3
import pandas as pd 

data = pd.read_csv('data/xwaveid.tab', sep ='\t')
hh_list = data[['pidp', 'a_hidp', 'b_hidp', 'c_hidp', 'd_hidp', 'e_hidp', 'f_hidp', 'g_hidp']]

hh_list.to_csv('data/xwave_hh_list.csv')