#!/usr/bin/env python3
"""
author: Gonzalo
date started: 01/11/18

This script creates 5-dimensional contingency tables.
Also includes the option to unstack the tables and filter the data.
Maps survey data to census definitions before unstacking.
It saves a dataframe with the counts of this 5-dimensional table to CSV.
"""
import argparse
import pandas as pd 
import numpy as np
from pathlib import Path
from common import remap, constrain

pd.options.mode.chained_assignment = None # supress SettingWithCopyWarning - False positive when using remap

data_root_dir = Path("./data")

def contingency_table(wave):

    waveletter = chr(96+wave) # 1 -> "a" etc
    data = pd.read_csv(data_root_dir / ("UKDA-6614-tab/tab/ukhls_w" + str(wave)) / (waveletter + '_hhresp.tab'), sep = '\t')
    #data = pd.read_csv(data_root_dir / (waveletter+'_hhresp.tab'), sep ='\t')
    # hhsamp = pd.read_csv(data_root_dir / (waveletter+'_hhsamp.tab'), sep ='\t')

    # need to remove cases with one or more missing rooms/beds values *before* aggregating rooms
    data = data[(data[waveletter+'_hsrooms'] > 0) & (data[waveletter+'_hsbeds'] >= 0)]
    assert len(data[(data[waveletter+'_hsrooms'] > 0) & (data[waveletter+'_hsbeds'] < 0)]) == 0
    assert len(data[(data[waveletter+'_hsrooms'] < 1) & (data[waveletter+'_hsbeds'] >= 0)]) == 0

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
        6: 1, 8: 1, 10: 1, 11: 1, 12: 1, 19: 1, 20: 1, 21: 1, # couples
        16: 4, 17:4, 18: 4, 22: 4, 23: 4 # mixed
    }
    data = remap(data, waveletter+'_hhtype_dv', hhtype_map)

    # """ randomly assigning couples to married or cohabiting couples """
    # couples = data.index[data[waveletter+'_hhtype_dv'] == 1].tolist()
    # np.random.seed(9238456) # set seed to always get the same "random" numbers
    # to_change = np.random.choice(couples, size = round(0.25*len(couples)), replace=False)
    # data.loc[to_change, waveletter+'_hhtype_dv'] = 2

    # check whether couples are married or cohabiting
    marital_data = pd.read_csv(data_root_dir / ("UKDA-6614-tab/tab/ukhls_w" + str(wave)) / (waveletter + '_indall.tab'), sep = '\t')[['pidp', waveletter+'_mastat_dv']]
    couples = data.loc[data[waveletter+'_hhtype_dv'] == 1, [waveletter+'_hhtype_dv', waveletter+'_hidp', waveletter+'_hrpid']]
    couples = couples.merge(marital_data, how='left', left_on=waveletter+'_hrpid', right_on='pidp').set_index(couples.index)
    to_change = couples.index[couples[waveletter+'_mastat_dv']==10.0].to_list()
    data.loc[to_change, waveletter+'_hhtype_dv'] = 2    

    #data[waveletter+'_tenure_dv'].replace(tenure_map, inplace=True)

    a = data[waveletter+'_hhtype_dv']
    b = data[waveletter+'_tenure_dv']
    c = data[waveletter+'_hsrooms']
    d = data[waveletter+'_hhsize']
    e = data[waveletter+'_hsbeds']
    
    # f = hhsamp[waveletter+'_dweltyp']

    ctab = pd.crosstab(a, [b, c, d, e]) #add ',f' after 'e' too include dwelling 
    """ indexing requires unstacking """
    # unstack returns a multiindex Series not a dataframe
    # so construct a dataframe and make the multiindex into columns so we can filter
    ctab_us = pd.DataFrame({"frequency": ctab.unstack()}).reset_index()

    """ rename columns so they are consistent between files """
    ctab_us.columns = ['tenure', 'rooms', 'occupants', 'bedrooms', 'hhtype', 'frequency'] # add 'dwelling' after size if included in data
    return ctab_us

""" data processing """
def data_filter(wave_df):
    return wave_df.loc[(wave_df['frequency']!=0)]
                    # & (wave_df['dwelling']>0]

def main():

    if isinstance(args.wave, int):
        args.wave = [args.wave]

    """ automated """
    for wave in args.wave:
        ctab_us = contingency_table(wave) # create contingency table
        wave_df = data_filter(ctab_us) # filter table 
        wave_df.to_csv(data_root_dir / ("crosstab_wave" + str(wave) + ".csv"), index=False) #save output
        print("Processed wave %d: %d households" % (wave, np.sum(wave_df["frequency"])))
        print("Number of occupied states: %d\n" % len(wave_df))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wave", type=int, help="wave number(s) to process, defaults to wave 3 if no argument is provided", nargs='*', default=3)
    args = parser.parse_args()

    main()
