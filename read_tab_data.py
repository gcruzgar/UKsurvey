"""
author: Gonzalo
date started: 18/10/18

WIP
Note: it requires the data to be in the same folder as the path is not set.

This script compares the individuals that took part in two waves of the Understanding Society Survey.
It outputs a list of members that are in wave a and wave b.

An individual is then chosen (could choose at random) and the script checks which waves they are a member of.
A list of household IDs is produced for the individual.
This does not mean that the individual belongs to more than one household.
The household identifier is unique for every wave.  

Things to do:
-extract rows from each wave (for an individual) into a single dataframe to observe evolution of the individual. 
-can we identify when an event happens? and what triggers it?
"""

import pandas as pd 

# name of files/waves to compare
filename1 = "a_indresp.tab"
filename2 = "b_indresp.tab"

def wave_intercept(filename1, filename2):
    # Check which individuals from a wave are present in the next wave.
     
    df1 = pd.read_csv(filename1, sep='\t')
    df2 = pd.read_csv(filename2, sep='\t')

    df1_id = df1['pidp']
    df2_id = df2['pidp']

    #intercept between two lists:
    id_intercept = set(df2_id).intersection(set(df1_id))
    print("%d out of %d individuals present in both waves" % (len(id_intercept), len(df2_id)))
    print("%d new individuals compared to previous wave\n" % (len(df2_id) - len(df1_id)))
    return list(id_intercept)

id_intercept = wave_intercept(filename1,filename2)

# list of files/waves to read through & id of individual to check
filelist = ["a_indresp.tab", "b_indresp.tab", "c_indresp.tab", 
    "d_indresp.tab", "e_indresp.tab", "f_indresp.tab", "g_indresp.tab"]
pidp = id_intercept[549]

def household_id_list(filelist, pidp):
    # For a set of waves, obtain a list of household IDs belonging to the same individual.

    hidp_list = []
    wave_list = []
    wn = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g'}
    c=1
    for name in filelist:
        print("Loading wave %d data..." % c)
        df = pd.read_csv(name, sep='\t')
        if pidp in df['pidp'].values:
            kword = wn[c]+'_hidp'
            hidp = df.loc[df['pidp'] == pidp, kword].values
            hidp_list.append(hidp)
            wave_list.append(c)
        c+=1
    print("\nIndividual %d present in waves {}".format(wave_list) % pidp)    
    return hidp_list

hidp_list = household_id_list(filelist, pidp)