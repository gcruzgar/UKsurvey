"""
author: Gonzalo
date started: 07/11/18

This script generates the total number of rooms in each household.
Then outputs frequency distribution.

To do:
-filter data before sum (remove -9, -8, -1 values)
"""
import pandas as pd 
from collections import Counter

def total_rooms(wave):
    df = pd.read_csv(wave+"_hhresp.tab", sep = '\t')

    bedrooms = df[wave+'_hsbeds']
    rooms = df[wave+'_hsrooms']

    total = bedrooms + rooms
    total_count = Counter(total)
    return total_count

wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}

rooms_dict = {}
for wave in wn.values():
    print("Loading wave %s..." % wave)
    rooms_dict[wave] = total_rooms(wave)
