import pandas as pd 
from collections import Counter

dim_keys = ['_hhtype_dv', '_tenure_dv', '_hsbeds', '_hsrooms','_hhsize']
cols = ['type', 'tenure', 'beds', 'rooms', 'size', 'count']

def contingency_table(wave):

    data = pd.read_csv(wave + '_hhresp.tab', sep = '\t')

    a = data[wave+'_hhtype_dv']
    b = data[wave+'_tenure_dv']
    c = data[wave+'_hsbeds']
    d = data[wave+'_hsrooms']
    e = data[wave+'_hhsize']

    ctab = pd.crosstab(a, [b, c, d, e])
    """ indexing requires unstacking """
    ctab_us = ctab.unstack()
    # print(ctab_us.loc[2,3,4,1,3])

    return ctab, ctab_us

""" data processing """
def data_filter(wave, use_ctab_us = False, filename = None):
    if filename == None:
        filename = "Unstacked cross tabulation - wave "+wave+".csv"
    if use_ctab_us == False:
        wave_df = pd.read_csv(filename)
    else:
        wave_df = ctab_us
    wave_df = wave_df[wave_df['count']!=0]
    wave_df = wave_df[wave_df[wave+'_tenure_dv']>0]
    wave_df = wave_df[wave_df[wave+'_hsbeds']>0]
    wave_df = wave_df[wave_df[wave+'_hsrooms']>0].reset_index()
    return wave_df

wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}
wave = wn[3] # select wave

ctab, ctab_us = contingency_table(wave) # create contingency table
wave_df = data_filter(wave) # filter table

""" to save output: """
# ctab.to_csv("test.csv")
