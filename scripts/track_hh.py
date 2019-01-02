#!/usr/bin/env python3
"""
This script generates a dataframe with the value of a chosen parameter of any given household over time.
There is the option to save a list of households IDs to CSV. 
This will generate a file where each row is the IDs of a household at every wave.
"""
import pandas as pd 
import numpy as np 
import argparse
from common import hh_list, track_hh

def main(): 

    pidp = args.p    # individual (needed to match households)
    if args.var_name.startswith("_"): # variable to extract
        var_name = args.var_name    
    else:
        var_name = '_'+args.var_name
    waves = [1,2,3,4,5,6,7] # waves to include

    print("pidp: %d" % pidp)
    print("variable: %s\n" % var_name)

    hidp_list = hh_list() # obtain list of household ids to match each hh

    print("Extracting variable data...")
    var_dict = {}
    for wave in waves:
        waveletter = chr(96+wave) # 1 -> "a" etc
        data = pd.read_csv('data/'+waveletter+'_hhresp.tab', sep ='\t')
        var_dict[wave] = data[[waveletter+'_hidp', waveletter+var_name]]

    track_vals = track_hh(pidp, waves, var_name, hidp_list, var_dict)

    # generate dataframe for easier data handling
    track_df = pd.DataFrame(data=[pidp], columns=['pidp']) 
    for wave in waves: 
        waveletter = chr(96+wave) # 1 -> "a" etc
        track_df[waveletter+var_name] = track_vals[wave-1]
    print(track_df)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int, help="personal identifier to process, use the pidp of any member of the household of interest.", 
        nargs='?', default=280165)
    parser.add_argument("var_name", type=str, help="variable to extract, e.g. hhsize.", 
        nargs='?', default='_hhsize')        
    args = parser.parse_args()

    main()
