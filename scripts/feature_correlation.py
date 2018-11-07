"""
author: Gonzalo
date started: 06/11/18

This script generates a table of correlations for the selected features.
"""

import pandas as pd 
import numpy as np 

def feature_correlation(wave):
    cols = ['type', 'tenure', 'beds', 'rooms', 'size']
    df = pd.read_csv(wave + '_hhresp.tab', sep = '\t')

    feature_df = df[[wave+'_hhtype_dv', wave+'_tenure_dv', wave+'_hsbeds', wave+'_hsrooms', wave+'_hhsize']]
    feature_df.columns = cols

    fc = feature_df.corr()
    return fc

wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}

feature_dict = {}
for wave in wn.values():
    print("Loading wave %s" % wave)
    feature_dict[wave]= feature_correlation(wave)
