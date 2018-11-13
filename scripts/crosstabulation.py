"""
author: Gonzalo
date started: 01/11/18

This script creates 5-dimensional contingency tables.
Also includes the option to unstack the tables and filter the data.
"""
import pandas as pd 
from pathlib import Path
from collections import Counter

data_root_dir = Path("./data")

dim_keys = ['_hhtype_dv', '_tenure_dv', '_hsbeds', '_hsrooms','_hhsize']
cols = ['type', 'tenure', 'beds', 'rooms', 'size', 'count']

def contingency_table(wave):

    waveletter = chr(96+wave) # 1 -> "a" etc
    data = pd.read_csv(data_root_dir / ("UKDA-6614-tab/tab/ukhls_w" + str(wave)) / (waveletter + '_hhresp.tab'), sep = '\t')

    a = data[waveletter+'_hhtype_dv']
    b = data[waveletter+'_tenure_dv']
    c = data[waveletter+'_hsbeds']
    d = data[waveletter+'_hsrooms']
    e = data[waveletter+'_hhsize']

    ctab = pd.crosstab(a, [b, c, d, e])
    """ indexing requires unstacking """
    # unstack returns a multiindex Series not a dataframe
    # so construct a dataframe and make the multiindex into columns so we can filter
    ctab_us = pd.DataFrame({"count": ctab.unstack()}).reset_index()

    return ctab, ctab_us
""" data processing """
def data_filter(wave, wave_df):
    waveletter = chr(wave + 96) # 1 -> 'a' etc
    wave_df = wave_df[(wave_df['count']!=0) 
                    & (wave_df[waveletter+'_tenure_dv']>0) 
                    & (wave_df[waveletter+'_hsbeds']>0) 
                    & (wave_df[waveletter+'_hsrooms']>0)]
    return wave_df

wave = 3 # select wave

ctab, ctab_us = contingency_table(wave) # create contingency table
wave_df = data_filter(wave) # filter table

""" to save output: """
# ctab.to_csv("test.csv")
# ctab_us.to_csv(data_root_dir / ("crosstab_wave" + str(wave) + ".csv"), index=False)
