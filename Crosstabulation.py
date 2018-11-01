import pandas as pd 
from collections import Counter

dim_keys = ['c_hhtype_dv', 'c_tenure_dv', 'c_hsbeds', 'c_hsrooms','c_hhsize']
cols = ['type', 'tenure', 'beds', 'rooms', 'size', 'count']

def contingency_table():

    data_2011 = pd.read_csv('c_hhresp.tab', sep = '\t')

    a = data_2011['c_hhtype_dv']
    b = data_2011['c_tenure_dv']
    c = data_2011['c_hsbeds']
    d = data_2011['c_hsrooms']
    e = data_2011['c_hhsize']

    ctab = pd.crosstab(a, [b, c, d, e])
    """ indexing requires unstacking"""
    ctab_us = ctab.unstack()
    # print(ctab_us.loc[2,3,4,1,3])

    return ctab, ctab_us

""" to save output: """
# ctab.to_csv("contingency table 2011.csv")
