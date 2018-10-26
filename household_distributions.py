"""
author: Gonzalo
date started: 26/10/18
This script gives a count of each household type at each wave.

Things to do:
-percentage changes in household distribution
"""

import pandas as pd 
from collections import Counter

filelist = ["a_hhresp.tab", "b_hhresp.tab", "c_hhresp.tab", 
"d_hhresp.tab", "e_hhresp.tab", "f_hhresp.tab", "g_hhresp.tab"]

var_key = '_hhtype_dv'

possible_status = {
    1: "1 male, aged 65+, no children",
    2: "1 female, age 60+, no children",
    3: "1 adult under pensionable age, no children",
    4: "1 adult, 1 child",
    5: "1 adult, 2 or more children",
    6: "Couple both under pensionable age, no children",
    8: "Couple 1 or more over pensionable age, no children",
    10: "Couple with 1 child",
    11: "Couple with 2 children",
    12: "Couple with 3 or more children",
    16: "2 adults, not a couple, both under pensionable age, no children",
    17: "2 adults, not a couple, one or more over pensionable age, no children",
    18: "2 adults, not a couple, 1 or more children",
    19: "3 or more adults, no children ,incl. at least one couple",
    20: "3 or more adults, 1-2 children ,incl. at least one couple",
    21: "3 or more adults, >2 children ,incl. at least one couple",
    22: "3 or more adults, no children, excl. any couples",
    23: "3 or more adults, 1 or more children, excl. any couples",
    -2: "refusal",
    -9: "missing",
    -8: "inapplicable",
    -7: "proxy",
    -1: "don't know" 
}

def household_distribution(filelist, var_key):

    hh_dist_waves = {}
    wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}
    c=1

    for name in filelist:        
        
        df = pd.read_csv(name, sep='\t')

        kword = wn[c] + var_key
        v = df[kword]

        hh_dist = Counter(v)  # or use df[kword].value_counts()
        hh_dist_waves[wn[c]] = hh_dist
        c+=1
    return hh_dist_waves

hh_dist_waves = household_distribution(filelist, var_key)
