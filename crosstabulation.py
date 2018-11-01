import pandas as pd 
from collections import Counter

dim_keys = ['_hhtype_dv', '_tenure_dv', '_hsbeds', '_hsrooms','_hhsize']
cols = ['type', 'tenure', 'beds', 'rooms', 'size', 'count']

def contingency_table(wave):

    data_2011 = pd.read_csv(wave + '_hhresp.tab', sep = '\t')

    a = data_2011['wave_hhtype_dv']
    b = data_2011['wave_tenure_dv']
    c = data_2011['wave_hsbeds']
    d = data_2011['wave_hsrooms']
    e = data_2011['wave_hhsize']

    ctab = pd.crosstab(a, [b, c, d, e])
    """ indexing requires unstacking """
    ctab_us = ctab.unstack()
    # print(ctab_us.loc[2,3,4,1,3])

    return ctab, ctab_us

wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}

wave = wn[3]
ctab, ctab_us = contingency_table(wave)

""" to save output: """
# ctab.to_csv("contingency table 2011.csv")
