#!/usr/bin/env python3
"""
author: Gonzalo
date started: 01/11/18

This script creates 5-dimensional contingency tables.
Also includes the option to unstack the tables and filter the data.
Maps survey data to census definitions before unstacking.
"""
import argparse
import pandas as pd 
import numpy as np
from pathlib import Path

data_root_dir = Path("./data")

dim_keys = ['_hhtype_dv', '_tenure_dv', '_hsbeds', '_hsrooms','_hhsize']

def remap(table, column, mapping):
    """ Remaps to values in mapping and discards unmapped values """
    # first remove any values that are not keys in the mapping
    table = table[table[column].isin(mapping.keys())]
    # now map the values
    table[column].replace(mapping, inplace=True)
    return table

def constrain(table, column, minval, maxval, shift=0):
    """ Constrains values like so:
        - removes rows with values < minval
        - caps column values at maxval
        - shift values by shift (e.g. to allow for 0 to mean 1 bedroom)
    """
    table = table[table[column] >= minval]
    table.loc[table[column] > maxval, column] = maxval
    table[column] = table[column] + shift
    return table

def contingency_table(wave):

    waveletter = chr(96+wave) # 1 -> "a" etc
    data = pd.read_csv(data_root_dir / ("UKDA-6614-tab/tab/ukhls_w" + str(wave)) / (waveletter + '_hhresp.tab'), sep = '\t')
    #data = pd.read_csv(data_root_dir / (waveletter+'_hhresp.tab'), sep ='\t')
    # hhsamp = pd.read_csv(data_root_dir / (waveletter+'_hhsamp.tab'), sep ='\t')

    # Rooms excl. bedrooms -> to rooms incl. beds, i.e. total 
    data[waveletter+'_hsrooms'] = data[waveletter+'_hsrooms'] + data[waveletter+'_hsbeds']
    # Census automatically turns 0 beds into 1 bed (do this without impacting total)
    data[waveletter+'_hsbeds'] = np.maximum(data[waveletter+'_hsbeds'], 1)

    # mapping to census category values
    tenure_map = { 1: 0, # 2 (owned) in census
               2: 1, # 3 (mortgaged) in census
               3: 2, 4: 2, # 5 (rented social) in census
               5: 3, 6: 3, 7: 3 # 6 (rented private) in census
             }
    data = remap(data, waveletter+'_tenure_dv', tenure_map)
    # constrain within range then shift
    data = constrain(data, waveletter+'_hsrooms', 1, 6, shift=-1)
    data = constrain(data, waveletter+'_hsbeds', 1, 4, shift=-1)
    data = constrain(data, waveletter+'_hhsize', 1, 4, shift=-1)

    hhtype_map = {
        1: 0, 2: 0, 3: 0, # single occ
        4: 3, 5: 3, # single parent
        6: 1, 7: 2, 8: 1, 9: 2, 10: 1, 11: 2, 12: 1, 19: 2, 20: 1, 21: 2, # couples (alternating between married/cohabiting)
        16: 4, 17:4, 18: 4, 22: 4, 23: 4 # mixed
    }
    data = remap(data, waveletter+'_hhtype_dv', hhtype_map)

    #data[waveletter+'_tenure_dv'].replace(tenure_map, inplace=True)

    a = data[waveletter+'_hhtype_dv']
    b = data[waveletter+'_tenure_dv']
    c = data[waveletter+'_hsbeds']
    d = data[waveletter+'_hsrooms']
    e = data[waveletter+'_hhsize']
    # f = hhsamp[waveletter+'_dweltyp']

    ctab = pd.crosstab(a, [b, c, d, e]) #add ',f' after 'e' too include dwelling 
    """ indexing requires unstacking """
    # unstack returns a multiindex Series not a dataframe
    # so construct a dataframe and make the multiindex into columns so we can filter
    ctab_us = pd.DataFrame({"count_value": ctab.unstack()}).reset_index()

    """ rename columns so they are consistent between files """
    ctab_us.columns = ['tenure', 'beds', 'rooms', 'occupants', 'hhtype', 'count_value'] # add 'dwelling' after size if included in data
    return ctab_us

""" data processing """
def data_filter(wave_df):
    return wave_df.loc[(wave_df['count_value']!=0)]
                    # & (wave_df['dwelling']>0]

def main():

    wave = 3 # select wave

    ctab_us = contingency_table(wave) # create contingency table
    wave_df = data_filter(ctab_us) # filter table

    """ to save output: """
    # ctab.to_csv("test.csv")
    # ctab_us.to_csv(data_root_dir / ("crosstab_wave" + str(wave) + ".csv"), index=False)

    """ automated """
    for wave in range(1,8):
        ctab_us = contingency_table(wave) # create contingency table
        wave_df = data_filter(ctab_us) # filter table 
        wave_df.to_csv(data_root_dir / ("crosstab_wave" + str(wave) + ".csv"), index=False)
        print("Processed wave %d: %d households" % (wave, np.sum(wave_df["count_value"])))

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("", type=str, help="")
    # args = parser.parse_args()

    main()
