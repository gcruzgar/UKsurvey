"""
author: Gonzalo
date started: 06/11/18

This script generates a table of correlations for the selected features.
"""

import pandas as pd 
import numpy as np 

cols = ['type', 'tenure', 'beds', 'rooms', 'size']

wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}
wave = wn[1] # select wave

df = pd.read_csv(wave + '_hhresp.tab', sep = '\t')

feature_df = df[[wave+'_hhtype_dv', wave+'_tenure_dv', wave+'_hsbeds', wave+'_hsrooms', wave+'_hhsize']]
feature_df.columns = cols

feature_df.corr()